from gi.repository import Gtk
from gi.repository import WebKit

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Inventory DB")
        self.set_size_request(1000,500)
        self.connect("delete-event", Gtk.main_quit)
        webView = WebKit.WebView()
        webView.linkClicked.connect(lambda url: print("Call!!!"))
        scroll = Gtk.ScrolledWindow()
        scroll.add(webView)
        self.add(scroll)
        webView.load_uri("http://127.0.0.1:5000")
        self.show_all()

def start_desk():
    win = MainWindow()
    Gtk.main()
