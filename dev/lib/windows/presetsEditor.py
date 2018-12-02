from AppKit import NSFont
from vanilla import Sheet, TextBox, Button, EditText, List, TextEditor

monoFont = NSFont.fontWithName_size_("Monaco", 13)

class PresetsEditor:
    def __init__(self, mainWindow, presetsList):
        self.presets = presetsList
        self.presetNames = [preset.name for preset in self.presets]
        self.selectedPreset = None
        self.selectedGroupIndex = None

        left = 10
        row = 10
        colWidth = 240
        listHeight = 210
        gutter = 15
        col2Left = left + colWidth + gutter
        col3Left = col2Left + colWidth + gutter
        # col4Left = col3Left + colWidth + gutter
        buttonWidth = 100
        windowWidth = col3Left + buttonWidth + 10

        self.w = Sheet((windowWidth, 500), mainWindow)

        self.w.presetsText = TextBox((left, row, colWidth, 20),
                                     "Presets:",
                                     sizeStyle="small")

        self.w.proofGroupsText = TextBox((col2Left, row, colWidth, 20),
                                         "Proof groups:",
                                         sizeStyle="small")

        row += 17
        self.w.presetsList = List((left, row, colWidth, listHeight),
                                  items=self.presetNames,
                                  allowsSorting=False,
                                  allowsMultipleSelection=False,
                                  allowsEmptySelection=False,
                                  selectionCallback=self.updatePresetInfo)

        self.w.proofGroupNames = List((col2Left, row, colWidth, listHeight),
                                      items=[],
                                      allowsSorting=False,
                                      allowsMultipleSelection=False,
                                      selectionCallback=self.updateGroupContents)

        buttonRow = row
        self.w.newPresetButton = Button((col3Left, buttonRow, buttonWidth, 22),
                                        "New preset",
                                        callback=self.testerCB)

        buttonRow += 30
        self.w.delPresetButton = Button((col3Left, buttonRow, buttonWidth, 22),
                                        "Delete preset",
                                        callback=self.testerCB)

        buttonRow += 60
        self.w.newGroupButton = Button((col3Left, buttonRow, buttonWidth, 22),
                                       "New group",
                                       callback=self.testerCB)

        buttonRow += 30
        self.w.delGroupButton = Button((col3Left, buttonRow, buttonWidth, 22),
                                       "Delete group",
                                       callback=self.testerCB)

        buttonRow += 102
        self.w.importText = TextBox((col3Left, buttonRow, buttonWidth, 20),
                                    "Import:",
                                    sizeStyle="small")

        buttonRow += 15
        self.w.importJSONButton = Button((col3Left, buttonRow, buttonWidth, 22),
                                         "JSON",
                                         callback=self.testerCB)
        buttonRow += 30
        self.w.importGroupsButton = Button((col3Left, buttonRow, buttonWidth, 22),
                                           "Proof groups",
                                           callback=self.testerCB)

        row += (listHeight + 12)
        self.w.groupContentsText = TextBox((left, row, colWidth, 20),
                                           "Group contents:",
                                           sizeStyle="small")

        row += 17
        self.w.groupContents = TextEditor((left, row, colWidth * 2 + gutter, -10),
                                          text="",
                                          readOnly=True,
                                          callback=self.editGroupContents)
        self.w.groupContents.getNSTextView().setFont_(monoFont)

        # self.w.renameText = TextBox((left, row, colWidth, 20),
        #                             "Rename preset:",
        #                             sizeStyle="small")

        # self.w.renameEdit = EditText((left, row, colWidth, 22))
        self.w.okButton = Button((col3Left, -32, buttonWidth, 22),
                                 "OK",
                                 callback=self.closeCB)

        self.w.setDefaultButton(self.w.okButton)

        self.updatePresetInfo()

    def closeCB(self, sender):
        self.w.close()

    def testerCB(self, sender):
        print("hit: %s" % sender)

    def updatePresetInfo(self, sender=None):
        """
        Update self.w.proofGroupNames and self.w.renameEdit,
        and reset proofGroupNames selection and groupContents
        when user selects preset from list
        """
        if sender is None:
            selectionIndex = 0
        else:
            if not sender.getSelection():
                return
            selectionIndex = sender.getSelection()[0]
        self.selectedPreset = self.presets[selectionIndex]

        self.w.proofGroupNames.set(self.selectedPreset.groupNames)
        self.w.proofGroupNames.setSelection([])
        self._resetGroupContents()

    def updateGroupContents(self, sender):
        """
        Update groupContents when user selects a proof group
        """
        if not sender.getSelection():
            self._resetGroupContents()
            return
        self.selectedGroupIndex = sender.getSelection()[0]
        selectedGroup = self.selectedPreset.groups[self.selectedGroupIndex]

        self.w.groupContents.set("\n".join(selectedGroup.contents))
        self.w.groupContents.getNSTextView().setEditable_(True)

    def editGroupContents(self, sender):
        """
        Set group contents to new contents
        """
        newContents = sender.get().split("\n")
        self.selectedPreset.editGroup(self.selectedGroupIndex,
                                      {"contents": newContents})

    def _resetGroupContents(self):
        """
        Set w.groupContents to empty string and
        make it readOnly
        """
        self.w.groupContents.set("")
        self.w.groupContents.getNSTextView().setEditable_(False)

if __name__ == "__main__":
    # Make a list of presets
    import os
    import proofPreset as pp
    from vanilla import Window

    currentDir = os.path.dirname(__file__)
    presetsDir = os.path.join(currentDir, "..", "..", "resources", "presets")

    # Mock main window
    class MockWindow:
        def __init__(self):
            self.w = Window((400, 400), "Mock Window")
            self.w.sheetButton = Button((10, 10, -10, 20),
                                        "Open sheet",
                                        callback=self.buttonCB)
            self.presets = []
            self._createPresetsList()

        def _createPresetsList(self):
            for f in os.listdir(presetsDir):
                fullPath = os.path.join(presetsDir, f)
                if os.path.isfile(fullPath) and os.path.splitext(f)[-1] == ".json":
                    preset = pp.ProofPreset()
                    preset.importFromJSON(fullPath)
                    self.presets.append(preset)

        def buttonCB(self, sender):
            sheet = PresetsEditor(self.w, self.presets)
            sheet.w.open()

    mockWindow = MockWindow()
    mockWindow.w.open()
