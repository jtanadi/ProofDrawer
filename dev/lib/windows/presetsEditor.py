from vanilla import Sheet, TextBox, Button, EditText,\
                    Box, Window, List, TextEditor
# from proofPreset import ProofPreset

class PresetsEditor:
    def __init__(self, mainWindow):
        self.w = Sheet((630, 300), mainWindow)

        left = 10
        row = 10
        width = 240
        height = 200
        col2Left = left + width + 15
        col3Left = col2Left + width + 15
        buttonWidth = 60

        self.w.presetsText = TextBox((left, row, width, 20),
                                     "Presets:",
                                     sizeStyle="small")

        self.w.proofGroupsText = TextBox((col2Left, row, width, 20),
                                         "Proof groups:",
                                         sizeStyle="small")

        row += 17
        self.w.presetsList = List((left, row, width, 200),
                                  items=[],
                                  rowHeight=17,
                                  allowsSorting=False)

        self.w.proofGroupsList = TextEditor((col2Left, row, width, height),
                                            text="List\nof\nproof\ngroups",
                                            readOnly=True)

        buttonRow = row
        self.w.closeButton = Button((col3Left, buttonRow, 100, 22),
                                    "Close",
                                    callback=self.closeCB)

        buttonRow += 50
        self.w.importPresetButton = Button((col3Left, buttonRow, 100, 22),
                                           "Import Preset",
                                           callback=self.testerCB)
        buttonRow += 30
        self.w.importGroupsButton = Button((col3Left, buttonRow, 100, 22),
                                           "Import Proof Groups",
                                           callback=self.testerCB)

        row += (height + 10)
        self.w.presetName = TextBox((left, row, width, 20),
                                    "Preset name:",
                                    sizeStyle="small")

        row += 17
        self.w.presetNameEdit = EditText((left, row, width, 22))

    def closeCB(self, sender):
        self.w.close()

    def testerCB(self, sender):
        print("hit: %s" % sender.get())

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
