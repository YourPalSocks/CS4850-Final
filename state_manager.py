from block import Block
from table import Table
from claw import Claw
from solver import Solver

class State_Manager:
    # State format: <blocks in 1>-<blocks in 2>-<blocks in 3>

    # Snapshots of each state
    states = []
    solver = ""

    def __init__(self, blocks, table, claw, canvas):
        self.initial_state = ""
        self.final_state = ""
        # GUI Elements
        self.blocks = blocks
        self.table = table
        self.claw = claw
        self.canvas = canvas
        # Solver
        self.solver = Solver(self)

    def create_initial_state(self, init):
        # Set to first state
        self.reset_states()
        self.states.append(init)
        # Create the first state on screen
        self.create_state(0)
        # Give to solver
        self.solver.add_initial(init)
        
    
    def create_final_state(self, fin):
        # Set to final state
        self.states.append(fin)
        # Give to solver
        self.solver.add_final(fin)

    def get_state_num(self):
        return len(self.states)

    def create_state(self, state_num):
        # Remove everything
        self.canvas.delete('all')
        self.table.draw_table(self.canvas)
        try:
            cur_spot = 1
            for spot in self.states[state_num].split('-'):
                for block in list(spot):
                    pos = self.table.get_table_position(cur_spot)
                    self.blocks.get(str(block)).move_block(pos[0], pos[1])
                    self.blocks.get(str(block)).draw_block(self.canvas)
                cur_spot += 1
                
        except IndexError:
            return 1 # State requested does not exist, send error signal
        
    def reset_states(self):
        self.states = []
