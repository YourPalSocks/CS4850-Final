# Data-based classes containing information relavent to the solver
# This is separated from the other *.py classes that act as a graphical shell for this state information

class Block_State:
    # Relation info
    #   above: List of blocks this block is above
    #   on: The block this block directly sits on
    #   clear: Does this block have anything on top of it?
    #   table: Does this block sit directly on the table?
    def __init__(self, clear : bool, table : bool, label : chr):
        self.clear = clear
        self.table = table
        self.label = label

    def __eq__(self, other): # Overwrite to compare two blocks to each other
        # Account for other being null
        if(not other):
            return False
        # Check single properties
        if self.label != other.label or self.table != other.table \
                or self.clear != other.clear:
            return False
        # All tests passed
        return True

class Arm_State:
    def __init__(self):
        self.holding = False # Holding nothing by default
        self.location = 1 # At location L1 by default

    def __eq__(self, other):
        return self.holding == other.holding and self.location == other.location

    def let_go(self):
        self.holding = False

    def grab(self, block):
        self.holding = block

    def move(self, loc):
        self.location = loc

    def get_location(self):
        return self.location

    def get_held(self):
        return self.holding


class Table_State:
    def __init__(self):
        # Keep track of what is where with 3 lists
        self.L1 = []
        self.L2 = []
        self.L3 = []

    def __eq__(self, other):
        res1 = self.__compare_stack(self.L1, other.L1)
        res2 = self.__compare_stack(self.L2, other.L2)
        res3 = self.__compare_stack(self.L3, other.L3)
        if res1 and res2 and res3:
            return True
        return False

    def __compare_stack(self, stack, other):
        if len(stack) != len(other):
            return False
        # Check if both are empty
        if len(stack) == 0 and len(other) == 0:
            return True
        for i in range(0, len(stack)):
            # Compare the blocks above this block
            above_me = stack[i:len(stack)]
            above_other = other[i:len(stack)]
            if above_me != above_other:
                return False
            if stack[i] != other[i]:
                return False
        return True

    def get_stack(self, num : int):
        if num == 1:
            return self.L1
        elif num == 2:
            return self.L2
        else:
            return self.L3
        

# Used to store actions FIFO order
class Queue:
    def __init__(self):
        self.__items = []

    def enqueue(self, item):
        self.__items.append(item)

    def dequeue(self):
        return self.__items.pop(0)
    
    def size(self):
        return len(self.__items)
    
    def clear(self):
        self.__items = []
    
# Used to create graph of states to follow
class Node:
    def __init__(self, data, parent):
        self.__data = data
        self.viewed = False
        self.parent = parent
        self.goal = False # Is this the goal node
    
    def get_data(self):
        return self.__data
    
class StateTree:
    def __init__(self, data):
        # Create root of tree, move pointer to root
        self.root = Node(data, 0)
        self.layers = {
            0 : [self.root]
        }
        self.num_layers = 0
        self.goal_index = 0
        self.depth = 0 # current depth

    def is_root(self):
        return self.depth == 0
    
    def get_layer(self):
        return self.layers[self.depth]

    def add(self, node): # Add node to this layer
        self.layers[self.depth].append(node)
    
    def down_layer(self):
        self.depth += 1
        self.layers[self.depth] = []
