import sys
import os
import json
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QUrl, QDir, QObject, Signal, Slot
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebChannel import QWebChannel

class Comm(QObject):
    logAck = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(str)
    def log(self, message):
        data = json.loads(message)
        print(type(data))
        self.logAck.emit('Ok Vue !')

class MainWindow(QMainWindow):
    def __init__(self, debug=False, parent=None):
        super().__init__(parent)

        self.view = QWebEngineView(self)
        self.setCentralWidget(self.view)

        # Set the QWebEngineSettings attributes
        self.view.page().settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        self.view.page().settings().setAttribute(QWebEngineSettings.JavascriptCanPaste, True)

        self.chan = QWebChannel(self)
        self.comm = Comm(self)
        self.chan.registerObject('channelInterface', self.comm)
        self.view.page().setWebChannel(self.chan)
        self.view.setContextMenuPolicy(Qt.NoContextMenu)

        if debug:
            self.view.load(QUrl('http://localhost:8080'))
            self.devView = QWebEngineView()
            self.view.page().setDevToolsPage(self.devView.page())
            self.devView.show()
        else:
            url = 'file:///' + QDir.fromNativeSeparators(
                os.path.abspath(os.path.join(os.path.dirname(__file__), './frontend/dist/index.html')))
            self.view.load(QUrl(url))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow(True)
    window.resize(500, 400)
    window.show()
    sys.exit(app.exec())

