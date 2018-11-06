from vanilla import Window

class TesterWindow:
    """
    Window that's passed into main window.
    This is a candidate for DB preview window.
    """
    def __init__(self):
        self.w = Window((600, 800), "Test Window")
        self.w.open()