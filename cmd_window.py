from tkinter import ttk, Misc, scrolledtext
import tkinter as tk

class Cmd_Window(scrolledtext.ScrolledText):

    def __init__(self, parent):
        scrolledtext.ScrolledText.__init__(self)
        self.root = parent
        self.config(state='disabled')

    def do_clear(self):
        self.config(state='normal')
        self.delete('1.0', tk.END)
        self.config(state='disabled')

    def log(self, txt):
        self.configure(state='normal')
        self.insert(tk.END, txt + "\n")
        self.see(tk.END)
        self.configure(state='disabled')