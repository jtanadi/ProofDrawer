from vanilla import FloatingWindow, TextBox, EditText,\
                    ComboBox, TextEditor, Button
from mojo.events import postEvent

class ProofGroupInspector:
    def __init__(self):
        """
        Initialize inspector with empty fields.
        Fields will be populated when
        ProofGroupInspector.setProofGroup() is called.
        """
        left = 10
        row = 10
        textboxWidth = 92
        leftEditText = left + 95
        pointSizes = ["6", "8", "10", "12", "14", "18",\
                      "21", "24", "36", "48", "60", "72"]

        self.w = FloatingWindow((400, 275),
                                closable=False)

        self.w.groupName = TextBox((left, row + 2, textboxWidth, 20),
                                   "Group name:",
                                   alignment="right")

        self.w.groupNameEdit = EditText((leftEditText, row, -10, 22))

        row += 33
        self.w.typeSize = TextBox((left, row + 2, textboxWidth, 20),
                                  "Type size (pt):",
                                  alignment="right")

        self.w.typeSizeEdit = ComboBox((leftEditText, row, 55, 22),
                                       pointSizes,
                                       continuous=True,
                                       callback=self._checkFloat)

        self.w.leading = TextBox((leftEditText + 80, row + 2, 60, 22),
                                 "Leading:")

        self.w.leadingEdit = ComboBox((leftEditText + 139, row, 55, 22),
                                      pointSizes,
                                      continuous=True,
                                      callback=self._checkFloat)

        row += 33
        self.w.contents = TextBox((left, row, textboxWidth, 20),
                                  "Contents:",
                                  alignment="right")

        self.w.contentsEdit = TextEditor((leftEditText, row, -10, 150))

        row += 160
        self.w.okButton = Button((leftEditText, row, 138, 20),
                                 "OK",
                                 callback=self.okCB)
        leftEditText += 147
        self.w.cancelButton = Button((leftEditText, row, 138, 20),
                                     "Cancel",
                                     callback=self.cancelCB)

    def _checkFloat(self, sender):
        """
        Make sure users don't input non-floats by capturing
        value prior to new input, then using it
        if user tries to input an illegal character
        """
        # Store everything up to newly-typed character
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

    def setProofGroup(self, proofGroup):
        self.w.setTitle("Edit Proof Group: %s" % proofGroup["group"])
        self.w.groupNameEdit.set(proofGroup["group"])
        self.w.typeSizeEdit.set(proofGroup["type size"])
        self.w.leadingEdit.set(proofGroup["leading"])
        self.w.contentsEdit.set("\n".join(proofGroup["contents"]))

    def okCB(self, sender):
        """
        Get everything from fields, save in self.newProofGroup dict,
        post events (pass the new group to observer), and close window
        """
        newProofGroup = {}
        newProofGroup["group"] = self.w.groupNameEdit.get().strip()
        newProofGroup["type size"] = self.w.typeSizeEdit.get()
        newProofGroup["leading"] = self.w.leadingEdit.get()
        newProofGroup["contents"] = self._makeCleanList(self.w.contentsEdit.get())

        postEvent("comProofGroupEdited", newProofGroup=newProofGroup)
        postEvent("comInspectorClosed")
        self.w.hide()

    def cancelCB(self, sender):
        postEvent("comInspectorClosed")
        self.w.hide()


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

    groupInspector = ProofGroupInspector()
    groupInspector.setProofGroup(tempProofGroup)
    groupInspector.w.open()
