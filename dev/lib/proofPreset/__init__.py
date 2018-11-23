"""
Proof preset-related stuff in here
"""

import copy
import json
import os.path

from proofPreset import utils
from proofPreset.errors import ProofPresetError

class ProofPreset:
    """
    A proof preset object for ProofDrawer().

    Only top-most structure exists when initialized:
    {"name": presetName, "groups": []}

    Import / export methods:
    - importFromJSON(jsonInput, overwrite=False)
    - importPyDict(pyDictInput)
    - importFromXML(xmlTaggedInput)
    - exportToJSON(filePath)
    - exportToXML(filePath)

    Preset methods:
    - renamePreset()
    - duplicatePreset()

    Group methods:
    - addGroup(groupToAdd, overwrite=False)
    - removeGroup(groupToRemove)
    - moveGroup(currentIndex, newIndex)
    - editGroup(groupToEdit)

    Getters:
    - getPresetName()
    - getPreset()
    - getGroupNames(returnCopies=True)
    - getGroups(verbose=True)
    - getXMLGroups()
    """
    def __init__(self, presetName="myPreset"):
        """
        Initialize an empty ProofPreset object
        """
        self.preset = {}
        self.preset["name"] = presetName
        self.preset["groups"] = []

        self._xmlGroups = None

        self._groupNameCount = {}
        self._keysInGroup = ["name", "typeSize", "leading",\
                            "print", "contents"]

    def _addMissingKeysToGroup(self, groupToProcess):
        """
        Return new dict with missing keys added
        """
        dictWithAddedKeys = {}

        for key in self._keysInGroup:
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
        Return new dict with only keys in self._keysInGroup
        """
        return {key:value for key, value in groupToProcess.items()\
                if key in self._keysInGroup}

    def _countNameCopies(self, newName):
        """
        Return a "count" appended to name if name
        already exists in the Preset groups.

        groupName, groupName-1, groupName-2, etc.
        """

        # A while loop version, in case we want
        # to stop using self._groupNameCount dict...
        # baseName = newName
        # count = 1
        # while newName in groupNames:
        #     newName = "%s-%s" % (baseName, count)
        #     count += 1
        # return newName

        nameToReturn = newName
        # If newName hasn't been tracked,
        # initialize key/value in dict
        if newName not in self.getGroupNames():
            self._groupNameCount[newName] = 1

        # Else, append count to nameToReturn and
        # increment newName count
        else:
            nameToReturn += "-%s" % self._groupNameCount[newName]
            self._groupNameCount[newName] += 1

        return nameToReturn

    def _inspectAndFixGroupNames(self, restartCount=False):
        """
        On fresh XML, JSON, or preset import, count how many
        times the same group name appears. If more than once,
        append a "count" to all but the first group.

        Counts start at "-0", but those are never shown
        (ie. "original" name is always "-0"):
        groupName, groupName-1, groupName-2, etc.

        When restartCount=True, self._groupNameCount -> empty dict
        Do this when importing an entire preset
        """
        if restartCount:
            self._groupNameCount = {}

        groupNames = self.getGroupNames()

        # Do an overall count of all groupNames
        # use list.count() instead of incrementing
        # so we can skip same names as we iterate
        for name in groupNames:
            if name not in self._groupNameCount.keys():
                nameCount = groupNames.count(name)
                self._groupNameCount[name] = nameCount

        # For all names that appear more than once,
        # append a "count"
        for countedName, value in self._groupNameCount.items():
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

    def _makePresetGroupsFromXML(self):
        """
        Return list of preset groups,
        converted from proofGroups
        """
        presetList = []
        startGroup = False

        for line in self._xmlGroups:
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

    def duplicatePreset(self, duplicateName=None):
        """
        Return a deepcopy of this instance of the
        ProofPreset() object. If duplicateName is
        not given, the duplicated preset will have
        the same name as the original, with "-copy"
        appended to its name.

        The duplicated object will need to be
        captured by a variable.
        """
        duplicatePreset = copy.deepcopy(self)

        if duplicateName is None:
            duplicatePreset.name = self.preset["name"] + "-copy"
        else:
            duplicatePreset.name = duplicateName

        return duplicatePreset

    @property
    def name(self):
        """
        Return Preset name
        """
        return self.preset["name"]

    @name.setter
    def name(self, newName):
        """
        Rename preset
        """
        self.preset["name"] = newName

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

    @property
    def uniqueGroupNames(self):
        """
        Return unique group names as an attribute
        """
        return self.getGroupNames(returnCopies=False)

    def getGroupNames(self, returnCopies=True):
        """
        Return a list of all group names.
        If returnCopies=False, only return names without count
        (ie. out of group, group-1, group-2, only return group)
        """
        # Maybe a little hacky, but we already have a dict
        # of "base" group names
        if not returnCopies:
            return [groupName for groupName in self._groupNameCount]

        return [group["name"] for group in self.preset["groups"]]

    @property
    def groups(self):
        """
        Return non-verbose groups as an attribute
        """
        return self.getGroups(verbose=False)

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

    @property
    def xmlGroups(self):
        """
        Return XML-formatted groups:
        <group>
        UC
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        </group>

        <group>
        lc
        abcdefghijklmnopqrstuvwxyz
        </group>
        ...
        """
        xmlGroups = ""
        presetGroups = self.getGroups(verbose=False)
        for index, group in enumerate(presetGroups):
            xmlGroup = "<group>\n"
            xmlGroup += group["name"]
            xmlGroup += "\n"
            xmlGroup += "\n".join(group["contents"])
            xmlGroup += "\n"

            if index != len(presetGroups) - 1:
                xmlGroup += "</group>\n\n"
            else:
                xmlGroup += "</group>"

            xmlGroups += xmlGroup

        return xmlGroups

    def addGroup(self, groupToAdd, overwrite=False):
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
            newGroup["name"] = self._countNameCopies(newGroup["name"])
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
            if groupToEdit not in self.getGroupNames():
                raise ValueError("Group name doesn't exist")

            for group in self.preset["groups"]:
                if groupToEdit == group["name"]:
                    groupToEdit = group

        elif isinstance(groupToEdit, int):
            if groupToEdit > len(self.preset["groups"]) - 1:
                raise IndexError("Index out of range")

            groupToEdit = self.preset["groups"][groupToEdit]

        for key, value in kwargs.items():
            if key not in self._keysInGroup:
                continue
            elif key == "name" and value in self.getGroupNames():
                raise ValueError("Name already exists")
            elif key == "typeSize" and not isinstance(value, float):
                raise ValueError("Type size should be a float")
            elif key == "leading" and not isinstance(value, float):
                raise ValueError("Type size should be a float")
            elif key == "print" and not isinstance(value, bool):
                raise TypeError("Group print setting has to be a boolean")
            elif key == "contents" and not isinstance(value, list):
                raise TypeError("Group contents has to be a list")

            groupToEdit[key] = value

    def importFromJSON(self, jsonInput, overwrite=False):
        """
        Import JSON object and convert to a ProofPreset() object.
        jsonInput can be a filePath or a JSON object.

        The overwrite behaviour is the same as ProofPreset.importPyDict()
        """
        jsonObj = None
        if isinstance(jsonInput, str):
            if not os.path.isfile(jsonInput):
                jsonObj = jsonInput

            else:
                ext = os.path.splitext(jsonInput)[1].lower()
                if ext == ".json":
                    with open(jsonInput, "r") as jsonFile:
                        jsonObj = jsonFile.read()

        if not jsonObj:
            raise ProofPresetError("Invalid JSON input")

        presetFromJSON = json.loads(jsonObj)
        self.importPyDict(presetFromJSON, overwrite)

    def importPyDict(self, pyDictInput, overwrite=False):
        """
        Import a WHOLE ProofPreset (py dict).
        To import from JSON, use ProofPreset.importFromJSON()

        pyDictInput is a dictionary. Whenever a group
        in pyDictInput is missing a setting, it's added
        with empty values.

        If overwrite is False, raise an error when there's
        already a stored preset["groups"].
        """
        if not overwrite and self.preset["groups"]:
            raise ProofPresetError("There's already a preset in here.")

        # Validate imported preset
        if not pyDictInput["name"]:
            raise ProofPresetError("Imported preset has no name")
        elif not pyDictInput["groups"]:
            raise ProofPresetError("Imported preset has no groups")

        # Copy so we're not changing imported object later
        dictPreset = copy.deepcopy(pyDictInput)

        # Remove unneeded keys & add missing keys
        # Maybe should clean contents?
        for group in dictPreset["groups"]:
            group = self._removeUnneededKeysInGroup(group)
            group = self._addMissingKeysToGroup(group)

        # Import preset & fix groupNames
        self.preset = dictPreset
        self._inspectAndFixGroupNames(restartCount=True)

    def importFromXML(self, xmlTaggedInput):
        """
        Import XML-tagged proof and convert to ProofPreset() object.
        xmlTaggedInput can be a filePath, a string, or a list.

        File extensions can be .xml or .txt.
        Recognized XML tags are <group> </group>

        If xmlTaggedInput is a string:
        "<group>\nUC\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n</group>"

        if xmlTaggedInput is a list:
        ["<group>", "UC", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "</group>"]

        This method performs some basic cleaning & validation,
        including ingnoring everything before first <group> tag
        and everything after last </group> tag.
        """
        xmlObj = None
        if isinstance(xmlTaggedInput, str):
            if not os.path.isfile(xmlTaggedInput):
                xmlObj = xmlTaggedInput.split("\n")

            else:
                ext = os.path.splitext(xmlTaggedInput)[1].lower()
                if ext in (".xml", ".txt"):
                    with open(xmlTaggedInput, "r") as xmlFile:
                        xmlObj = xmlFile.readlines()

        elif isinstance(xmlTaggedInput, list):
            xmlObj = copy.deepcopy(xmlTaggedInput)

        if not xmlObj:
            raise ProofPresetError("Invalid XML input")

        self._xmlGroups = utils.cleanList(xmlObj,
                                          discardBefore="<group>",
                                          discardAfter="</group>")

        if not self._xmlGroups:
            raise ProofPresetError("Imported XML object is empty")

        utils.checkForTags(self._xmlGroups, "group")
        utils.checkXMLtagsSequence(self._xmlGroups, "group")

        # Main import & fix groupNames
        self.preset["groups"] = self._makePresetGroupsFromXML()
        self._inspectAndFixGroupNames()

    def exportToJSON(self, filePath):
        """
        Export preset to JSON file.

        filePath will be created if it doesn't exist,
        but must have an extension of .json

        This method is a helper built on top of
        ProofPreset.getPreset(jsonFormat=True)
        """
        ext = os.path.splitext(filePath)[1].lower()
        if ext != ".json":
            raise ProofPresetError("File not .json")

        with open(filePath, "w+") as jsonFile:
            jsonFile.write(self.getPreset(jsonFormat=True))

    def exportToXML(self, filePath):
        """
        Export groups to XML file.

        filePath will be created if it doesn't exist,
        but must have an extension of .xml or .txt

        This method is a helper built on top of
        ProofPreset.getXMLGroups()
        """
        ext = os.path.splitext(filePath)[1].lower()
        if ext not in (".xml", ".txt"):
            raise ProofPresetError("File not .xml or .txt")

        with open(filePath, "w+") as xmlFile:
            xmlFile.write(self.xmlGroups)


if __name__ == "__main__":
    fileDir = os.path.dirname(__file__)
    testFileDir = os.path.join(fileDir, "tests", "resources", "proofDocTest.txt")

    with open(testFileDir, "r") as testFile:
        readList = testFile.readlines()

    # Simple testing:
    preset = ProofPreset("myPreset")
    preset.importFromXML(readList)
    print(preset.getPreset())
