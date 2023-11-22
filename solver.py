# Class responsible for actually solving the problem
# Talks to State Manager to create GUI shell of solution
class Solver:
    state_man = ""
    state_count = 0
    states = {
        1 : {
        "L1": [],
        "L2": [],
        "L3": [],
        "Claw": [1, ''] # [0] = Spot (1,2,3) | [1] = block held
        }
    } # Everything inbetween initial and final (strings)
    block_vals = {} # Tie blocks to numbers for easy comparison
    initial_state = ""
    final_state = ""

    def __init__(self, sm):
        self.state_man = sm

    def add_initial(self, init : str):
        self.initial_state = init
        # Add state to state dictionary
        for spot in range(len(init.split('-'))): # L1-L3
            block_list = init.split('-')[spot]
            for block in list(block_list):
                self.states[1]['L' + str(spot)].append(block)
        self.state_count += 1


    def add_final(self, fin):
        self.final_state = fin
        self.state_count += 1

    def solve(self):
        # Initial and Final not set, stop
        if(self.state_count != 2):
            return 1
        
        # First, get every block in the right table spot
        self._get_blocks_in_proper_order()
        # Next, reorganize blocks in proper order in spot
        self._get_blocks_in_proper_spot()

    def _get_blocks_in_proper_spot(self):
        pass

    def _get_blocks_in_proper_order(self):
        pass