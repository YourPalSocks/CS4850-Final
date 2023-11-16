from tkinter import ttk, Misc, scrolledtext
import tkinter as tk

class Cmd_Window(scrolledtext.ScrolledText):

    
    def __init__(self, parent):
        scrolledtext.ScrolledText.__init__(self)
        self.root = parent

    def do_clear(self):
        self.delete(0, tk.END)

    # Due to python's nature, parse_command needs to be last in this class
    cmd_table = {
        "clear": do_clear
    }

    def parse_command(self, cmd):
        pass
