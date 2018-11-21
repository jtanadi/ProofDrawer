"""
Main window of Proof Drawer
"""

import os
from mojo.events import addObserver, removeObserver
from vanilla import Window, TextBox, PopUpButton, ImageButton, Button,\
                    List, CheckBoxListCell, HorizontalLine

from utils.readWritePreset import readJSONpreset, writeJSONpreset
from utils import helperFunctions as hf
from proofPreset import ProofPreset
from windows.proofGroupInspector import ProofGroupInspector

class ProofDrawer:
    def __init__(self, presetsList):
        self.fonts = ["Font 1", "Font 2"]
        self.presetsList = presetsList

        self.currentPreset = self.presetsList[0]
        self.presetNamesList = self._getPresetNames()

        # These 3 might be up for deletion
        self.proofGroupInspector = None
        self.editedGroupIndex = None
        self.listHasBeenEdited = False # A flag for later... see closeWindowCB()

        self._buildUI()
        self._refreshProofGroups()

        addObserver(self, "_inspectorClosed", "com.InspectorClosed")
        addObserver(self, "editProofGroupCB", "com.ProofGroupEdited")
        self.w.bind("close", self.closeWindowCB)

    def _buildUI(self):
        editPresetsImgPath = os.path.join(currentFileDir,\
                                          "..", "resources",\
                                          "editPresetsIcon.pdf")

        listForList = [
            {
                "title": "#",
                "key": "order",
                "width": 20,
                "editable": False
            },
            {
                "title": "Group name",
                "key": "name",
                "width": 160,
                "editable": True
            },
            {
                "title": "Type size",
                "key": "typeSize",
                "width": 70,
                "editable": True,
            },
            {
                "title": "Leading",
                "key": "leading",
                "width": 65,
                "editable": True
            },
            {
                "title": " 🖨",
                "key": "print",
                "cell": CheckBoxListCell()
            }
        ]

        width = 425
        left = 10
        row = 10
        textWidth = 48
        textHeight = 20
        popUpLeft = left + textWidth + 5
        presetsPopUpWidth = width - popUpLeft - 47
        listWidth = textWidth + presetsPopUpWidth

        self.w = Window((width, 600), "Proof Drawer")

        self.w.fontText = TextBox((left, row, textWidth, textHeight),
                                  "Font:",
                                  alignment="right")
        self.w.fontsList = PopUpButton((popUpLeft, row, -10, textHeight),
                                       items=self.fonts,
                                       callback=self.fontButtonCB)

        row += 30
        self.w.presetText = TextBox((left, row, textWidth, textHeight),
                                    "Preset:",
                                    alignment="right")

        self.w.presetsList = PopUpButton((popUpLeft, row, presetsPopUpWidth, textHeight),
                                         items=self.presetNamesList,
                                         callback=self.setCurrentPresetCB)

        self.w.editPresets = ImageButton((width - 38, row, 22, 22),
                                         imagePath=editPresetsImgPath,
                                         bordered=False,
                                         callback=self.testerCB)

        row += 35
        self.w.line1 = HorizontalLine((left, row, -10, 1))

        row += 15
        self.w.proofGroups = List((left + 3, row, listWidth, 255),
                                  rowHeight=18,
                                  items=[],
                                  columnDescriptions=listForList,
                                  allowsSorting=False,
                                  allowsMultipleSelection=False,
                                  editCallback=self.editProofGroupCB)

        buttonGroup1Left = popUpLeft + presetsPopUpWidth + 3
        buttonGroup1Top = row + 58
        self.w.inspectGroup = Button((buttonGroup1Left, buttonGroup1Top, 30, 20),
                                "\u24D8",
                                callback=self.inspectGroupCB)

        buttonGroup1Top += 40
        self.w.moveGroupUP = Button((buttonGroup1Left, buttonGroup1Top, 30, 20),
                                    "↑",
                                    callback=self.moveGroupCB)
        buttonGroup1Top += 25
        self.w.moveGroupDN = Button((buttonGroup1Left, buttonGroup1Top, 30, 20),
                                    "↓",
                                    callback=self.moveGroupCB)

        buttonGroup1Top += 40
        self.w.removeGroup = Button((buttonGroup1Left, buttonGroup1Top, 30, 20),
                                    "-",
                                    callback=self.removeGroupCB)

        row += 275
        self.w.line2 = HorizontalLine((left, row, -10, 1))

        row += 10
        self.w.additionalGroupNamesText = TextBox((left, row, -10, 20),
                                              "Add more proof groups:")

        row += 25
        self.w.additionalGroupNames = List((left + 3, row, listWidth, 150),
                                           rowHeight=17,
                                           items=self.currentPreset.getGroupNames(returnCopies=False),
                                           allowsSorting=False,
                                           allowsMultipleSelection=True)

        self.w.addGroup = Button((buttonGroup1Left, row + 60, 30, 20),
                                 "+",
                                 callback=self.addProofGroupsCB)

        # row += 25
        # self.w.previewButton = Button((additionalWidth + 20, row, -10, 20),
        #                               "Preview",
        #                               callback=self.testerCB)
        
        # row += 25
        # self.w.printButton = Button((additionalWidth + 20, row, -10, 20),
        #                              "Print",
        #                              callback=self.testerCB)

    def _getPresetNames(self):
        """
        Get preset names for display
        """
        return [preset.getPresetName() for preset in self.presetsList]

    def _uiEnabled(self, onOff=True):
        """
        A master switch for all editable UI elements
        """
        self.w.proofGroups.enable(onOff)
        self.w.fontsList.enable(onOff)
        self.w.presetsList.enable(onOff)
        self.w.editPresets.enable(onOff)
        self.w.editPresets.enable(onOff)
        self.w.inspectGroup.enable(onOff)
        self.w.moveGroupUP.enable(onOff)
        self.w.moveGroupDN.enable(onOff)
        self.w.removeGroup.enable(onOff)
        self.w.additionalGroupNames.enable(onOff)
        self.w.addGroup.enable(onOff)

    def _inspectorClosed(self, info):
        """
        Prevent more than one inspector window
        from being opened.
        """
        self._uiEnabled(True)

    def _refreshProofGroups(self, newSelection=0):
        """
        Refresh the proof groups list, set order numbers,
        and set selection.

        newSelection defaults to first index in list.
        """
        # Set flag so editProofGroupCB() isn't
        # called when set proofGroups contents &
        # set order numbers
        self._proofReadyToEdit = False

        self.w.proofGroups.set(self.currentPreset.getGroups())

        newOrder = 1
        for item in self.w.proofGroups:
            item["order"] = newOrder
            newOrder += 1

        self._proofReadyToEdit = True
        self.w.proofGroups.setSelection([newSelection])

    def fontButtonCB(self, sender):
        selectedFont = self.fonts[sender.get()]
        self.w.setTitle("Proof Drawer: %s" % selectedFont)

    def setCurrentPresetCB(self, sender):
        selectedPresetIndex = sender.get()
        self.currentPreset = self.presetsList[selectedPresetIndex]
        self._refreshProofGroups()
        self.w.additionalGroupNames.set(self.currentPreset.getGroupNames(returnCopies=False))

    def inspectGroupCB(self, sender):
        """
        Open new window that lets user inspect and further edit
        selected group.
        """
        if not self.w.proofGroups.getSelection():
            return

        editGroupIndex = self.w.proofGroups.getSelection()[0]
        selectedGroup = self.currentPreset.getGroups()[editGroupIndex]
        # self.editedGroupIndex = self.w.proofGroups.getSelection()[0]
        # selectedGroup = self.w.proofGroups[self.editedGroupIndex]

        self.proofGroupInspector = ProofGroupInspector(selectedGroup)
        self.proofGroupInspector.w.open()
        self.proofGroupInspector.w.center()
        self.proofGroupInspector.w.makeKey()
        self._uiEnabled(False)

    def editProofGroupCB(self, senderOrInfo):
        """
        Edit selected proof group and refresh proof groups list.
        senderOrInfo accepts callback sender or info from PostEvent

        ProofPreset.editGroup() is called on a field-by-field basis
        so we're not trying to edit "name" when only editing "leading"
        """
        # Don't do anything if proof groups aren't
        # ready to be edited or if nothing is selected
        if not self._proofReadyToEdit or\
        not self.w.proofGroups.getSelection():
            return

        selectedIndex = self.w.proofGroups.getSelection()[0]

        # Capture current values for checking later
        currentGroup = self.currentPreset.getGroups()[selectedIndex]
        # currentName = currentGroup["name"]
        # currentPrint = currentGroup["print"]
        # currentSize = currentGroup["typeSize"]
        # currentLeading = currentGroup["leading"]
        # currentContents = currentGroup["contents"]

        # iterate instead
        for key in currentGroup:
            currentValue = currentGroup[key]

            if isinstance(senderOrInfo, dict) and senderOrInfo["editedProofGroup"]:
                newValue = senderOrInfo["editedProofGroup"][key]
            else:
                print('hey')
                newValue = self.w.proofGroups[selectedIndex][key]

                if key == "typeSize" or key == "leading":
                    try:
                        newValue = float(newValue)
                    except ValueError:
                        newValue = currentValue

            if newValue != currentValue:
                self.currentPreset.editGroup(selectedIndex, key=newValue)


        # # Print isn't edited in inspector
        # # Contents aren't edited in main window
        # newPrint = None
        # newContents = None

        # if senderOrInfo["editedProofGroup"]:
        #     editedGroup = senderOrInfo["editedProofGroup"]
        #     newName = editedGroup["name"]
        #     newSize = editedGroup["typeSize"]
        #     newLeading = editedGroup["leading"]
        #     newContents = editedGroup["contents"]

        # else:
        #     newName = self.w.proofGroups[selectedIndex]["name"]
        #     newPrint = self.w.proofGroups[selectedIndex]["print"]

        #     # ProofPreset.editGroup() will only accept floats for
        #     # typeSize and leading
        #     try:
        #         newSize = float(self.w.proofGroups[selectedIndex]["typeSize"])
        #     except ValueError:
        #         newSize = currentSize
        #     try:
        #         newLeading = float(self.w.proofGroups[selectedIndex]["leading"])
        #     except ValueError:
        #         newLeading = currentLeading

        # # "Target" editGroup() more precisely, so we're not constantly
        # # calling editGroup() on all the other values if we've only edited one
        # # For ex. if calling editGroup() on everything, when only editing leading,
        # # we'll get a ValueError("Name already exists") because it'll try to
        # # update current group name with the same "new" name
        # if newName != currentName:
        #     self.currentPreset.editGroup(selectedIndex, name=newName)
        # if newPrint is not None and newPrint != currentPrint:
        #     self.currentPreset.editGroup(selectedIndex, print=newPrint)
        # if newSize != currentSize:
        #     self.currentPreset.editGroup(selectedIndex, typeSize=newSize)
        # if newLeading != currentLeading:
        #     self.currentPreset.editGroup(selectedIndex, leading=newLeading)
        # if newContents is not None and newContents != currentContents:
        #     self.currentPreset.editGroup(selectedIndex, contents=newContents)

        self._refreshProofGroups(selectedIndex)

    def moveGroupCB(self, sender):
        """
        Move selected group and refresh proof groups list.

        Both up and down buttons call this method because they
        both call ProofPreset.moveGroup(currentIndex, new Index)
        """
        if not self.w.proofGroups or not self.w.proofGroups.getSelection():
            return

        direction = sender.getTitle()
        currentIndex = self.w.proofGroups.getSelection()[0]

        if direction == "↑":
            # First object can't move up
            if currentIndex == 0:
                return
            newIndex = currentIndex - 1
        else:
            # Last object can't move down
            if currentIndex == len(self.w.proofGroups) - 1:
                return
            newIndex = currentIndex + 1

        self.currentPreset.moveGroup(currentIndex, newIndex)
        self._refreshProofGroups(newSelection=newIndex)

    def removeGroupCB(self, sender):
        """
        Delete selected group and refresh proof groups list
        """
        if not self.w.proofGroups or not self.w.proofGroups.getSelection():
            return
        groupToDeleteIndex = self.w.proofGroups.getSelection()[0]

        self.currentPreset.removeGroup(groupToDeleteIndex)
        self._refreshProofGroups(newSelection=groupToDeleteIndex) # This will select next group

    def addProofGroupsCB(self, sender):
        """
        Add new groups from additionalGroupNames list
        """
        newGroupNamesIndices = self.w.additionalGroupNames.getSelection()
        if not newGroupNamesIndices:
            return

        for index in newGroupNamesIndices:
            groupToAdd = {"name": self.w.additionalGroupNames[index]}
            self.currentPreset.addGroup(groupToAdd)

        self._refreshProofGroups()

    def closeWindowCB(self, sender):
        """
        On close, save the state of the current preset.
        """
        # if self.proofGroupInspector:
        #     self.proofGroupInspector.w.close()

        # listToWrite = hf.convertToListOfPyDicts(self.w.proofGroups)

        # newPresetPath = os.path.join(currentFilePath, "..", "resources",\
        #                              "presets", "newTestPreset.json")
        # writeJSONpreset(newPresetPath, listToWrite)

        removeObserver(self, "com.InspectorClosed")
        removeObserver(self, "com.ProofGroupEdited")

    def testerCB(self, sender):
        """
        Use this for fake CB
        """
        print("hit: ", sender)


if __name__ == "__main__":
    currentFileDir = os.path.dirname(__file__)
    presetsDir = os.path.join(currentFileDir, "..", "resources", "presets")

    presetsToUse = []
    for fileName in os.listdir(presetsDir):
        ext = os.path.splitext(fileName)[1]
        if ext == ".json":
            jsonPath = os.path.join(presetsDir, fileName)
            newPreset = ProofPreset()
            newPreset.importFromJSON(jsonPath)
            presetsToUse.append(newPreset)

    proofDrawer = ProofDrawer(presetsToUse)
    proofDrawer.w.open()
    proofDrawer.w.center()
