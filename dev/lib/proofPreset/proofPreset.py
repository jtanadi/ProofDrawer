"""
Proof preset-related stuff in here
"""

class XMLtagError(Exception):
    pass

class ProofPresetError(Exception):
    pass

class ProofPreset:
    """
    A proof preset object for ProofDrawer().

    Only top-most structure exists when initialized:
    {"name": presetName, "groups": []}

    Use ProofPreset.importProof(proofGroups)
    to turn an XML-tagged proofGroups object (string or list)
    into a preset.

    proofGroups is a collection of proof groups,
    and they should be structured like:
    <group>
    UC, numerals
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    0123456789
    </group>
    <group>
    lc
    abcdefghijklmnopqrstuvwxyz
    </group>

    ProofPreset.getGroups() will return the groups,
    formatted as a list of dicts:
    [
        {
            "group": "UC, numerals",
            "contents": [
                "ABCEFGHIJKLMNOPQRSTUVWXYZ,
                "0123456789"
            ]
        }
    ]

    ProofPreset.getPreset() will return a preset object
    that can be saved as a JSON file:
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
            },
            {
                "group": "lc",
                "order": 2,
                "type size": 12,
                "leading": 14,
                "print": False,
                "contents": [
                    "abcefghijklmnopqrstuvwxyz"
                ]
            }
        ]
    }
    """
    def __init__(self, presetName="myPreset"):
        """
        Initialize an empty ProofPreset object
        """
        self.preset = {}
        self.preset["name"] = presetName
        self.preset["groups"] = []

        self.proofGroups = None

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
        return item == "<group>" or item == "</group>"

    def _getTags(self):
        """
        Return a list of tags
        """
        return [item for item in self.proofGroups if self._isTag(item)]

    def _checkForTags(self):
        """
        Make sure object has opening & closing tags at all
        """
        if "<group>" not in self.proofGroups and \
        "</group>" not in self.proofGroups:
            raise XMLtagError("<group> tags not in imported proofGroup")

    def _checkXMLtagsSequence(self):
        """
        Make sure open tags have closing ones:
        [<tag>, </tag>, <tag>, </tag>]
        """
        openTag = True
        openTagCount = 0
        closeTagCount = 0

        for tag in self._getTags():
            if openTag and tag == "<group>":
                openTagCount += 1
                openTag = False # Next is supposed to be close tag
            elif not openTag and tag == "</group>":
                closeTagCount += 1
                openTag = True # Next is supposed to be open tag
            else:
                raise XMLtagError("Incorrect <tag></tag> sequence")

        if openTagCount != closeTagCount:
            raise XMLtagError("Not all tags are paired")

    def _makePresetGroups(self):
        """
        Return list of preset groups,
        converted from proofGroups
        """
        if not self.proofGroups:
            return []

        presetList = []
        startGroup = False
        order = 1

        for line in self.proofGroups:
            # Open tag: initialize and move on
            if "<group>" in line:
                group = {}
                startGroup = True
                continue

            # Close tag: add group to presetList and move on
            elif "</group>" in line:
                presetList.append(group)
                continue

            # Title line: add title to group["group"] and initialize presets
            if startGroup:
                group["group"] = line.strip()
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

    def renamePreset(self, newName):
        """
        Rename preset
        """
        self.preset["name"] = newName

    def addGroup(self, newGroup, overwrite=False):
        """
        Add one group. (Keep loop outside.)

        newGroup is a dict that AT LEAST contains a name,
        but can include other preset items:
        {
            "group": "new group dict",
            "type size": 12,
            "leading": 14,
            "print": False,
            "contents": "abcde"
        }

        If NOT overwriting, raise an error when
        newGroup exactly matches another group. 
        """
        # if not isinstance(newGroup, dict):
        #     raise TypeError("newGroup has to be a dictionary")
        # elif not newGroup[self.tagName]:
        #     raise ProofPresetError("newGroup needs a name (tagName)")

        # if not overwrite and 
        
        # for group in self.preset["groups"]:

        pass

    def removeGroup(self, groupName):
        """
        Remove group.

        groupName is a string. If it doesn't exist,
        raise an error.
        """
        if groupName not in self.preset["groups"]:
            raise ProofPresetError("Group doesn't exist")

        for group in self.preset["groups"]:
            if group["group"] == groupName:
                del group

    def importProof(self, proofToImport):
        """
        Import collection of proof groups and perform
        some basic cleaning and validation

        proofToImport can be a string or list
        """
        if isinstance(proofToImport, str):
            proofToImport = proofToImport.split("\n")

        self.proofGroups = self._cleanList(proofToImport)

        self._checkForTags()
        self._checkXMLtagsSequence()

        self.preset["groups"] = self._makePresetGroups()

    def importPreset(self, presetToImport, overwrite=False):
        """
        Import a proof preset (eg. from JSON file).

        presetToImport is a dictionary that will be validated
        before the full thing is imported.

        If NOT overwriting, raise an error when there's
        already a stored preset["groups].
        """
        if not overwrite and self.preset["groups"]:
            raise ProofPresetError("There's already a preset in here")

        # validate imported preset
        if not presetToImport["name"]:
            raise ProofPresetError("Imported preset has no name")
        elif not presetToImport["groups"]:
            raise ProofPresetError("Imported preset has no groups")

        keysToValidate = ["group", "order", "type size",\
                          "leading", "print", "contents"]

        for group in presetToImport["groups"]:
            for key in keysToValidate:
                if not group[key]:
                    raise ProofPresetError("Imported preset is missing %s" % key)

        # import preset
        self.preset = presetToImport

    def getName(self):
        """
        Return Preset name
        """
        return self.preset["name"]

    def getGroups(self):
        """
        Return list of proof groups, without the preset info
        [
            {
                "group": UC,
                "contents": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            },
            {
                "group": lc,
                "contents": "abcdefghijklmnopqrstuvwxyz"
            }
        ]
        """
        returnGroups = []
        for group in self.preset["groups"]:
            tempDict = {}
            tempDict["group"] = group["group"]
            tempDict["contents"] = group["contents"]

            returnGroups.append(tempDict)

        return returnGroups

    def getPreset(self):
        """
        Return JSON-able preset in the following format:
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
        return self.preset


if __name__ == "__main__":
    import os.path

    fileDir = os.path.dirname(__file__)
    testFileDir = os.path.join(fileDir, "tests", "resources", "proofDocTest.txt")

    with open(testFileDir, "r") as testFile:
        readList = testFile.readlines()

    # Simple testing:
    preset = ProofPreset("myPreset")
    preset.importProof(readList)
    print(preset.getPreset())
