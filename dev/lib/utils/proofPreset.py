"""
A container for proof list, with a .getPreset() method
to convert tagged proof doc into preset (list of dicts)
that can be saved as a JSON file
"""

class XMLtagError(Exception):
    pass

class ProofPreset:
    """
    Initialize with list of input and tag name used
    ProofPreset.getPreset() will return list of dicts for JSON
    """
    def __init__(self, inputList, tagName):
        """
        inputList is list, doesn't have to be "clean"
        tagName is a string, the tag used in proof doc
        tagName for <group>proof</group> is "group"
        """
        self.inputList = self._cleanList(inputList)
        self.tagName = tagName

        # Run some basic validation on init
        self._checkForTags()
        self._checkXMLtagsSequence()

    def _cleanList(self, listToClean):
        """
        Get rid of leading and trailing whitespaces all at once
        Only include non-empty items in returned list
        """
        return [item.strip() for item in listToClean if item.strip()]

    def _isTag(self, item):
        """
        Return if item is tag (open or close)
        """
        return item == "<%s>" % self.tagName or item == "</%s>" % self.tagName

    def _checkForTags(self):
        """
        Make sure object has opening & closing tags at all
        """
        if not "<%s>" % self.tagName in self.inputList\
        and "</%s>" % self.tagName in self.inputList:
            raise XMLtagError("Tags should be <tag>content here</tag>")

    def _checkXMLtagsSequence(self):
        """
        Make sure open tags have closing ones:
        [<tag>, </tag>, <tag>, </tag>]
        """
        openTag = True
        openTagCount = 0
        closeTagCount = 0

        for tag in self.getTags():
            if openTag and tag == "<%s>" % self.tagName:
                openTagCount += 1
                openTag = False # Next is supposed to be close tag
            elif not openTag and tag == "</%s>" % self.tagName:
                closeTagCount += 1
                openTag = True # Next is supposed to be open tag
            else:
                raise XMLtagError("Incorrect <tag></tag> sequence")

        if openTagCount != closeTagCount:
            raise XMLtagError("Not all tags are paired")

    def getTags(self):
        """
        Return a list of tags only
        """
        return [item for item in self.inputList if self._isTag(item)]

    def getNonTags(self):
        """
        Return a list of non tags
        """
        return [item for item in self.inputList if not self._isTag(item)]

    def getPreset(self):
        """
        Return a list of dicts from proofDoc formatted like so:
        [{tagName: group title, "contents": [content1, content2, etc.]}]
        tagName is the tag it should look out for.

        Proof doc should be written like example below.
        First line after opening tag is the title.
        <group>
        UC, lc, and numerals
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        </group>
        """
        # Check if tags are in sequence before anything else
        self._checkXMLtagsSequence()

        presetList = []
        startGroup = False

        for line in self.inputList:
            # Open tag: initialize and move on
            if "<%s>" % self.tagName in line:
                group = {}
                startGroup = True
                continue

            # Close tag: add group to presetList and move on
            elif "</%s>" % self.tagName in line:
                presetList.append(group)
                continue

            # Title line: add title to group[self.tagName] and initialize presets
            if startGroup:
                group[self.tagName] = line.strip()
                group["type size"] = ""
                group["leading"] = ""
                group["print"] = False
                group["contents"] = []
                startGroup = False # not the start of group anymore

            # Middle of block: just add line to group["contents"]
            else:
                group["contents"].append(line)

        return presetList


if __name__ == "__main__":
    import os.path

    fileDir = os.path.dirname(__file__)
    testFileDir = os.path.join(fileDir, "tests", "resources", "proofDocTest.txt")

    with open(testFileDir, "r") as testFile:
        readList = testFile.readlines()

    # Simple testing:
    preset = ProofPreset(readList, "group")
    print(preset.getTags())
