from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
import webbrowser

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        vbox = QVBoxLayout(self)
        self.webView = QWebView(self)
        self.setCentralWidget(self.webView)
        self.webView.setUrl(QUrl("http://127.0.0.1:5000"))
        self.webView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.webView.linkClicked.connect(self.linkClicked)
        self.setWindowTitle("Inventory DB")

    def linkClicked(self, url):
        print("Page changed: " + url.toString())
        if url.toString().startswith("http://127.0.0.1"):
            self.webView.load(url)
            self.webView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        else:
            webbrowser.open(str(url.toString()))

def start_desk():
    app = QApplication([])
    win = MainWindow()
    win.show()
    return app.exec_()
