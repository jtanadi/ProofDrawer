from vanilla import Window, TextBox, EditText, TextEditor, Button
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

        self.w = Window((400, 320),
                        "Edit Proof Group")

        self.w.groupName = TextBox((left, row, 150, 20),
                                   "Edit Proof Group: %s" % self.proofGroup["group"])

        row += 22
        self.w.groupNameEdit = EditText((left, row, -10, 20),
                                        self.proofGroup["group"])

        row += 35
        self.w.typeSize = TextBox((left, row + 2, 95, 20),
                                  "Type size (pt):")

        self.w.typeSizeEdit = EditText((left + 95, row, 45, 22),
                                       self.proofGroup["type size"])

        self.w.leading = TextBox((left + 150, row + 2, 60, 22),
                                 "Leading:")
        self.w.leadingEdit = EditText((left + 210, row, 45, 22),
                                      self.proofGroup["leading"])

        row += 35
        self.w.contents = TextBox((left, row, 150, 20),
                                  "Contents:")

        row += 22
        self.w.contentsEdit = TextEditor((left, row, -10, 150),
                                         "\n".join(self.proofGroup["contents"]))

        row += 160
        self.w.okButton = Button((left, row, 185, 20),
                                 "OK",
                                 callback=self.okCB)
        left += 195
        self.w.cancelButton = Button((left, row, 185, 20),
                                     "Cancel",
                                     callback=self.cancelCB)

        self.w.bind("close", self._postCloseEvent)

    def _postCloseEvent(self, sender):
        postEvent("comInspectorClosed")

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
