import helperFuncs as hf
from vanilla import Window, TextBox, PopUpButton, Button, List, CheckBoxListCell
import os.path

# If imported proof group is a py list in a module:
# from proofList import proofList
# (but has to live in the same folder, otherwise it's too messy (ie. deal w/ packages))

currentFilePath = os.path.dirname(__file__)
jsonFilePath = os.path.join(currentFilePath, "..", "resources", "proofList.json")

class ProofDrawer:
    def __init__(self, proofListFilePath):
        self.fonts = ["Font 1", "Font 2"]

        # These lists should be imported from json preset file
        self.proofGroupsList = hf.readJSONpresets(proofListFilePath)
        self.additionalGroupsList = hf.getValuesFromListOfDicts(self.proofGroupsList, "Group")

        self.w = Window((400, 600), "Proof Drawer")

        self.w.fontText = TextBox((10, 10, 80, 20), "Select font:")
        self.w.fontButton = PopUpButton((100, 10, -10, 20),
                                        items=self.fonts,
                                        callback=self.fontButtonCB)

        self.w.proofGroups = List((10, 50, -10, 250),
                                  rowHeight=18,
                                  items=self.proofGroupsList,
                                  columnDescriptions=[
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
                                          "title": "Print?",
                                          "cell": CheckBoxListCell()
                                      }
                                  ],
                                  allowsMultipleSelection=False,
                                  selectionCallback=self.checkCheck)

        self.w.proofGroupText = TextBox((10, 325, -10, 20), "Add more proof groups:")
        self.w.additionalGroups = List((10, 350, -10, 200),
                                       rowHeight=17,
                                       items=self.additionalGroupsList,
                                       allowsMultipleSelection=False)

        self.w.addProofGroup = Button((10, 560, -10, 20),
                                      "Add to proof list",
                                      callback=self.addProofGroupCB)

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
                "Group": self.additionalGroupsList[index],
                "Type size": "",
                "Leading": "",
                "Print?": 0
            }
            self.proofGroupsList.append(proofRow)

        self.w.proofGroups.set(self.proofGroupsList)

    def testerCB(self, sender):
        """
        Use this for fake CB
        """
        pass

if __name__ == "__main__":
    proofDrawer = ProofDrawer(jsonFilePath)
    proofDrawer.w.open()
