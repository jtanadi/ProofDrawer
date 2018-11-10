from vanilla import Window, TextBox, EditText, TextEditor

class ProofGroupInspector:
    def __init__(self, proofGroup):
        self.w = Window((500, 400), "Edit Proof Group")

        left = 10
        row = 10

        self.w.groupName = TextBox((left, row, 150, 20),
                                   "Group name:")

        row += 25
        self.w.groupNameEdit = EditText((left, row, -10, 20))

        row += 30
        self.w.typeSize = TextBox((left, row, 150, 20),
                                  "Point size:")
        self.w.typeSizeEdit = EditText((left + 175, row, 50, 20))
        
        self.w.leading = TextBox((left + 250, row, 150, 20),
                                 "Leading:")
        self.w.leadingEdit = EditText((left + 425, row, 50, 20))
    
if __name__ == "__main__":
    tempProofGroup = [
        {
            "group": "UC, lc, numerals",
            "type size": "",
            "order": 1,
            "leading": "",
            "print": False,
            "contents": [
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "abcdefghijklmnopqrstuvwxyz",
            "0123456789"
            ]
        }
    ]

    groupInspector = ProofGroupInspector(1) # pass in something...
    groupInspector.w.open()
