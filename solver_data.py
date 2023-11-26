# Data-based classes containing information relavent to the solver
# This is separated from the other *.py classes that act as a graphical shell for this state information

class Block_State:
    # Relation info
    #   above: List of blocks this block is above
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

    def __eq__(self, other): # Overwrite to compare two blocks to each other
        return(self.above == other.above and self.on == other.on and 
           self.clear == other.clear and self.table == other.table and self.label == other.label)
    

class Arm_State:
    def __init__(self):
        self.holding = False # Holding nothing by default
        self.location = 1 # At location L1 by default

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

    def get_stack(self, num : int):
        if num == 1:
            return self.L1
        elif num == 2:
            return self.L2
        else:
            return self.L3
        
    def get_stack_number(self, num : int):
        return len(self.get_stack(num))
        

# Used to store actions FIFO order
class Queue:
    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        return self._items.pop()
    
    def size(self):
        return len(self._items)
    
# Used to create graph of states to follow
class Node:
    def __init__(self, data, parent):
        self.__data = data
        self.parent = parent
        self.children = []
        self.viewed = False

    def __eq__(self, other):
        return self.__data == other.__data
    
    def get_data(self):
        self.viewed = True
        return self.__data

    def viewed(self):
        return self.viewed
    
    def add_child(self, child):
        self.children.append(child)
    
class StateTree:
    def __init__(self, data):
        # Create root of tree, move pointer to root
        self.root = Node(data, 0)
        self.pointer = self.root
        self.pointer_depth = 0
        self.goal_pointer = False # Which node is the goal state? For uptracing later

    def add(self, n_data): # Add new node to pointer location
        self.pointer.add_child(Node(n_data))
    
    def move_pointer(self, loc : int):
        try:
            if loc == -1 and self.pointer != self.root:
                self.pointer = self.pointer
                self.pointer_depth -= 1
            else:
                self.pointer = self.pointer.get_children()[loc]
                self.pointer_depth += 1
            return 0
        except IndexError:
            return -1