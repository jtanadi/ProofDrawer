from utils.readWritePreset import readJSONpreset, writeJSONpreset
from utils.proofPreset import ProofPreset
from utils import helperFunctions as hf
from vanilla import Window, TextBox, PopUpButton, Button,\
                    List, CheckBoxListCell, ImageButton, HorizontalLine
import os.path

class ProofDrawer:
    def __init__(self, proofGroupsList):
        self.fonts = ["Font 1", "Font 2"]
        self.presets = ["Preset 1", "Preset 2"]
        editPresetsImgPath = os.path.join(currentFilePath,\
                                          "..", "resources",\
                                          "editPresetsIcon.pdf")

        # These lists should be imported from json preset file
        # self.proofGroupsList = readJSONpreset(proofListFilePath)
        
        # Testing importing list
        self.proofGroupsList = proofGroupsList
        self.additionalGroupsList = hf.getValuesFromListOfDicts(self.proofGroupsList, "group")
        self.listHasBeenEdited = False # A flag for later... see closeWindowCB()

        listForList = [
            {
                "title": "#",
                "key": "order",
                "width": 20,
                "editable": False,
            },
            {
                "title": "Group",
                "width": 160,
                "editable": False
            },
            {
                "title": "Type size",
                "editable": True,
                "width": 70
            },
            {
                "title": "Leading",
                "editable": True,
                "width": 65
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
        textWidth = 60
        textHeight = 20
        popUpLeft = left + textWidth
        presetsPopUpWidth = width - popUpLeft - 44
        listWidth = textWidth + presetsPopUpWidth - 5

        self.w = Window((width, 600), "Proof Drawer")

        self.w.fontText = TextBox((left, row, textWidth, textHeight),
                                  "Font:")
        self.w.fontsList = PopUpButton((popUpLeft, row, -10, textHeight),
                                       items=self.fonts,
                                       callback=self.fontButtonCB)

        row += 30
        self.w.presetText = TextBox((left, row, textWidth, textHeight),
                                    "Preset:")

        
        self.w.presetsList = PopUpButton((popUpLeft, row, presetsPopUpWidth, textHeight),
                                         items=self.presets,
                                         callback=self.testerCB)

        self.w.editPresets = ImageButton((width - 37, row, 22, 22),
                                         imagePath=editPresetsImgPath,
                                         bordered=False,
                                         callback=self.testerCB)


        row += 35
        self.w.line1 = HorizontalLine((left, row, -10, 1))

        row += 15
        self.w.proofGroups = List((left, row, listWidth, 255),
                                  rowHeight=18,
                                  items=self.proofGroupsList,
                                  columnDescriptions=listForList,
                                  allowsMultipleSelection=False,
                                  editCallback=self.checkCheck,
                                  enableDelete=True)

        buttonGroup1Left = popUpLeft + presetsPopUpWidth + 5
        buttonGroup1Top = row + 58
        self.w.inspectGroup = Button((buttonGroup1Left, buttonGroup1Top, 30, 20),
                                "\u24D8",
                                callback=self.testerCB)

        buttonGroup1Top += 40
        self.w.moveGroupUP = Button((buttonGroup1Left , buttonGroup1Top, 30, 20),
                                    "↑",
                                    callback=self.testerCB)
        buttonGroup1Top += 25
        self.w.moveGroupDN = Button((buttonGroup1Left, buttonGroup1Top, 30, 20),
                                    "↓",
                                    callback=self.testerCB)

        buttonGroup1Top += 40
        self.w.removeGroup = Button((buttonGroup1Left, buttonGroup1Top, 30, 20),
                                    "-",
                                    callback=self.testerCB)
        

        row += 275
        self.w.line2 = HorizontalLine((left, row, -10, 1))

        row += 10
        self.w.proofGroupText = TextBox((left, row, -10, 20),
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

        self.w.bind("close", self.closeWindowCB)

    def closeWindowCB(self, sender):
        # If list was edited, then each dict becomes __NSDictionaryM
        # so each __NSDictionaryM has to be converted to py dict.
        if not self.listHasBeenEdited:
            listToWrite = self.proofGroupsList
        else:
            listToWrite = []
            for dictItem in self.proofGroupsList:
                tempDict = {}
                for key in dictItem:
                    tempDict[key] = dictItem[key]
                
                listToWrite.append(tempDict)
            
        newPresetPath = os.path.join(currentFilePath, "..", "resources", "newPreset.json")
        writeJSONpreset(newPresetPath, listToWrite)

    def fontButtonCB(self, sender):
        # pass
        selectedFont = self.fonts[sender.get()]
        self.w.setTitle("Proof Drawer: %s" % selectedFont)

    def deselectListItem(self, sender):
        # Prevents selection by setting selection of sender object to empty list
        sender.setSelection([])

    def checkCheck(self, sender):
        # Refreshes list so it remembers user input (sizes & print)
        self.proofGroupsList = sender.get()
        self.listHasBeenEdited = True

    def addProofGroupCB(self, sender):
        # We capture the index of what was selected
        # and add the item to our proofGroupsList
        selectionIndex = self.w.additionalGroups.getSelection()

        for index in selectionIndex:
            proofRow = {
                "group": self.additionalGroupsList[index],
                "order": len(self.w.proofGroups) + 1,
                "type size": "",
                "leading": "",
                "print": False
            }
            self.proofGroupsList.append(proofRow)

        self.w.proofGroups.set(self.proofGroupsList)

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
