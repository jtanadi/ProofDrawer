from vanilla import Sheet, TextBox, Button, EditText,\
                    HorizontalLine, Window, List, TextEditor
# from proofPreset import ProofPreset

class PresetsEditor:
    def __init__(self, mainWindow):
        self.w = Sheet((630, 300), mainWindow)

        left = 10
        row = 10
        width = 240
        height = 210
        col2Left = left + width + 15
        col3Left = col2Left + width + 15
        buttonWidth = 100

        self.w.presetsText = TextBox((left, row, width, 20),
                                     "Presets:",
                                     sizeStyle="small")

        self.w.proofGroupsText = TextBox((col2Left, row, width, 20),
                                         "Proof groups:",
                                         sizeStyle="small")

        row += 17
        self.w.presetsList = List((left, row, width, height),
                                  items=["List", "of", "presets", "go", "here"],
                                  rowHeight=17,
                                  allowsSorting=False)

        self.w.proofGroupsList = TextEditor((col2Left, row, width, height),
                                            text="List\nof\nproof\ngroups",
                                            readOnly=True)

        buttonRow = row
        self.w.newButton = Button((col3Left, buttonRow, buttonWidth, 22),
                                  "New preset",
                                  callback=self.testerCB)

        buttonRow += 30
        self.w.deleteButton = Button((col3Left, buttonRow, buttonWidth, 22),
                                     "Delete preset",
                                     callback=self.testerCB)

        # buttonRow += 50
        # self.w.line1 = HorizontalLine((col3Left, buttonRow, -10, 1))

        buttonRow += 112
        self.w.importText = TextBox((col3Left, buttonRow, buttonWidth, 20),
                                    "Import:",
                                    sizeStyle="small")

        buttonRow += 17
        self.w.importJSONButton = Button((col3Left, buttonRow, buttonWidth, 22),
                                         "JSON",
                                         callback=self.testerCB)
        buttonRow += 30
        self.w.importGroupsButton = Button((col3Left, buttonRow, buttonWidth, 22),
                                           "Proof groups",
                                           callback=self.testerCB)

        row += (height + 12)
        self.w.renameText = TextBox((left, row, width, 20),
                                    "Rename preset:",
                                    sizeStyle="small")

        row += 17
        self.w.renameEdit = EditText((left, row, width, 22))
        self.w.closeButton = Button((col3Left, row, buttonWidth, 22),
                                    "Close",
                                    callback=self.closeCB)

    def closeCB(self, sender):
        self.w.close()

    def testerCB(self, sender):
        print("hit: %s" % sender)

if __name__ == "__main__":
    # Mock main window
    class MockWindow:
        def __init__(self):
            self.w = Window((400, 400), "Mock Window")
            self.w.sheetButton = Button((10, 10, -10, 20),
                                        "Open sheet",
                                        callback=self.buttonCB)

        def buttonCB(self, sender):
            sheet = PresetsEditor(self.w)
            sheet.w.open()

    mockWindow = MockWindow()
    mockWindow.w.open()
