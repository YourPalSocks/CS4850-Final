# Data-based classes containing information relavent to the solver
# This is separated from the other *.py classes that act as a graphical shell for this state information

class Block_State:
    # Relation info
    #   above: List of blocks this block is above
    #   on: The block this block directly sits on
    #   clear: Does this block have anything on top of it?
    #   table: Does this block sit directly on the table?
    def __init__(self, above, clear : bool, table : bool, label : chr):
        self.above = above
        self.clear = clear
        self.table = table
        self.label = label
        self.at_goal = False # Is this block its desired goal state?

    def __eq__(self, other): # Overwrite to compare two blocks to each other
        # Account for other being null
        if(not other):
            return False
        return(self.above == other.above and self.clear == other.clear 
               and self.table == other.table and self.label == other.label)
    

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
        self.parent = parent
        self.children = []
        self.viewed = False

    def __eq__(self, other):
        return self.__data == other.get_data()
    
    def get_data(self):
        return self.__data
    
    def get_child(self, index):
        return self.children[index]
    
    def add_child(self, child):
        self.children.append(child)
        # Return index of added child
        return len(self.children) - 1

    # Get first unviewed child, -1 if all children viewed
    # Does not consider this node in search
    def get_unviewed_child(self):
        for child in self.children:
            if not child.viewed:
                return child
        return -1
    
class StateTree:
    def __init__(self, data):
        # Create root of tree, move pointer to root
        self.root = Node(data, 0)
        self.pointer = self.root
        self.depth = 0
        self.goal_pointer = False # Which node is the goal state? For uptracing later

    def is_root(self):
        return self.depth == 0

    def add(self, n_data): # Add new node to pointer location
        return self.pointer.add_child(Node(n_data, self.pointer))
