import os
from tkinter import *
from multiprocessing import Pool
from block import Block
from table import Table
from claw import Claw
from solver import Solver
from cmd_window import Cmd_Window

state = 1
states = []
state_num = 0

# Global components
cmd_win = ""
tab = ""
blocks = {}
claw = ""
canvas = ""
state_lab = ""
in_progress = False

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
    state_lab = Label(root, borderwidth=2, text=f"{state}/{len(states)}")
    state_lab.pack(side=TOP)
    # Add components
    canvas = Canvas(disp_frame, bg="white", height=300, width=600)
    canvas.pack()
    stats = Label(disp_frame, borderwidth=2, text=f"# States: {len(states)}\t\tTime: {0.0}s")
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

    setup_canvas()
    # Give focus to command area
    cmd_in.focus_set()

    # Star the main loop
    root.mainloop()

def setup_canvas():
    global tab
    global blocks
    global claw

    # Table object
    tab = Table()
    # Blocks
    for c in range(ord('a'), ord('n') + 1):
        blocks.update({chr(c) : Block(25, 25, chr(c))})
    # Claw
    claw = Claw()

def create_initial_state(init):
    global states
    global state_num

    # Set to first state
    reset_sim()
    states.append(init)
    # Create the first state on screen
    create_state(0)
    state_num += 1

def create_final_state(fin):
    global states
    global state_num
    
    # Set to final state
    states.append(fin)
    state_num += 1

# Draw a state to the GUI
def create_state(state_num):
    global tab
    global blocks
    global canvas
    global claw
    global cmd_win
    global states

    # Remove everything
    canvas.delete('all')
    tab.draw_table(canvas)
    try:
        cur_spot = 1
        for spot in states[state_num].split('-'):
            for block in list(spot):
                pos = tab.get_table_position(cur_spot)
                blocks.get(str(block)).move_block(pos[0], pos[1])
                blocks.get(str(block)).draw_block(canvas)
            cur_spot += 1
            
    except IndexError:
        return 1 # State requested does not exist, send error signal
    
def reset_sim():
    global states
    
    setup_canvas()
    states = []

def parse_command(win, c_in):
    global state
    global in_progress
    global state_num

    # Get command (and argument) from input, then clear it
    cmd = c_in.get('1.0', 'end-1c').replace('\n', '')
    arg = ""
    if(len(cmd.split(" ")) > 1):
        arg = cmd.split(" ")[1]
    # Cleanup
    cmd = cmd.split(" ")[0]
    c_in.delete('1.0', END)
    # Add it to window before parsing
    cmd_win.log(f"> {cmd} {arg}")
    # Process the command
    if cmd == "clear": # Clear command window and last run
        if not in_progress: # Only clear state manager if not running
            reset_sim()
        win.do_clear()
    elif cmd == "next":
        state += 1
        if create_state(state) == 1:
            cmd_win.log("ERROR: Requested state does not exist")
    elif cmd == "prev":
        state -= 1
        if create_state(state) == 1:
            cmd_win.log("ERROR: Requested state does not exist")
    elif cmd == "initial":
        if(not arg):
            cmd_win.log("ERROR: intial state must be non-null")
            return
        create_initial_state(arg)
    elif cmd == "final":
        if(not arg):
            cmd_win.log("ERROR: final state must be non-null")
            return
        create_final_state(arg)
    elif cmd == "run":
        if(state_num < 2):
            cmd_win.log("ERROR: initial and final states must be set before running")
            return
        if(in_progress):
            cmd_win.log("ERROR: Solver already running")
            return
        # Run and log the results
        with Pool(processes=1) as pool:
            in_progress = True
            pool.apply_async(start_state_solver, args=(states[0], states[-1]), callback=resultReceived, error_callback=errorReceived)
            pool.close()
            pool.join()
        cmd_win.log("Done")
    elif cmd == "help":
        cmd_win.do_help()
    else:
        cmd_win.log("ERROR: unknown command")

def start_state_solver(init : str, fin : str):
    # Set up the solver
    solver = Solver(init, fin)
    return solver.solve()

def resultReceived(result):
    global in_progress

    in_progress = False
    print(result, flush=True)
    return result

def errorReceived(error):
    global in_progress

    in_progress = False
    print(error, flush=True)
    return 1

if __name__ == "__main__":   
    main()