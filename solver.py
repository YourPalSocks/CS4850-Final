import time
from solver_data import *
# Class responsible for actually solving the problem
# Talks to State Manager to create GUI shell of solution

# Relations: ABOVE, ON, CLEAR, TABLE
class Solver:
    state_man = ""
    state_count = 0

    # State format: <blocks in 1>-<blocks in 2>-<blocks in 3>
    initial_state = {}
    current_state = {}
    final_state = {}

    def __init__(self, sm):
        self.state_man = sm

    def add_initial(self, init : str):
        temp_table = {
            "L1" : [],
            "L2" : [],
            "L3" : []
        }
        for blocks in init.split('-'):
            index = 0
            spot = 1
            for b in list(blocks): # Building bottom-up
                # Fill out block properties
                on = False
                if(index != 0): # Not on table? Must be on top of something
                    on = temp_table["L" + str(spot)][index - 1]
                block = Block_State(False, on, index == len(list(blocks)) - 1, index == 0, b) # Come back for above
                temp_table["L" + str(spot)].append(block)
                index += 1
            spot += 1

        # Build list of above blocks
        for spot in range(1,4):
            block_num = len(temp_table["L" + str(spot)])
            for i in range(block_num - 1, 0, -1): # Start top -> down
                above_blocks = []
                for j in range(i, block_num):
                    above_blocks.append(temp_table["L" + str(spot)][j])
                temp_table["L" + str(spot)][i].above = above_blocks

        # Create initial state as data structure
        self.initial_state["Arm"] = Arm_State()
        self.initial_state["Table"] = Table_State()
        self.initial_state["Table"].L1 = temp_table["L1"]
        self.initial_state["Table"].L2 = temp_table["L2"]
        self.initial_state["Table"].L3 = temp_table["L3"]
        # Clone to current
        self.current_state = self.initial_state

    def add_final(self, fin):
        temp_table = {
            {"L1" : []},
            {"L2" : []},
            {"L3" : []}
        }
        for spot in fin.split('-'):
            index = 0
            spot_num = 1
            for b in list(spot): # Building bottom-up
                # Fill out block properties
                on = False
                if(score != 0): # Not on table? Must be on top of something
                    on = temp_table["L" + str(spot_num)][index - 1]
                block = Block_State(False, on, index == len(list(spot_num)) - 1, score == 0) # Come back for above
                temp_table["L" + str(spot_num)].append(block)
                score += 1
            spot_num += 1

        # Build list of above blocks
        for spot in range(1,4):
            block_num = len(temp_table["L" + str(spot)])
            for i in range(block_num - 1, 0, -1): # Start top -> down
                above_blocks = []
                for j in range(i, block_num - 1):
                    above_blocks.append(temp_table["L" + str(spot)][j])
                temp_table["L" + str(spot)][i].above = above_blocks

        # Create goal state as data structure
        self.initial_state.append({"Arm" : Arm_State()})
        self.final_state.append({"Table" : Table_State()})
        self.final_state["Table"].L1 = temp_table["L1"]
        self.final_state["Table"].L2 = temp_table["L2"]
        self.final_state["Table"].L3 = temp_table["L3"]

    # The actual solver
    def solve():
        start_time = time.start()
            

    # Actions
    def stack(li):
        '''
        PRE:: Arm is holding x; CLEAR(y); y and x at same location
        POST:: ON(x, y); CLEAR(y); ABOVE(x, y); ABOVE(x, y.above)
        '''
        pass

    def unstack(li):
        '''
        PRE:: Arm is empty; CLEAR(x); ON(x, y); !TABLE(x); !GOAL(x)
        POST:: Arm is holding x; !CLEAR(x); Nothing on x; x above == null
        '''
        pass

    def pickup(li):
        '''
        PRE:: Arm is empty; TABLE(x); CLEAR(x); !GOAL(x)
        POST:: Arm is holding x; !TABLE(x); !CLEAR(x); x above == null
        '''
        pass

    def putdown(li):
        '''
        PRE:: Arm is holding x; No blocks at location; Arm at location
        POST:: CLEAR(x); TABLE(x); Arm is empty
        '''
        pass

    def move(li, lk):
        '''
        PRE:: Arm is at li
        POST:: Arm is at lk
        '''
        pass

    def noop():
        pass

    # Helper functions
    def _is_block_at_goal(self, block):
        # Find the target block within goal state
        # It is assumed block is valid
        goal_block = 0
        for n_spot in range(1,4):
            spot = self.final_state["Table"].get_stack(n_spot)
            for searched in spot:
                if searched.label == block.label:
                    goal_block = searched
            if goal_block != 0:
                break
        # Compare the two blocks
        return block == goal_block
    
    def is_at_goal(self):
        flag = True
        for n_spot in range(1,4):
            spot = self.initial_state["Table"].get_stack(n_spot)
            for block in spot:
                flag = self._is_block_at_goal(block)
            if not flag:
                break
        return flag
