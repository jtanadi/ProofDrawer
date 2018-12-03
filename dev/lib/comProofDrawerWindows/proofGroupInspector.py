"""
Proof group inspector window for ProofDrawer

Values in proof group passed-in aren't edited dynamically
(ie. if user edits "name" here, the original proof group
isn't immediately affected). Instead, values are passed
*back* to ProofDrawer only when user hits the OK button.

This is to prevent the edits made here from being permanent
while editing, in case user changes their mind and wants
to cancel.

The inspector posts an event when user presses OK button
(change is committed and data is passed back to ProofDrawer)
and when the window is closed (to enable ProofDrawer UI)
"""

from vanilla import FloatingWindow, TextBox, EditText,\
                    ComboBox, TextEditor, Button
from mojo.events import postEvent

from comProofDrawerUtils import helperFunctions as hf
from comProofDrawerWindows import monoFont

class ProofGroupInspector:
    def __init__(self, proofGroup):
        """
        Initialize inspector with proofGroup data.
        proofGroup is a dictionary passed in by ProofDrawer().
        """
        self.proofGroup = proofGroup
        self.editedProofGroup = {}

        left = 10
        row = 10
        textboxWidth = 92
        leftEditText = left + 95
        pointSizes = ["6", "8", "10", "12", "14", "18",\
                      "21", "24", "36", "48", "60", "72"]

        self.w = FloatingWindow((400, 275),
                                "Edit Proof Group: %s" % self.proofGroup["name"])

        self.w.groupName = TextBox((left, row + 2, textboxWidth, 20),
                                   "Group name:",
                                   alignment="right")

        self.w.groupNameEdit = EditText((leftEditText, row, -10, 22),
                                        self.proofGroup["name"])

        row += 33
        self.w.typeSize = TextBox((left, row + 2, textboxWidth, 20),
                                  "Type size (pt):",
                                  alignment="right")

        self.w.typeSizeEdit = ComboBox((leftEditText, row, 55, 22),
                                       pointSizes,
                                       continuous=True,
                                       callback=self._checkFloat)

        self.w.typeSizeEdit.set(self.proofGroup["typeSize"])

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
        self.w.contentsEdit.getNSTextView().setFont_(monoFont)

        row += 160
        self.w.cancelButton = Button((leftEditText, row, 138, 20),
                                     "Cancel",
                                     callback=self.cancelCB)

        leftEditText += 147
        self.w.okButton = Button((leftEditText, row, 138, 20),
                                 "OK",
                                 callback=self.okCB)

        self.w.setDefaultButton(self.w.okButton)
        self.w.bind("close", self._postCloseEvent)

    def _postCloseEvent(self, sender):
        postEvent("com.InspectorClosed")

    def _checkFloat(self, sender):
        """
        Make sure users don't input non-floats by capturing
        value prior to new input, then using it
        if user tries to input an illegal character
        """
        # pass
        # Store everything up to newly-typed character
        allButLast = sender.get()[:-1]
        try:
            float(sender.get())

            # Get rid of whitespaces immediately
            sender.set(sender.get().strip())
        except ValueError:
            sender.set(allButLast)

    def okCB(self, sender):
        """
        Get everything from fields, save in self.editedProofGroup dict,
        post event, pass the edited group to observer, and close window
        """
        self.editedProofGroup["name"] = self.w.groupNameEdit.get().strip()
        self.editedProofGroup["typeSize"] = self.w.typeSizeEdit.get()
        self.editedProofGroup["leading"] = self.w.leadingEdit.get()
        self.editedProofGroup["print"] = self.proofGroup["print"] # just pass this back for now
        self.editedProofGroup["contents"] = hf.makeCleanListFromStr(self.w.contentsEdit.get())

        postEvent("com.ProofGroupEdited", editedProofGroup=self.editedProofGroup)
        self.w.close()

    def cancelCB(self, sender):
        self.w.close()


if __name__ == "__main__":
    # Test basic functions
    tempProofGroup = {
        "name": "UC, lc, numerals",
        "typeSize": 10,
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
