"""
Proof preset-related stuff in here
"""

class XMLtagError(Exception):
    pass

class ProofPreset:
    """
    A proof preset for ProofDrawer().

    Use ProofPreset.importProof(proofGroups, tagName)
    to turn an XML-tagged proof string into a preset.

    proofGroups is a collection of proof groups,
    each should be structured like:
    <group>
    UC, numerals
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    0123456789
    </group>

    On import, the groups are converted into a List:
    [<group>, "UC, numerals", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0123456789"]

    ProofPreset.getPreset() will return a preset object
    that can be saved as a JSON file.

    Final preset object's structure:
    {
        "name": presetName,
        "groups": [
            {
                "group": "UC, numerals",
                "order": 1,
                "type size": 12,
                "leading": 14,
                "print": True,
                "contents": [
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    "0123456789"
                ]
            }
        ]
    }
    """
    def __init__(self, presetName):
        """
        Initialize an empty ProofPreset object
        presetName is string.
        """
        self.preset = {}
        self.preset["name"] = presetName
        self.preset["groups"] = []

        self.inputList = None
        self.tagName = None

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

    def importProof(self, proofGroups, tagName):
        """
        Import collection of proof groups and perform
        some basic cleaning and validation

        proofGroups can be a string or list
        
        tagName is a string—the tag used in to separate
        groups in proofGroups.
        For example, tagName for <group>proof</group> is "group"
        """
        if proofGroups is str:
            proofGroups = proofGroups.split("\n")

        self.inputList = self._cleanList(proofGroups)
        self.tagName = tagName

        self._checkForTags()
        self._checkXMLtagsSequence()

    def getTags(self):
        """
        Return a list of tags only
        """
        if not self.tagName:
            return None
        return [item for item in self.inputList if self._isTag(item)]

    def getNonTags(self):
        """
        Return a list of non tags
        """
        return [item for item in self.inputList if not self._isTag(item)]

    def getPresetList(self):
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
        if not self.inputList:
            return []

        # Check if tags are in sequence before anything else
        self._checkXMLtagsSequence()

        presetList = []
        startGroup = False
        order = 1

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
                group["order"] = order
                group["type size"] = ""
                group["leading"] = ""
                group["print"] = False
                group["contents"] = []
                startGroup = False # not the start of group anymore
                order += 1

            # Middle of block: just add line to group["contents"]
            else:
                group["contents"].append(line)

        return presetList    

    def getPreset(self):
        self.preset["groups"] = self.getPresetList()
        return self.preset


if __name__ == "__main__":
    import os.path

    fileDir = os.path.dirname(__file__)
    testFileDir = os.path.join(fileDir, "tests", "resources", "proofDocTest.txt")

    with open(testFileDir, "r") as testFile:
        readList = testFile.readlines()

    # Simple testing:
    preset = ProofPreset("myPreset")
    preset.importProof(readList, "group")
    print(preset.getPreset())
