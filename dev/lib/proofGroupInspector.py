from vanilla import Window, TextBox, EditText,\
                    ComboBox, TextEditor, Button
from mojo.events import postEvent

class ProofGroupInspector:
    def __init__(self, proofGroup):
        """
        Initialize inspector with empty fields.
        Fields will be populated when
        ProofGroupInspector.setProofGroup() is called.
        """
        self.proofGroup = proofGroup
        self.newProofGroup = {}

        left = 10
        row = 10
        textboxWidth = 92
        leftEditText = left + 95
        pointSizes = ["6", "8", "10", "12", "14", "18",\
                      "21", "24", "36", "48", "60", "72"]

        self.w = Window((400, 275),
                        "Edit Proof Group: %s" % self.proofGroup["group"])

        self.w.groupName = TextBox((left, row + 2, textboxWidth, 20),
                                   "Group name:",
                                   alignment="right")

        self.w.groupNameEdit = EditText((leftEditText, row, -10, 22),
                                        self.proofGroup["group"])

        row += 33
        self.w.typeSize = TextBox((left, row + 2, textboxWidth, 20),
                                  "Type size (pt):",
                                  alignment="right")

        self.w.typeSizeEdit = ComboBox((leftEditText, row, 55, 22),
                                       pointSizes,
                                       continuous=True,
                                       callback=self._checkFloat)

        self.w.typeSizeEdit.set(self.proofGroup["type size"])

        self.w.leading = TextBox((leftEditText + 80, row + 2, 60, 22),
                                 "Leading:")

        self.w.leadingEdit = ComboBox((leftEditText + 139, row, 55, 22),
                                      pointSizes,
                                      continuous=True,
                                      callback=self._checkFloat)

        self.w.leadingEdit.set(self.proofGroup["leading"])

        row += 33
        self.w.contents = TextBox((left, row, textboxWidth, 20),
                                  "Contents:",
                                  alignment="right")

        self.w.contentsEdit = TextEditor((leftEditText, row, -10, 150),
                                         "\n".join(self.proofGroup["contents"]))

        row += 160
        self.w.okButton = Button((leftEditText, row, 138, 20),
                                 "OK",
                                 callback=self.okCB)
        leftEditText += 147
        self.w.cancelButton = Button((leftEditText, row, 138, 20),
                                     "Cancel",
                                     callback=self.cancelCB)

        self.w.bind("close", self._postCloseEvent)

    def _postCloseEvent(self, sender):
        postEvent("comInspectorClosed")

    def _checkFloat(self, sender):
        """
        Make sure users don't input non-floats by capturing
        value prior to new input, then using it
        if user tries to input an illegal character
        """
        # "last" is newly-typed character
        allButLast = sender.get()[:-1]
        try:
            float(sender.get())

            # Get rid of whitespaces immediately
            sender.set(sender.get().strip())
        except ValueError:
            sender.set(allButLast)

    def _makeCleanList(self, contentString):
        """
        Return a clean list from passed-in contentString

        Clean means no empty items and no leading and
        trailing whitespaces
        """
        tempList = contentString.split("\n")
        return [item.strip() for item in tempList if item.strip()]

    def okCB(self, sender):
        """
        Get everything from fields, save in self.newProofGroup dict,
        post events (pass the new group to observer), and close window
        """
        self.newProofGroup["group"] = self.w.groupNameEdit.get().strip()
        self.newProofGroup["type size"] = self.w.typeSizeEdit.get()
        self.newProofGroup["leading"] = self.w.leadingEdit.get()
        self.newProofGroup["contents"] = self._makeCleanList(self.w.contentsEdit.get())

        postEvent("comProofGroupEdited", newProofGroup=self.newProofGroup)
        self.w.close()

    def cancelCB(self, sender):
        self.w.close()


if __name__ == "__main__":
    # Test basic functions
    tempProofGroup = {
        "group": "UC, lc, numerals",
        "order": 1,
        "type size": 10,
        "leading": 18,
        "print": False,
        "contents": [
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "abcdefghijklmnopqrstuvwxyz",
            "0123456789"
        ]
    }

    groupInspector = ProofGroupInspector(tempProofGroup)
    groupInspector.w.open()
