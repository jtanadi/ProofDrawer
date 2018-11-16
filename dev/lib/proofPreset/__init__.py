"""
Proof preset-related stuff in here
"""

from proofPreset import utils
from proofPreset.errors import ProofPresetError

import copy
import json

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
            "name": "UC, numerals",
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
                "name": "UC, numerals",
                "type size": 12,
                "leading": 14,
                "print": True,
                "contents": [
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    "0123456789"
                ]
            },
            {
                "name": "lc",
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

        self.xmlGroups = None

        self.nameCopyIndex = 1
        self.keysInGroup = ["name", "type size", "leading",\
                            "print", "contents"]

    def _addMissingKeysToGroup(self, groupToProcess):
        """
        Return new dict with missing keys added
        """
        dictWithAddedKeys = {}

        for key in self.keysInGroup:
            if key in groupToProcess:
                dictWithAddedKeys[key] = groupToProcess[key]
            else:
                if key == "print":
                    dictWithAddedKeys[key] = False
                elif key == "contents":
                    dictWithAddedKeys[key] = []
                else:
                    dictWithAddedKeys[key] = ""

        return dictWithAddedKeys

    def _removeUnneededKeysInGroup(self, groupToProcess):
        """
        Return new dict with only keys in self.keysInGroup
        """
        return {key:value for key, value in groupToProcess.items()\
                if key in self.keysInGroup}

    def _makePresetGroupsFromXML(self):
        """
        Return list of preset groups,
        converted from proofGroups
        """
        presetList = []
        startGroup = False

        for line in self.xmlGroups:
            # Open tag: initialize and move on
            if "<group>" in line:
                group = {}
                startGroup = True
                continue

            # Close tag: add group to presetList and move on
            elif "</group>" in line:
                presetList.append(group)
                continue

            # Title line: add title to group["name"] and initialize presets
            # This is a little shorter than iterating & using if statements...
            if startGroup:
                group["name"] = line.strip()
                group["type size"] = ""
                group["leading"] = ""
                group["print"] = False
                group["contents"] = []
                startGroup = False # not the start of group anymore

            # Middle of block: just add line to group["contents"]
            else:
                group["contents"].append(line)

        return presetList

    def renamePreset(self, newName):
        """
        Rename preset
        """
        self.preset["name"] = newName

    def getPresetName(self):
        """
        Return Preset name
        """
        return self.preset["name"]

    def getGroupNames(self):
        """
        Return a list of all group names
        """
        return [group["name"] for group in self.preset["groups"]]

    def getGroups(self, verbose=True):
        """
        Return list of ProofPreset groups.

        If NOT verbose, return without preset info:
        [
            {
                "name": UC,
                "contents": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            },
            {
                "name": lc,
                "contents": "abcdefghijklmnopqrstuvwxyz"
            }
        ]
        """
        if not verbose:
            returnGroups = []
            for group in self.preset["groups"]:
                tempGroup = {}
                tempGroup["name"] = group["name"]
                tempGroup["contents"] = group["contents"]

                returnGroups.append(tempGroup)

        else:
            returnGroups = copy.deepcopy(self.preset["groups"])

        return returnGroups

    def getPreset(self, jsonFormat=False):
        """
        Return preset, either as Py dict, or when
        jsonFormat is True, as a JSON object.

        Object structure:
        {
            "name": presetName,
            "groups": [
                {
                    "name": "UC, numerals",
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
        if jsonFormat:
            return json.dumps(self.preset, indent=2)
        return self.preset

    def addGroup(self, groupToAdd, overwrite=False):
        """
        Add one group. (Keep loop outside.)

        groupToAdd is a dict that AT LEAST contains a name,
        but can include other preset items:
        {
            "name": "new group dict",
            "type size": 12,
            "leading": 14,
            "print": False,
            "contents": "abcde"
        }

        groupToAdd will always be added to the END of
        the groups list. For anything more precise,
        use py list methods on self.preset["groups"]

        If NOT overwriting, add "index" to end of name:
        newGroup, newGroup-1, newGroup-2
        """
        if not isinstance(groupToAdd, dict):
            raise TypeError("groupToAdd has to be a dictionary")
        elif "name" not in groupToAdd.keys():
            raise ProofPresetError("groupToAdd needs a name")

        # Copy so we're not referencing the dict being passed in
        newGroup = copy.deepcopy(groupToAdd)

        # Remove unnecessary keys & add missing keys
        newGroup = self._removeUnneededKeysInGroup(newGroup)
        newGroup = self._addMissingKeysToGroup(newGroup)

        # Not overwriting: just add to groups
        if not overwrite:
            if newGroup["name"] in self.getGroupNames():
                newGroup["name"] += "-%s" % self.nameCopyIndex
                self.nameCopyIndex += 1

            self.preset["groups"].append(newGroup)

        # Overwriting: find existing group with same name,
        # and copy newGroup to saved group
        else:
            for group in self.preset["groups"]:
                if group["name"] == newGroup["name"]:
                    for key in group:
                        group[key] = newGroup[key]

    def removeGroup(self, groupToRemove):
        """
        Remove group by name or index.

        groupToRemove can be a str or int, and must
        be a valid name or valid index.
        """
        if isinstance(groupToRemove, str):
            if groupToRemove not in self.getGroupNames():
                raise ProofPresetError("Group doesn't exist")

            for index, group in enumerate(self.preset["groups"]):
                if group["name"] == groupToRemove:
                    del self.preset["groups"][index]

        elif isinstance(groupToRemove, int):
            if groupToRemove > len(self.preset["groups"] - 1):
                raise ProofPresetError("Group doesn't exist")
            del self.preset["groups"][groupToRemove]

    def importFromXML(self, xmlTaggedObj):
        """
        Import XML-tagged string or list, and perform
        some basic cleaning and validation.

        If xmlTaggedObj is a string:
        "<group>\nUC\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n</group>"

        if xmlTaggedObj is a list:
        ["<group>", "UC", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "</group>"]
        """
        if isinstance(xmlTaggedObj, str):
            newObj = xmlTaggedObj.split("\n")
        elif isinstance(xmlTaggedObj, list):
            newObj = copy.deepcopy(xmlTaggedObj)

        self.xmlGroups = utils.cleanList(newObj)

        if not self.xmlGroups:
            raise ProofPresetError("List is empty!")

        utils.checkForTags(self.xmlGroups, "group")
        utils.checkXMLtagsSequence(self.xmlGroups, "group")

        self.preset["groups"] = self._makePresetGroupsFromXML()

    def importFromJSON(self, jsonObj, overwrite=False):
        """
        Import JSON object and convert to ProofPreset
        The overwrite behaviour is the same as ProofPreset.importPreset()

        This method doesn't read files
        """
        presetFromJSON = json.loads(jsonObj)
        self.importPreset(presetFromJSON, overwrite)

    def importPreset(self, presetToImport, overwrite=False):
        """
        Import a WHOLE ProofPreset (py dict).
        To import from JSON, use ProofPreset.importFromJSON()

        presetToImport is a dictionary. Whenever a group
        in presetToImport is missing a setting, add it
        with empty values.

        If overwrite is False, raise an error when there's
        already a stored preset["groups"].
        """
        if not overwrite and self.preset["groups"]:
            raise ProofPresetError("There's already a preset in here.")

        # Validate imported preset
        if not presetToImport["name"]:
            raise ProofPresetError("Imported preset has no name")
        elif not presetToImport["groups"]:
            raise ProofPresetError("Imported preset has no groups")

        # Copy so we're not changing imported object later
        newPreset = copy.deepcopy(presetToImport)

        # Remove unneeded keys & add missing keys
        for group in newPreset["groups"]:
            group = self._removeUnneededKeysInGroup(group)
            group = self._addMissingKeysToGroup(group)

        # Import preset, sort by group order, and reorder
        self.preset = newPreset


if __name__ == "__main__":
    import os.path

    fileDir = os.path.dirname(__file__)
    testFileDir = os.path.join(fileDir, "tests", "resources", "proofDocTest.txt")

    with open(testFileDir, "r") as testFile:
        readList = testFile.readlines()

    # Simple testing:
    preset = ProofPreset("myPreset")
    preset.importFromXML(readList)
    print(preset.getPreset())
