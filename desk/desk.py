#!/usr/bin/python3
from gi.repository import Gtk
from gi.repository import WebKit
import sqlite3

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Inventory DB")
        self.set_size_request(1000,500)
        webView = WebKit.WebView()
        scroll = Gtk.ScrolledWindow()
        scroll.add(webView)
        self.add(scroll)
        #webView.load_uri("http://127.0.0.1:5000/test")
        webView.load_uri("http://127.0.0.1:5000")

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
