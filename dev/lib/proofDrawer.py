from utils.readWritePreset import readJSONpreset, writeJSONpreset
from utils.proofPreset import ProofPreset
from utils import helperFunctions as hf
from vanilla import Window, TextBox, PopUpButton, Button, List, CheckBoxListCell
import os.path

class ProofDrawer:
    def __init__(self, proofGroupsList):
        self.fonts = ["Font 1", "Font 2"]

        # These lists should be imported from json preset file
        # self.proofGroupsList = readJSONpreset(proofListFilePath)
        
        # Testing importing list
        self.proofGroupsList = proofGroupsList

        self.additionalGroupsList = hf.getValuesFromListOfDicts(self.proofGroupsList, "group")

        listForList = [
            {
                "title": "Group",
                "width": 175
            },
            {
                "title": "Type size",
                "editable": True,
                "width": 65
            },
            {
                "title": "Leading",
                "editable": True,
                "width": 65
            },
            {
                "title": "Print",
                "cell": CheckBoxListCell()
            }
        ]

        # Auto-add key so proof drawer can match w/ preset
        for item in listForList:
            item["key"] = item["title"].lower()

        self.w = Window((400, 600), "Proof Drawer")

        self.w.fontText = TextBox((10, 10, 80, 20), "Select font:")
        self.w.fontButton = PopUpButton((100, 10, -10, 20),
                                        items=self.fonts,
                                        callback=self.fontButtonCB)

        self.w.proofGroups = List((10, 50, -10, 250),
                                  rowHeight=18,
                                  items=self.proofGroupsList,
                                  columnDescriptions=listForList,
                                  allowsMultipleSelection=False,
                                  editCallback=self.checkCheck)

        self.w.proofGroupText = TextBox((10, 325, -10, 20), "Add more proof groups:")
        self.w.additionalGroups = List((10, 350, -10, 200),
                                       rowHeight=17,
                                       items=self.additionalGroupsList,
                                       allowsMultipleSelection=False)

        self.w.addProofGroup = Button((10, 560, -10, 20),
                                      "Add to proof list",
                                      callback=self.addProofGroupCB)

        self.w.bind("close", self.closeWindowCB)

    def closeWindowCB(self, sender):
        # Have to convert from list of __NSDictionaryM to list of py dicts
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

    def addProofGroupCB(self, sender):
        # We capture the index of what was selected
        # and add the item to our proofGroupsList
        selectionIndex = self.w.additionalGroups.getSelection()

        for index in selectionIndex:
            proofRow = {
                "group": self.additionalGroupsList[index],
                "type size": "",
                "leading": "",
                "print": True
            }
            self.proofGroupsList.append(proofRow)

        self.w.proofGroups.set(self.proofGroupsList)

    def testerCB(self, sender):
        """
        Use this for fake CB
        """
        pass

if __name__ == "__main__":
    currentFilePath = os.path.dirname(__file__)
    proofFilePath = os.path.join(currentFilePath, "..", "resources", "proofFile.txt")
    # jsonFilePath = os.path.join(currentFilePath, "..", "resources", "proofPreset.json")

    proofFile = open(proofFilePath, "r")
    proofList = proofFile.readlines()
    proofFile.close()

    preset = ProofPreset(proofList, "group")
    proofDrawer = ProofDrawer(preset.getPreset())
    proofDrawer.w.open()
