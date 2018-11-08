"""
For converting proof doc into preset file (JSON)
"""

class XMLtagError(Exception):
    pass

class ProofConverter:
    def __init__(self, inputList, tagName):
        self.inputList = inputList
        self.tagName = tagName

        # Run some basic validation on init
        self._checkForTags()
        self._checkXMLtagsSequence()
        
    def _checkForTags(self):
        """
        Make sure object has opening & closing tags at all
        """
        if not ("<%s>" % self.tagName and "</%s>" % self.tagName) in self.inputList:
            raise XMLtagError("Tags should be <tag>content here</tag>")

    def _checkXMLtagsSequence(self):
        """
        Make sure open tags have closing ones:
        [<tag>, </tag>, <tag>, </tag>]
        """
        openTag = False
        for tag in self.getTags():
            # Detect open tag and continue
            if not openTag and "<" in tag and "/" not in tag:
                tagName = tag.strip("<").strip(">")
                openTag = True

            # If tag is open, close it if possible
            # if not possible, raise XMLtagError.
            # (Closing tag must match opening tag)
            else:
                if "</%s>" % tagName in tag:
                    openTag = False
                else:
                    raise XMLtagError("Incorrect <tag></tag> sequence")

    def getTags(self):
        """
        Return a list of tags only
        """
        return [item.strip() for item in self.inputList\
                if "<%s>" % self.tagName in item or "</%s>" % self.tagName in item]

    def returnAllButTags(self):
        """
        Return everything but tag?
        """
        pass
        # return stringWithTags.replace("<%s>" % self.tagName, "")\
        #                     .replace("</%s>" % self.tagName, "")


    def parseProofDoc(self):
        """
        Return a list of dicts from proofDoc formatted like so:
        [{tagName: group title, "contents": [content1, content2, etc.]}]
        tagName is the tag it should look out for.

        Proof doc should be written like example below.
        First line after opening tag is the title
        <group>
        UC, lc, and numerals
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        </group>
        """
        # Check if tags are in sequence before anything else
        self._checkXMLtagsSequence()

        proofList = []
        startGroup = False

        for line in self.inputList:
            # Skip over empty items (linebreak, etc.)
            cleanLine = line.strip()
            if not cleanLine:
                continue

            # Open tag: initialize and move on
            if "<%s>" % self.tagName in cleanLine:
                group = {}
                startGroup = True
                continue

            # Close tag: add group to proofList and move on
            elif "</%s>" % self.tagName in cleanLine:
                proofList.append(group)
                continue

            # Title line: add title to group[self.tagName] and initialize contents list
            if startGroup:
                group[self.tagName] = line.strip()
                group["contents"] = []
                startGroup = False # not the start of group anymore

            # Middle of block: just add line to group["contents"]
            else:
                group["contents"].append(cleanLine)

        return proofList


if __name__ == "__main__":
    import os.path

    fileDir = os.path.dirname(__file__)
    testFileDir = os.path.join(fileDir, "tests", "resources", "proofDocTest.txt")

    testFile = open(testFileDir, "r")
    readList = testFile.readlines()
    testFile.close()

    # Simple testing:
    preset = Proof2Preset(readList, "group")
    print(preset.parseProofDoc())
