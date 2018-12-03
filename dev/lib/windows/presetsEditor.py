from AppKit import NSFont
from vanilla import Sheet, TextBox, Button, EditText,\
                    List, TextEditor, Box

monoFont = NSFont.fontWithName_size_("Monaco", 13)

class PresetsEditor:
    def __init__(self, mainWindow, presetsList):
        self.presets = presetsList
        self.presetNames = [preset.name for preset in self.presets]
        self.selectedPreset = None
        self.selectedGroupIndex = None

        gutter = 10
        left = 10
        row = 10
        colWidth = 275
        listHeight = 115
        col2Left = left + colWidth + gutter
        btnWidth = 85
        btnHeight = 22
        boxWidth = btnWidth * 2 + 15
        windowWidth = col2Left + boxWidth + 10

        self.w = Sheet((windowWidth, 550), mainWindow)

        self.w.presetsText = TextBox((left, row, colWidth, 20),
                                     "Presets:",
                                     sizeStyle="small")

        row += 17
        self.w.presetsList = List((left, row, colWidth, listHeight),
                                  items=self.presetNames,
                                  allowsSorting=False,
                                  allowsMultipleSelection=False,
                                  allowsEmptySelection=False,
                                  selectionCallback=self.updatePresetInfo)

        self.w.presetCtrls = Box((col2Left, row, boxWidth, listHeight))

        boxLeft = 0
        boxRow = 0
        self.w.presetCtrls.edit = TextBox((boxLeft, boxRow, btnWidth, 20),
                                          "Edit:",
                                          sizeStyle="small")
        boxRow += 15
        self.w.presetCtrls.newBtn = Button((boxLeft, boxRow, btnWidth, btnHeight),
                                           "New",
                                           sizeStyle="small",
                                           callback=self.testerCB)

        boxRow += 22
        self.w.presetCtrls.dupeBtn = Button((boxLeft, boxRow, btnWidth, btnHeight),
                                            "Duplicate",
                                            sizeStyle="small",
                                            callback=self.testerCB)

        boxRow += 22
        self.w.presetCtrls.renameBtn = Button((boxLeft, boxRow, btnWidth, btnHeight),
                                              "Rename",
                                              sizeStyle="small",
                                              callback=self.testerCB)

        boxRow += 22
        self.w.presetCtrls.delBtn = Button((boxLeft, boxRow, btnWidth, btnHeight),
                                           "Delete",
                                           sizeStyle="small",
                                           callback=self.testerCB)

        boxRow = 0
        boxLeft += btnWidth + 7
        self.w.presetCtrls.importText = TextBox((boxLeft, boxRow, btnWidth, 20),
                                                "Import:",
                                                sizeStyle="small")

        boxRow += 15
        self.w.presetCtrls.importJSON = Button((boxLeft, boxRow, btnWidth, btnHeight),
                                               "JSON",
                                               sizeStyle="small",
                                               callback=self.testerCB)
        boxRow += 22
        self.w.presetCtrls.importGroups = Button((boxLeft, boxRow, btnWidth, btnHeight),
                                                 "Proof groups",
                                                 sizeStyle="small",
                                                 callback=self.testerCB)

        row += listHeight + 12
        self.w.proofGroupsText = TextBox((left, row, colWidth, 20),
                                         "Proof groups:",
                                         sizeStyle="small")

        row += 17
        listHeight = 150
        self.w.proofGroupNames = List((left, row, colWidth, listHeight),
                                      items=[],
                                      allowsSorting=False,
                                      allowsMultipleSelection=False,
                                      selectionCallback=self.updateGroupContents)

        self.w.groupCtrls = Box((col2Left, row, boxWidth, listHeight))

        boxLeft = 0
        boxRow = 0
        self.w.groupCtrls.newBtn = Button((boxLeft, boxRow, btnWidth, btnHeight),
                                          "New",
                                          sizeStyle="small",
                                          callback=self.testerCB)

        boxRow += 22
        self.w.groupCtrls.dupeBtn = Button((boxLeft, boxRow, btnWidth, btnHeight),
                                           "Duplicate",
                                           sizeStyle="small",
                                           callback=self.testerCB)

        boxRow += 22
        self.w.groupCtrls.rename = Button((boxLeft, boxRow, btnWidth, btnHeight),
                                          "Rename",
                                          sizeStyle="small",
                                          callback=self.testerCB)

        boxRow += 22
        self.w.groupCtrls.delBtn = Button((boxLeft, boxRow, btnWidth, btnHeight),
                                          "Delete",
                                          sizeStyle="small",
                                          callback=self.testerCB)

        boxRow = 22
        boxLeft += btnWidth + 7 + (btnWidth / 2 - 15)
        self.w.groupCtrls.upBtn = Button((boxLeft, boxRow, 30, btnHeight),
                                         "↑",
                                         sizeStyle="small",
                                         callback=self.testerCB)
        boxRow += 22
        self.w.groupCtrls.dnBtn = Button((boxLeft, boxRow, 30, btnHeight),
                                         "↓",
                                         sizeStyle="small",
                                         callback=self.testerCB)



        row += listHeight + 12
        self.w.groupContentsText = TextBox((left, row, colWidth, 20),
                                           "Group contents:",
                                           sizeStyle="small")

        row += 17
        self.w.groupContents = TextEditor((left, row, -10, -36),
                                          text="",
                                          readOnly=True,
                                          callback=self.editGroupContents)
        self.w.groupContents.getNSTextView().setFont_(monoFont)


        # self.w.renameText = TextBox((left, row, colWidth, 20),
        #                             "Rename preset:",
        #                             sizeStyle="small")

        # self.w.renameEdit = EditText((left, row, colWidth, btnHeight))
        row += 17
        self.w.okButton = Button((windowWidth/2 - btnWidth/2, -31, btnWidth, btnHeight),
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
    mockWindow.w.center()
