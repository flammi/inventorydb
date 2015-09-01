#!/usr/bin/python3
from gi.repository import Gtk
import sqlite3

class MainWindowHandler:
    def onSearchClick(self, btn):
        print("Test!")

builder = Gtk.Builder()
builder.add_from_file("gui.glade")
win = builder.get_object("window1")
builder.connect_signals(MainWindowHandler())
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
