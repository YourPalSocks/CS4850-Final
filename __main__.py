from tkinter import *
from block import Block
from cmd_window import Cmd_Window

def main():
    root = Tk()
    root.title("CS4850 Final Project - Ethan Heinlein")
    # Configure window properties
    root.configure(background="snow")
    root.geometry("800x500+50+50")
    root.resizable(False, False)
    # Add component frames
    disp_frame = Frame(root) # Frame used for canvas and stats area
    disp_frame.pack(side=TOP)
    state_num = Label(root, borderwidth=-2, text="1/n")
    state_num.pack(side=TOP)
    # Add components
    c = Canvas(disp_frame, bg="white", height=300, width=600)
    setup_canvas(c)
    c.pack()
    stats = Label(disp_frame, borderwidth=2, text="Steps: 0\t\tTime: 0.0s")
    stats.pack()
    # Text area
    cmd_win = Cmd_Window(root)
    cmd_win.configure(width=80)
    cmd_win.pack(pady=10)
    cmd_win.bind("<<Modified>>", on_modification)

    root.mainloop()

def setup_canvas(canvas):
    # Table line
    b = Block(25,25,"b")
    b.move_block(300, 150)
    canvas.create_line(0, 250, 600, 250, width=5,)
    b.draw_block(canvas)
    pass

def on_modification(event):
    print("HI")

if __name__ == "__main__":
    main()