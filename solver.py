# Class responsible for actually solving the problem
# Talks to State Manager to create GUI shell of solution

# Relations: ABOVE, ON, CLEAR, TABLE
class Solver:
    state_man = ""
    state_count = 0
    state_strings = []

    # State format: <blocks in 1>-<blocks in 2>-<blocks in 3>
    initial_state = ""
    final_state = ""

    def __init__(self, sm):
        self.state_man = sm

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

# Data-based classes containing information relavent to the solver
# This is separated from the other *.py classes that act as a graphical shell for this state information

class Block_State:
    # Relation info
    #   above: List of blocks above this one
    #   on: The block this block directly sits on
    #   clear: Does this block have anything on top of it?
    #   table: Does this block sit directly on the table? (0 if no)
    def __init__(self, above, on, clear : bool, table : int):
        self.above = above
        self.on = on
        self.clear = clear
        self.table = table
        self.at_goal = False # Is this block its desired goal state?

    def is_at_goal(self, fin_state):
        pass
    
class Arm_State:
    def __init__(self):
        self.holding = False # Holding nothing by default
        self.location = 1 # At location L1 by default

    def get_held(self):
        return self.holding

class Table_State:
    def __init__(self):
        # Keep track of what is where with 3 lists
        self.L1 = []
        self.L2 = []
        self.L3 = []