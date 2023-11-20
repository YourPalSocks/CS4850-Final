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

    def do_help(self):
        self.log("""
initial <arg> -- Set the initial state of the blocks.
final   <arg> -- Set the final state of the blocks.
next          -- View the next state.
prev          -- View the previous state.
run           -- Run the AI simulation.
clear         -- Clear the Command Window and the last run. 
                 
State format: <blocks in 1>-<blocks in 2>-<blocks in 3> (blocks seperated by commas)""")

    def log(self, txt):
        self.configure(state='normal')
        self.insert(tk.END, txt + "\n")
        self.see(tk.END)
        self.configure(state='disabled')