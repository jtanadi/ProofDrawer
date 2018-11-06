from vanilla import *

class ProofDrawerWindow:
    def __init__(self, childWindow, childSheet):
        self.childWindow = childWindow
        self.childSheet = childSheet

        self.w = Window((300, 600), "Proofing Drawer")
        self.drawer = Drawer((280, 600),
                             self.w,
                             leadingOffset=0,
                             trailingOffset=10)

        self.w.openDrawer = Button((10, 10, -10, 30),
                                   "Open drawer",
                                   callback=self.openDrawerCB,
                                   sizeStyle="regular")
        self.w.openWindow = Button((10, 50, -10, 30),
                                   "Open Window",
                                   callback=self.openWindowCB,
                                   sizeStyle="regular")
        self.w.openSheet = Button((10, 90, -10, 30),
                                  "Open Sheet",
                                  callback=self.openSheetCB,
                                  sizeStyle="regular")

        self.w.open()
        self.w.center()

    def openDrawerCB(self, sender):
        self.drawer.toggle()
    
    def openWindowCB(self, sender):
        self.childWindow()

    def openSheetCB(self, sender):
        """
        This is a weird way of opening a sheet?
        - Create new instance of the passed-in sheet
        - Execute the instance's Sheet.open() method

        vs.
        - Keep self.w.open() in TesterSheet()
        - Just call self.childSheet(self.w) here
        """
        childSheetInstance = self.childSheet(self.w)
        childSheetInstance.w.open()

if __name__ == "__main__":
    from ui.testerSheet import TesterSheet
    from ui.testerWindow import TesterWindow
    ProofDrawerWindow(TesterWindow, TesterSheet)
