from proofPreset import ProofPreset

from vanilla import Sheet, TextBox, Button, EditText,\
                    Box, Window

class PresetsEditor:
    def __init__(self, mainWindow):
        self.w = Sheet((350, 300), mainWindow)

        left = 10
        row = 10
        textWidth = 90
        editLeft = left + textWidth + 5

        self.w.presetName = TextBox((left, row, textWidth, 20),
                                    "Preset name:")
        
        self.w.presetNameEdit = EditText((editLeft, row, -10, 22))

        
        row += 30
        self.w.importBox = Box((left, row, -10, 100))
        
        boxRow = 0
        boxLeft = 0
        self.w.importBox.importText = TextBox((boxLeft + 4, boxRow, -10, 20),
                                              "Import new proof file")

        boxRow += 30
        self.w.importBox.filePath = TextBox((boxLeft, boxRow, textWidth, 20),
                                            "File path:",
                                            alignment="right")
        self.w.importBox.filePathEdit = EditText((editLeft, boxRow, -10, 22))

        row += 100
        self.w.closeSheet = Button((left, row, -10, 20),
                                   "Close",
                                   callback=self.closeCB)

    def closeCB(self, sender):
        self.w.close()


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
