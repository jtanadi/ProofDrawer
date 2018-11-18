"""
Proof preset-related stuff in here
"""

from proofPreset import utils
from proofPreset.errors import ProofPresetError

import copy
import json
import os.path

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
                "typeSize": 12,
                "leading": 14,
                "print": True,
                "contents": [
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    "0123456789"
                ]
            },
            {
                "name": "lc",
                "typeSize": 12,
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

        self.groupNameCount = {}
        self.keysInGroup = ["name", "typeSize", "leading",\
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
                group["typeSize"] = ""
                group["leading"] = ""
                group["print"] = False
                group["contents"] = []
                startGroup = False # not the start of group anymore

            # Middle of block: just add line to group["contents"]
            else:
                group["contents"].append(line)

        return presetList

    def _inspectAndFixGroupNames(self, restartCount=False):
        """
        On fresh XML, JSON, or preset import, count how many
        times the same group name appears. If more than once,
        append a "count" to all but the first group.

        Counts start at "-0", but those are never shown
        (ie. "original" name is always "-0"):
        groupName, groupName-1, groupName-2, etc.

        When restartCount=True, self.groupNameCount -> empty dict
        Do this when importing an entire preset
        """
        if restartCount:
            self.groupNameCount = {}

        groupNames = self.getGroupNames()

        # Do an overall count of all groupNames
        # use list.count() instead of incrementing
        # so we can skip same names as we iterate
        for name in groupNames:
            if name not in self.groupNameCount.keys():
                nameCount = groupNames.count(name)
                self.groupNameCount[name] = nameCount

        # For all names that appear more than once,
        # append a "count"
        for countedName, value in self.groupNameCount.items():
            if value <= 1:
                continue

            # Start count at 0 but don't append "-0"
            nameCount = 0
            for group in self.preset["groups"]:
                if group["name"] == countedName:
                    if nameCount == 0:
                        nameCount += 1
                        continue
                    group["name"] += "-%s" % nameCount
                    nameCount += 1

    def _checkForNameCopy(self, newName):
        """
        Return a "count" appended to name if name
        already exists in the Preset groups.

        groupName, groupName-1, groupName-2, etc.
        """
        groupNames = self.getGroupNames()
        nameToReturn = newName

        # If newName hasn't been tracked,
        # initialize key/value in dict
        if newName not in groupNames:
            self.groupNameCount[newName] = 1

        # Else, append count to nameToReturn and
        # add increment newName count
        else:
            nameToReturn += "-%s" % self.groupNameCount[newName]
            self.groupNameCount[newName] += 1

        return nameToReturn

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
                "name": "UC",
                "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
            },
            {
                "name": "lc",
                "contents": ["abcdefghijklmnopqrstuvwxyz"]
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
                    "typeSize": 12,
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

    def addGroup(self, groupToAdd, overwrite=False, _checkForCopy=True):
        """
        Add one group. (Keep loop outside.)

        groupToAdd is a dict that AT LEAST contains a name,
        but can include other preset items:
        {
            "name": "new group dict",
            "typeSize": 12,
            "leading": 14,
            "print": False,
            "contents": "abcde"
        }

        groupToAdd will always be added to the END of
        the groups list. For anything more precise,
        use py list methods on self.preset["groups"]

        If NOT overwriting, add "index" to end of name:
        newGroup, newGroup-1, newGroup-2

        _checkForCopy is for internal testing
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
            if _checkForCopy:
                newGroup["name"] = self._checkForNameCopy(newGroup["name"])
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
                raise KeyError("Group doesn't exist")

            for group in self.preset["groups"]:
                if group["name"] == groupToRemove:
                    self.preset["groups"].remove(group)

        elif isinstance(groupToRemove, int):
            if groupToRemove > len(self.preset["groups"]) - 1:
                raise IndexError("Index out of range")
            del self.preset["groups"][groupToRemove]

    def moveGroup(self, currentIndex, newIndex):
        """
        Move group in currentIndex to newIndex.
        """
        if not isinstance(currentIndex, int) or\
        not isinstance(newIndex, int):
            raise TypeError("Only pass in index")

        if currentIndex > len(self.preset["groups"]) or\
        newIndex > len(self.preset["groups"]):
            # list.insert() doesn't raise IndexError
            raise IndexError("Index out of range")

        # Remove & capture currentIndex group &
        # insert into list at newIndex
        currentGroup = self.preset["groups"].pop(currentIndex)
        self.preset["groups"].insert(newIndex, currentGroup)

    def editGroup(self, groupToEdit, **kwargs):
        """
        Edit group by name or index.

        groupToEdit can be a str or int, and must
        be a valid name or valid index.

        The following arguments are any key/value pairs.
        Possible keys are: name, typeSize, leading, print, contents
        Anything else will be ignored.
        """
        if isinstance(groupToEdit, str):
            # Why not leave to KeyError?
            if groupToEdit not in self.getGroupNames():
                raise ValueError("Group name doesn't exist")

            for group in self.preset["groups"]:
                if groupToEdit == group["name"]:
                    groupToEdit = group

        elif isinstance(groupToEdit, int):
            # Why not leave to IndexError?
            if groupToEdit > len(self.preset["groups"]) - 1:
                raise IndexError("Index out of range")

            groupToEdit = self.preset["groups"][groupToEdit]

        for key, value in kwargs.items():
            if key not in self.keysInGroup:
                continue
            elif key == "name" and value in self.getGroupNames():
                raise ValueError("Name already exists")
            elif key == "print" and not isinstance(value, bool):
                raise TypeError("Group print setting has to be a boolean")
            elif key == "contents" and not isinstance(value, list):
                raise TypeError("Group contents has to be a list")

            groupToEdit[key] = value

    def importFromXML(self, xmlTaggedProof):
        """
        Import XML-tagged proof and convert to ProofPreset() object.
        xmlTaggedProof can be a directory, a string, or a list.
        
        Dir extensions can be .xml or .txt. 
        Recognized XML tags are <group> </group>

        If xmlTaggedProof is a string:
        "<group>\nUC\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n</group>"

        if xmlTaggedProof is a list:
        ["<group>", "UC", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "</group>"]

        This method performs some basic cleaning & validation,
        including ingnoring everything before first <group> tag
        and everything after last </group> tag.
        """
        if os.path.isdir(xmlTaggedProof):
            ext = os.path.splitext(xmlTaggedProof)[1].lower()
            if ext in (".xml", ".txt"):
                with open(xmlTaggedProof, "r") as xmlFile:
                    xmlObj = xmlFile.readlines()
        elif isinstance(xmlTaggedProof, str):
            xmlObj = xmlTaggedProof.split("\n")
        elif isinstance(xmlTaggedProof, list):
            xmlObj = copy.deepcopy(xmlTaggedProof)

        self.xmlGroups = utils.cleanList(xmlObj)

        if not self.xmlGroups:
            raise ProofPresetError("Imported XML object is empty")

        utils.checkForTags(self.xmlGroups, "group")
        utils.checkXMLtagsSequence(self.xmlGroups, "group")

        # Main import & fix groupNames
        self.preset["groups"] = self._makePresetGroupsFromXML()
        self._inspectAndFixGroupNames()

    def importFromJSON(self, jsonInput, overwrite=False):
        """
        Import JSON object and convert to a ProofPreset() object.
        jsonInput can be a directory or a JSON object.

        The overwrite behaviour is the same as ProofPreset.importPyDict()
        """
        jsonObj = None
        if os.path.isdir(jsonInput):
            ext = os.path.splitext(jsonInput)[1].lower()
            if ext == ".json":
                with open(jsonInput, "r") as jsonFile:
                    jsonObj = jsonFile.read()
        elif isinstance(jsonInput, str):
            jsonObj = jsonInput

        if not jsonObj:
            raise ProofPresetError("Invalid JSON input")

        presetFromJSON = json.loads(jsonObj)
        self.importPyDict(presetFromJSON, overwrite)

    def importPyDict(self, presetToImport, overwrite=False):
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
        # Maybe should clean contents?
        for group in newPreset["groups"]:
            group = self._removeUnneededKeysInGroup(group)
            group = self._addMissingKeysToGroup(group)

        # Import preset & fix groupNames
        self.preset = newPreset
        self._inspectAndFixGroupNames(restartCount=True)


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
