import sys
import os
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QFileDialog, QListWidget, QDialog
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QUrl, QDir, QObject, Signal, Slot
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebChannel import QWebChannel

class CustomStream(QObject):
    newText = Signal(str)

    def write(self, text):
        text = text.rstrip('\n')  # 移除尾部的换行符
        if text:  # 只有当文本不为空时，才发射信号
            self.newText.emit(str(text))
    def flush(self):
        pass

class ConsoleWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Console Output")
        self.listbox = QListWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.listbox)
        self.setLayout(layout)

    def appendText(self, text):
        self.listbox.addItem(text)
        self.listbox.scrollToBottom()

class Comm(QObject):
    logAck = Signal(str)
    anotherSignal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(str)
    def log(self, message):
        data = json.loads(message)
        print(type(data))
        self.logAck.emit('Ok Vue !')

    @Slot(str)
    def anotherFunction(self, message):
        self.anotherSignal.emit('Response to anotherFunction')

class MainWindow(QMainWindow):
    def __init__(self, debug=False, parent=None):
        super().__init__(parent)

        self.view = QWebEngineView(self)
        self.setCentralWidget(self.view)

        # Redirect sys.stdout to custom stream
        sys.stdout = CustomStream(newText=self.onUpdateText)

        # Console Window
        self.consoleWindow = ConsoleWindow(self)
        self.consoleWindow.show()

        # Set the QWebEngineSettings attributes
        self.view.page().settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        self.view.page().settings().setAttribute(QWebEngineSettings.JavascriptCanPaste, True)

        self.chan = QWebChannel(self)
        self.comm = Comm(self)
        self.chan.registerObject('channelInterface', self.comm)
        self.view.page().setWebChannel(self.chan)
        self.view.setContextMenuPolicy(Qt.NoContextMenu)

        # Create a menu bar and add menu items
        self.createMenuBar()

        if debug:
            self.view.load(QUrl('http://localhost:8080'))
            self.devView = QWebEngineView()
            self.view.page().setDevToolsPage(self.devView.page())
            self.devView.show()
        else:
            url = 'file:///' + QDir.fromNativeSeparators(
                os.path.abspath(os.path.join(os.path.dirname(__file__), './frontend/dist/index.html')))
            self.view.load(QUrl(url))

    def createMenuBar(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        fileMenu = QMenu("Data File", self)
        openAction = QAction("Select", self)
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)
        menubar.addMenu(fileMenu)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
        if fileName:
            print(f"File selected: {fileName}")
            self.comm.anotherSignal.emit(fileName)

    def onUpdateText(self, text):
        self.consoleWindow.appendText(text)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow(True)
    window.resize(500, 400)
    window.show()
    sys.exit(app.exec())
