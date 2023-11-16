from tkinter import *
from block import Block
from table import Table
from state_manager import State_Manager
from cmd_window import Cmd_Window

state_man = State_Manager()
state = 1

# Global components
cmd_win = ""
tab = ""
blocks = []
claw = ""
canvas = ""

def main():
    global cmd_win
    global canvas

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
    canvas = Canvas(disp_frame, bg="white", height=300, width=600)
    setup_canvas()
    canvas.pack()
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
    cmd_win.log("Enter 'help' to view available commands")

    # Star the main loop
    root.mainloop()

def setup_canvas():
    global tab
    global blocks
    global canvas
    # Table object
    tab = Table()
    # Blocks
    a = Block(25,25,"a")
    a.move_block(300, 150)
    # Add block to blocks
    blocks.append(a)

    # Draw everything
    tab.draw_table(canvas)
    a.draw_block(canvas)
    pass

def parse_command(win, c_in):
    global state
    # Get command (and argument) from input, then clear it
    cmd = c_in.get('1.0', 'end-1c').replace('\n', '')
    arg = ""
    if(len(cmd.split(" ")) > 1):
        arg = cmd.split(" ")[1]
    # Cleanup
    cmd = cmd.split(" ")[0]
    c_in.delete('1.0', END)
    # Add it to window before parsing
    cmd_win.log(f"> {cmd}")
    # Process the command
    if cmd == "clear": # Clear command window and last run
        win.do_clear()
    elif cmd == "next":
        state += 1
        if state_man.create_state(state) == 1:
            cmd_win.log("ERROR: Requested state does not exist")
    elif cmd == "prev":
        state -= 1
        if state_man.create_state(state) == 1:
            cmd_win.log("ERROR: Requested state does not exist")
    elif cmd == "initial":
        if(not arg):
            cmd_win.log("ERROR: intial state must be non-null")
            return
        cmd_win.log(arg)
    elif cmd == "final":
        pass
    elif cmd == "run":
        pass
    elif cmd == "help":
        cmd_win.log("""
initial <arg> -- Set the initial state of the blocks.
final   <arg> -- Set the final state of the blocks.
next          -- View the next state.
prev          -- View the previous state.
run           -- Run the AI simulation.
clear         -- Clear the Command Window and the last run.
            """)
    else:
        cmd_win.log("ERROR: unknown command")



if __name__ == "__main__":
    main()