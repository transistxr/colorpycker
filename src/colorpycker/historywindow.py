from PySide6.QtWidgets import QApplication, QMainWindow


# Subclass QMainWindow to customize your application's main window
class HistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # TODO: Viewing history of colours

def run():
    app = QApplication.instance()
    window = HistoryWindow()
    window.show()
    app.exec()