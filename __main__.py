from tkinter import *
from block import Block
from table import Table
from claw import Claw
from state_manager import State_Manager
from cmd_window import Cmd_Window

state_man = State_Manager(0, 0, 0, 0)
state = 1
max_states = 1
compute_time = 0.0

# Global components
cmd_win = ""
tab = ""
blocks = {}
claw = ""
canvas = ""
state_lab = ""

def main():
    global cmd_win
    global canvas
    global state_lab

    root = Tk()
    root.title("CS4850 Final Project - Ethan Heinlein")
    # Configure window properties
    root.configure(background="snow")
    root.geometry("700x500+50+50")
    root.resizable(False, False)
    # Add component frames
    disp_frame = Frame(root) # Frame used for canvas and stats area
    disp_frame.pack(side=TOP)
    state_lab = Label(root, borderwidth=2, text=f"{state}/{max_states}")
    state_lab.pack(side=TOP)
    # Add components
    canvas = Canvas(disp_frame, bg="white", height=300, width=600)
    setup_canvas()
    canvas.pack()
    stats = Label(disp_frame, borderwidth=2, text=f"# States: {max_states}\t\tTime: {compute_time}s")
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

    # Give focus to command area
    cmd_in.focus_set()

    # Star the main loop
    root.mainloop()

def setup_canvas():
    global tab
    global blocks
    global canvas
    global state_man
    global claw

    # Table object
    tab = Table()
    # Blocks
    for c in range(ord('a'), ord('n') + 1):
        blocks.update({chr(c) : Block(25, 25, chr(c))})
    # Claw
    claw = Claw()
    claw.draw_claw(canvas)

    # Draw everything
    tab.draw_table(canvas)
    for block in blocks:
        blocks[block].draw_block(canvas)
    # Give to state manager
    state_man = State_Manager(blocks, tab, claw, canvas)

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
        state_man.reset_states()
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
        state_man.create_initial_state(arg)
    elif cmd == "final":
        if(not arg):
            cmd_win.log("ERROR: final state must be non-null")
            return
        state_man.create_final_state(arg)
    elif cmd == "run":
        if(state_man.get_state_num() < 2):
            cmd_win.log("ERROR: initial and final states must be set before running")
            return
        # TODO: Run the simulation
    elif cmd == "help":
        cmd_win.do_help()
    else:
        cmd_win.log("ERROR: unknown command")


if __name__ == "__main__":
    main()