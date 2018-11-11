from utils.readWritePreset import readJSONpreset, writeJSONpreset
from utils import helperFunctions as hf
from utils.proofPreset import ProofPreset
from proofGroupInspector import ProofGroupInspector

from mojo.events import addObserver, removeObserver
from vanilla import Window, TextBox, PopUpButton, ImageButton, Button,\
                    List, CheckBoxListCell, HorizontalLine
import os.path

class ProofDrawer:
    def __init__(self, proofGroupsList):
        self.fonts = ["Font 1", "Font 2"]
        self.presets = ["Preset 1", "Preset 2"]

        self.proofGroupInspector = None
        self.editedGroupIndex = None
        self.inspectorOpen = False

        # These lists should be imported from json preset file
        # proofGroupsList = readJSONpreset(proofListFilePath)
        # or the extension looks at the resources folder for presets
        
        # Testing importing list
        self.additionalGroupsList = hf.getValuesFromListOfDicts(proofGroupsList, "group")
        self.listHasBeenEdited = False # A flag for later... see closeWindowCB()

        self._buildUI(proofGroupsList)

        addObserver(self, "_trackInspectorWindow", "comInspectorClosed")
        addObserver(self, "_updateProofGroup", "comProofGroupEdited")
        self.w.bind("close", self.closeWindowCB)

    def _buildUI(self, proofGroupsList):
        editPresetsImgPath = os.path.join(currentFilePath,\
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
                "key": "group",
                "width": 160,
                "editable": True
            },
            {
                "title": "Type size",
                "width": 70,
                "editable": True
            },
            {
                "title": "Leading",
                "width": 65,
                "editable": True
            },
            {
                "title": " 🖨",
                "key": "print",
                "cell": CheckBoxListCell()
            }
        ]

        # Auto-add key so proof drawer can match w/ preset
        for item in listForList:
            if "key" not in item.keys():
                item["key"] = item["title"].lower()

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
                                         items=self.presets,
                                         callback=self.testerCB)

        self.w.editPresets = ImageButton((width - 38, row, 22, 22),
                                         imagePath=editPresetsImgPath,
                                         bordered=False,
                                         callback=self.testerCB)


        row += 35
        self.w.line1 = HorizontalLine((left, row, -10, 1))

        row += 15
        self.w.proofGroups = List((left, row, listWidth, 255),
                                  rowHeight=18,
                                  items=proofGroupsList,
                                  columnDescriptions=listForList,
                                  allowsMultipleSelection=False,
                                  enableDelete=True)

        buttonGroup1Left = popUpLeft + presetsPopUpWidth + 3
        buttonGroup1Top = row + 58
        self.w.inspectGroup = Button((buttonGroup1Left, buttonGroup1Top, 30, 20),
                                "\u24D8",
                                callback=self.inspectGroupCB)

        buttonGroup1Top += 40
        self.w.moveGroupUP = Button((buttonGroup1Left , buttonGroup1Top, 30, 20),
                                    "↑",
                                    callback=self.moveGroupCB)
        buttonGroup1Top += 25
        self.w.moveGroupDN = Button((buttonGroup1Left, buttonGroup1Top, 30, 20),
                                    "↓",
                                    callback=self.moveGroupCB)

        buttonGroup1Top += 40
        self.w.removeGroup = Button((buttonGroup1Left, buttonGroup1Top, 30, 20),
                                    "-",
                                    callback=self.removeGroup)
        

        row += 275
        self.w.line2 = HorizontalLine((left, row, -10, 1))

        row += 10
        self.w.additionalGroupsText = TextBox((left, row, -10, 20),
                                              "Add more proof groups:")

        row += 25
        self.w.additionalGroups = List((left, row, listWidth, 150),
                                       rowHeight=17,
                                       items=self.additionalGroupsList,
                                       allowsMultipleSelection=False)

        self.w.addGroup = Button((buttonGroup1Left, row + 60, 30, 20),
                            "+",
                            callback=self.addProofGroupCB)

        # row += 25
        # self.w.previewButton = Button((additionalWidth + 20, row, -10, 20),
        #                               "Preview",
        #                               callback=self.testerCB)
        
        # row += 25
        # self.w.printButton = Button((additionalWidth + 20, row, -10, 20),
        #                              "Print",
        #                              callback=self.testerCB)

    def _trackInspectorWindow(self, info):
        """
        Prevent more than one inspector window
        from being opened.
        """
        self.inspectorOpen = False
    
    def _updateProofGroup(self, info):
        """
        Update the proof groups list to reflect
        edits made in the inspector.

        The comProofGroupEdited event also returns
        the newly-edited proof group.
        """
        self.w.proofGroups[self.editedGroupIndex] = info["newProofGroup"]

    def _refreshOrder(self):
        """
        Simple method to refresh the order number.
        Private because user doesn't directly interact with it.
        """
        newOrder = 1
        for item in self.w.proofGroups:
            item["order"] = newOrder
            newOrder += 1

    def fontButtonCB(self, sender):
        # pass
        selectedFont = self.fonts[sender.get()]
        self.w.setTitle("Proof Drawer: %s" % selectedFont)

    def inspectGroupCB(self, sender):
        """
        Open new window that lets user inspect and further edit
        selected group.
        """
        if self.inspectorOpen or not self.w.proofGroups.getSelection():
            return

        self.editedGroupIndex = self.w.proofGroups.getSelection()[0]
        selectedGroup = self.w.proofGroups[self.editedGroupIndex]

        self.proofGroupInspector = ProofGroupInspector(selectedGroup)
        self.proofGroupInspector.w.open()
        self.inspectorOpen = True

    def moveGroupCB(self, sender):
        """
        Both up and down buttons call this method because
        they share the same sorting logic.

        The sorting works by holding the selected object
        in a temp variable, deleting from the groups list,
        and then re-inserting in the index before or after.
        """
        direction = sender.getTitle()
        selectionIndex = self.w.proofGroups.getSelection()[0]

        selectionObj = self.w.proofGroups[selectionIndex]
        if direction == "↑":
            # First object can't move up
            if selectionIndex == 0:
                return
            newIndex = selectionIndex - 1
        else:
            # Last object can't move down
            if selectionIndex == len(self.w.proofGroups) - 1:
                return
            newIndex = selectionIndex + 1
        
        del self.w.proofGroups[selectionIndex]
        self.w.proofGroups.insert(newIndex, selectionObj)
        self.w.proofGroups.setSelection([newIndex])
        self._refreshOrder()

    def removeGroup(self, sender):
        """
        Delete selected and refresh order number
        """
        selectionIndex = self.w.proofGroups.getSelection()[0]
        del self.w.proofGroups[selectionIndex]
        self._refreshOrder()

    def addProofGroupCB(self, sender):
        """
        Append selected additional group to main list and
        add some information along the way.
        """
        selectionIndices = self.w.additionalGroups.getSelection()

        for index in selectionIndices:
            proofRow = {
                "group": self.additionalGroupsList[index],
                "order": len(self.w.proofGroups) + 1,
                "type size": "",
                "leading": "",
                "print": False
            }
            self.w.proofGroups.append(proofRow)

    def closeWindowCB(self, sender):
        """
        On close, save the state of the current preset.
        """
        listToWrite = hf.convertToListOfPyDicts(self.w.proofGroups)

        newPresetPath = os.path.join(currentFilePath, "..", "resources", "newPreset.json")
        # turn this back on later
        # writeJSONpreset(newPresetPath, listToWrite)

        removeObserver(self, "comInspectorClosed")
        removeObserver(self, "comProofGroupEdited")

    def testerCB(self, sender):
        """
        Use this for fake CB
        """
        print("hit: ", sender)

if __name__ == "__main__":
    # This is just for testing. ProofDrawer() shouldn't import proof document
    # at init, and should import a json preset instead
    currentFilePath = os.path.dirname(__file__)
    proofFilePath = os.path.join(currentFilePath, "..", "resources", "proofFile.txt")
    # jsonFilePath = os.path.join(currentFilePath, "..", "resources", "proofPreset.json")

    with open(proofFilePath, "r") as proofFile:
        proofList = proofFile.readlines()

    preset = ProofPreset(proofList, "group")
    proofDrawer = ProofDrawer(preset.getPreset())
    proofDrawer.w.open()
