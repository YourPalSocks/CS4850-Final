from tkinter import *
from block import Block
from cmd_window import Cmd_Window

def main():
    root = Tk()
    root.title("CS4850 Final Project - Ethan Heinlein")
    # Configure window properties
    root.configure(background="snow")
    root.geometry("700x500+50+50")
    root.resizable(False, False)
    # Add component frames
    disp_frame = Frame(root) # Frame used for canvas and stats area
    disp_frame.pack(side=TOP)
    state_num = Label(root, borderwidth=2, text="1/n")
    state_num.pack(side=TOP)
    # Add components
    c = Canvas(disp_frame, bg="white", height=300, width=600)
    setup_canvas(c)
    c.pack()
    stats = Label(disp_frame, borderwidth=2, text="Steps: 0\t\tTime: 0.0s")
    stats.pack()
    # Text area for information
    cmd_win = Cmd_Window(root)
    cmd_win.configure(width=80, height=8)
    cmd_win.pack()
    # Cmd area
    cmd_in = Text(root, width=82, height=1)
    cmd_in.pack()
    cmd_in.bind("<Return>",
                lambda event, win=cmd_win, c_in=cmd_in:parse_command(win,c_in))

    root.mainloop()

def setup_canvas(canvas):
    # Table line
    b = Block(25,25,"b")
    b.move_block(300, 150)
    canvas.create_line(0, 250, 600, 250, width=5,)
    b.draw_block(canvas)
    pass

def parse_command(win, c_in):
    # Get command from input
    cmd = c_in.get('1.0', 'end-1c').replace('\n', '')
    c_in.delete('1.0', END)
    # Add it to window before parsing
    log(win, f"{cmd}")
    # Parse the command
    if cmd == "clear": # Clear command window and last run
        win.do_clear()
    elif cmd == "next":
        pass
    elif cmd == "prev":
        pass
    elif cmd == "initial":
        pass
    elif cmd == "final":
        pass
    elif cmd == "run":
        pass
    else:
        log(win, "ERROR: unknown command")

# Easy function for writing stuff to the log
def log(win, txt):
    win.configure(state='normal')
    win.insert(END, txt + "\n")
    win.configure(state='disabled')


if __name__ == "__main__":
    main()