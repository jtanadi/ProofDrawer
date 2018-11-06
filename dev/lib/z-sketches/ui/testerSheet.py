from vanilla import Sheet, Button

class TesterSheet:
    """
    Sheet that's passed into main dinwo.
    This is a candidate for DB preview window.
    """
    def __init__(self, parentWindow):
        self.w = Sheet((1200, 800), parentWindow)
        self.w.closeSheet = Button((10, 10, -10, 30),
                                   "Close Sheet",
                                   callback=self.closeSheetCB)
        # self.w.open()

    def closeSheetCB(self, sender):
        self.w.close()
