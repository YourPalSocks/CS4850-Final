import time
import traceback
from copy import deepcopy
from solver_data import *
from multiprocessing import current_process
# Class responsible for actually solving the problem
# Talks to State Manager to create GUI shell of solution

# Relations: ABOVE, ON, CLEAR, TABLE
class Solver:
    state_count = 0
    MAX_DEPTH = 2

    # State format: <blocks in 1>-<blocks in 2>-<blocks in 3>
    initial_state = {}
    final_state = {}
    unique_states = []

    def __init__(self, init : str, fin : str):
        # Add initial and final states
        self.__add_state(init, True)
        self.__add_state(fin, False)

    def __add_state(self, state_str : str, initflag : bool):
        temp_table = {
            "L1" : [],
            "L2" : [],
            "L3" : []
        }
        spot = 1
        for blocks in state_str.split('-'):
            index = 0
            above_blocks = []
            for b in list(blocks): # Building bottom-up
                # Fill out block properties
                block = Block_State(above_blocks, index == len(list(blocks)) - 1, index == 0, b) # Come back for above
                temp_table["L" + str(spot)].append(block)
                above_blocks.append(block)
                index += 1
            spot += 1

        # Create initial state as data structure
        if initflag:
            self.initial_state["Arm"] = Arm_State()
            self.initial_state["Table"] = Table_State()
            self.initial_state["Table"].L1 = temp_table["L1"]
            self.initial_state["Table"].L2 = temp_table["L2"]
            self.initial_state["Table"].L3 = temp_table["L3"]
        else:
            self.final_state["Arm"] = Arm_State()
            self.final_state["Table"] = Table_State()
            self.final_state["Table"].L1 = temp_table["L1"]
            self.final_state["Table"].L2 = temp_table["L2"]
            self.final_state["Table"].L3 = temp_table["L3"]
        # Clone to current
        self.state_count += 1

    # The actual solver
    def solve(self):
        # Get time of start
        start_time = time.time()
        # Queue up initial set of actions
        st = StateTree(self.initial_state)
        action_queue = Queue()
        goal = 0
        found = False

        # Check if first node is correct
        if self.is_goal(self.initial_state):
            found = True
            print("GOAL", flush=True)
            goal = self.initial_state

        # Start searching -- Breadth
        try:
            while st.depth <= self.MAX_DEPTH and found == False:
                print("\nDepth: ", st.depth, flush=True)
                # Cycle through all nodes at level, then move down to new one
                nodes = st.get_layer()
                # Create new layer for results
                st.down_layer()
                for node in nodes:
                    # Get all actions for node
                    self.get_all_actions(node.get_data(), action_queue)
                    action_count = action_queue.size()
                    for i in range(action_count):
                        action_info = action_queue.dequeue()
                        # Add action as child of node
                        new_node = Node(action_info[1], node)
                        print(action_info[0], flush=True)
                        st.add(new_node)
                        if self.is_goal(new_node.get_data()):
                            print("GOALLLL", flush=True)
                            found = True
                            goal = new_node
        except:
            print(traceback.format_exc(), flush=True)

        # Done
        # TODO: Build up from node to root for state information
        # TODO: Convert state to string for GUI
        # Get time of end
        end_time = time.time()
        # Get final stats
        results = {}
        results["Found"] = found
        results["Time"] = abs(start_time - end_time) # Run time
        return results

    # Actions
    def can_stack(self, state):
        block = state["Arm"].get_held()
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        if len(stack) == 0:
            return False
        return (block != False and stack[-1].clear)
    
    def stack(self, s):
        '''
        PRE:: Arm is holding x; CLEAR(y); y and x at same location
        POST:: CLEAR(x); !CLEAR(y); ABOVE(x, y); ABOVE(x, y.above)
        '''
        state = deepcopy(s)
        block = state["Arm"].get_held()
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        action_str = ""
        if self.can_stack(state): # PRECONDITIONS
            state["Arm"].let_go()
            action_str = "S(" + block.label + ", " + stack[-1].label + ", " + "L" + str(pos) + ")"
            # Adjust block properties
            block.above = stack[-1].above
            block.above.append(stack[-1])
            block.clear = True
            stack[-1].clear = False
            stack.append(block) # Add block to top of stack
        # Build action string
        return [action_str, state]

    def can_unstack(self, state):
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        return state["Arm"].get_held() == False and not stack[-1].table

    def unstack(self, s):
        '''
        PRE:: Arm is empty; CLEAR(x); ON(x, y); !TABLE(x); !GOAL(x)
        POST:: Arm is holding x; !CLEAR(x); Nothing on x; x above == null
        '''
        state = deepcopy(s)
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        action_str = ""
        if self.can_unstack(state): # PRECONDITIONS
            block = stack.pop() # Remove block from stack
            action_str = "U(" + block.label + ", " + stack[-1].label + ", " + "L" + str(pos) + ")"
            # Adjust block properties
            block.clear = False
            block.above = []
            # Adjust new top block
            stack[-1].clear = True
            # Give block to arm
            state["Arm"].grab(block)
        return [action_str, state]
    
    def can_pickup(self, state):
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        return (state["Arm"].get_held() == False and stack[-1].clear and stack[-1].table)

    def pickup(self, s):
        '''
        PRE:: Arm is empty; TABLE(x); CLEAR(x); !GOAL(x)
        POST:: Arm is holding x; !TABLE(x); !CLEAR(x); x above == null
        '''
        state = deepcopy(s)
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        action_str = ""
        if self.can_pickup(state): # PRECONDITIONS
            block = stack.pop()
            action_str = "Pi(" + block.label + ", " + str(pos)  + ", " + "L" + str(pos) + ")"
            # Adjust block properties
            block.table = False
            block.clear = False
            block.above = []
            # Give to arm
            state["Arm"].grab(block)
        return [action_str, state]
    
    def can_putdown(self, state):
        pos = state["Arm"].get_location()
        block = state["Arm"].get_held()
        stack = state["Table"].get_stack(pos)
        return block != False and len(stack) == 0

    def putdown(self, s):
        '''
        PRE:: Arm is holding x; No blocks at location; Arm at location
        POST:: CLEAR(x); TABLE(x); Arm is empty
        '''
        state = deepcopy(s)
        pos = state["Arm"].get_location()
        block = state["Arm"].get_held()
        stack = state["Table"].get_stack(pos)
        action_str = ""
        if self.can_putdown(state): # PRECONDITIONS
            action_str = "Pu(" + block.label + ", " + "L" + str(pos) + ")"
            # Adjust block properties
            block.clear = True
            block.table = True
            state["Arm"].let_go()
            stack.append(block)
        return [action_str, state]
    
    def can_move(self, state, lk):
        pos = state["Arm"].get_location()
        return lk > 0 and lk < 4 and pos != lk and state["Arm"].get_held() != False

    def move(self, s, lk):
        '''
        PRE:: Arm is at li ; Arm is holding something; Arm is not at lk
        POST:: Arm is at lk
        '''
        state = deepcopy(s)
        action_str = ""
        if self.can_move(state, lk): # PRECONDITIONS
            action_str = "M(" + str(state["Arm"].get_location()) + ", " + str(lk) + ")"
            state["Arm"].move(lk)
        return [action_str, state]

    def noop(self):
        pass

    # Helper functions
    def is_goal(self, state):
        # Match every spot in the current state to the final state
        return self.final_state["Table"] == state["Table"] and state["Arm"].holding == False
    
    def is_unique(self, other):
        for state in self.unique_states:
            if state["Table"] == other["Table"] and state["Arm"] == other["Arm"]:
                return False
        # If unique, add to unique states
        self.unique_states.append(other)
        return True
        
    # Get all possible actions of state and load into queue
    def get_all_actions(self, state, queue : Queue):
        states_found = 0
        if self.can_unstack(state):
            queue.enqueue(self.unstack(state))
            states_found+= 1
        if self.can_stack(state):
            queue.enqueue(self.stack(state))
            states_found+= 1
        if self.can_move(state, 1):
            queue.enqueue(self.move(state, 1))
            states_found+= 1
        if self.can_move(state, 2):
            queue.enqueue(self.move(state, 2))
            states_found+= 1
        if self.can_move(state, 3):
            queue.enqueue(self.move(state, 3))
            states_found+= 1
        if self.can_pickup(state):
            queue.enqueue(self.pickup(state))
            states_found+= 1
        if self.can_putdown(state):
            queue.enqueue(self.putdown(state))
            states_found+= 1
        # print("Actions found: ", states_found, flush=True)

    def state_to_string(self, state):
        # TODO: Convert state to something readable by __main__.py
        return "Bababooey"