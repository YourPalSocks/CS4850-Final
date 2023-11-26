# Data-based classes containing information relavent to the solver
# This is separated from the other *.py classes that act as a graphical shell for this state information

class Block_State:
    # Relation info
    #   above: List of blocks above this one
    #   on: The block this block directly sits on
    #   clear: Does this block have anything on top of it?
    #   table: Does this block sit directly on the table?
    def __init__(self, above, on, clear : bool, table : bool, label : chr):
        self.above = above
        self.on = on
        self.clear = clear
        self.table = table
        self.label = label
        self.at_goal = False # Is this block its desired goal state?

    def __eq__(self, other):
        flag = True
        if(self.above != other.above or self.on != other.on or 
           self.clear != other.clear or self.table != other.table):
            flag = False
        return flag
    
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

    def get_stack(self, num : int):
        if num == 1:
            return self.L1
        elif num == 2:
            return self.L2
        else:
            return self.L3
        