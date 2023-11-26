import time
from copy import deepcopy
from solver_data import *
from multiprocessing import current_process
# Class responsible for actually solving the problem
# Talks to State Manager to create GUI shell of solution

# Relations: ABOVE, ON, CLEAR, TABLE
class Solver:
    state_count = 0
    MAX_DEPTH = 16

    # State format: <blocks in 1>-<blocks in 2>-<blocks in 3>
    initial_state = {}
    final_state = {}

    def __init__(self, init : str, fin : str):
        self.add_initial(init)
        self.add_final(fin)

    def add_initial(self, init : str):
        temp_table = {
            "L1" : [],
            "L2" : [],
            "L3" : []
        }
        for blocks in init.split('-'):
            index = 0
            spot = 1
            above_blocks = []
            for b in list(blocks): # Building bottom-up
                # Fill out block properties
                block = Block_State(above_blocks, index == len(list(blocks)) - 1, index == 0, b) # Come back for above
                temp_table["L" + str(spot)].append(block)
                above_blocks.append(block)
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
        self.state_count += 1

    def add_final(self, fin : str):
        temp_table = {
            "L1" : [],
            "L2" : [],
            "L3" : []
        }
        for blocks in fin.split('-'):
            index = 0
            spot = 1
            above_blocks = []
            for b in list(blocks): # Building bottom-up
                # Fill out block properties
                block = Block_State(above_blocks, index == len(list(blocks)) - 1, index == 0, b) # Come back for above
                temp_table["L" + str(spot)].append(block)
                above_blocks.append(block)
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
        self.get_all_actions(self.initial_state, action_queue)
        st.pointer.viewed = True
        while(action_queue.size() > 0):
            print(action_queue.size(), flush=True)
            if(st.pointer_depth >= Solver.MAX_DEPTH):
                # Move pointer to parent, if possible
                if not st.is_root():
                    st.pointer = st.pointer.parent
                # Find adjacent node, if applicable or stay at parent
                adj_node = st.pointer.get_unviewed_child()
                if adj_node != -1:
                    st.pointer = adj_node
            # Get all actions of this state, if not done so already
            if not st.pointer.viewed:
                # Add each action to tree, check if goal
                for i in range(0, action_queue.size() - 1):
                    action = action_queue.dequeue()
                    index = st.add(action) # Add new action to StateTree
                    # Check if this is the goal
                    if self.is_goal(action):
                        # We have found the goal, assign accordingly and stop running
                        st.goal_pointer = st.pointer.get_child(index)
                        action_queue.clear()
                        break
            # Move down tree
            result = st.pointer.get_unviewed_child()
            # Queue up next set of actions, if possible
            if result != -1:
                st.pointer = result
                self.get_all_actions(st.pointer.get_data(), action_queue)
                st.pointer.viewed = True
            elif st.pointer.parent != 0: # All children cleared, queue up sibling of this node, if possible
                result = st.pointer.parent.get_unviewed_child()
                if result != -1:
                    st.pointer = result
                    self.get_all_actions(st.pointer.get_data(), action_queue)
                    st.pointer.viewed = True
        # Get time of end
        end_time = time.time()
        # Get final stats
        fin_time = abs(start_time - end_time) # Run time
        return fin_time

    # Actions
    def can_stack(self, state):
        block = state["Arm"].get_held()
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        return (block != False and stack[-1].clear)
    
    def stack(self, s):
        '''
        PRE:: Arm is holding x; CLEAR(y); y and x at same location
        POST:: ON(x, y); CLEAR(x); !CLEAR(y); ABOVE(x, y); ABOVE(x, y.above)
        '''
        state = deepcopy(s)
        block = state["Arm"].get_held()
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        if self.can_stack(state): # PRECONDITIONS
            state["Arm"].let_go()
            # Adjust block properties
            block.above.append(stack[-1])
            block.above.append(stack[-1].above)
            block.clear = True
            stack[-1].clear = False
            stack.append(block) # Add block to top of stack
        return state

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
        if self.can_unstack(state): # PRECONDITIONS
            block = stack.pop() # Remove block from stack
            # Adjust block properties
            block.clear = False
            block.above = []
            # Adjust new top block
            stack[-1].clear = True
            # Give block to arm
            state["Arm"].grab(block)
        return state
    
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
        if self.can_pickup(state): # PRECONDITIONS
            block = stack.pop
            # Adjust block properties
            block.table = False
            block.clear = False
            block.above = []
            # Give to arm
            state["Arm"].grab(block)
        return state
    
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
        if self.can_putdown(state): # PRECONDITIONS
            # Adjust block properties
            block.clear = True
            block.table = True
            state["Arm"].let_go()
            stack.append(block)
        return state
    
    def can_move(self, state, lk):
        pos = state["Arm"].get_location()
        return lk > 0 and lk < 4 and pos != lk and state["Arm"].get_held() != False

    def move(self, s, lk):
        '''
        PRE:: Arm is at li ; Arm is holding something
        POST:: Arm is at lk
        '''
        state = deepcopy(s)
        if self.can_move(state, lk): # PRECONDITIONS
            state["Arm"].move(lk)
        return state

    def noop(self):
        pass

    # Helper functions
    def is_goal(self, state):
        # Match every spot in the current state to the final state
        for n_spot in range(1,4):
            spot = state["Table"].get_stack(n_spot)
            final_spot = self.final_state["Table"].get_stack(n_spot)
            # Block_Data has an equal operator override
            if(spot != final_spot):
                return False
        return True
    
    def get_stack_name(self, num : int):
        if(num > 0 and num < 4):
            return "L" + str(num)
        
    # Get all possible actions of state and load into queue
    def get_all_actions(self, state, queue : Queue):
        if self.can_unstack(state):
            queue.enqueue(self.unstack(state))
        if self.can_stack(state):
            queue.enqueue(self.stack(state))
        if self.can_move(state, 1):
            queue.enqueue(self.move(state, 1))
        if self.can_move(state, 2):
            queue.enqueue(self.move(state, 2))
        if self.can_move(state, 3):
            queue.enqueue(self.move(state, 3))
        if self.can_pickup(state):
            queue.enqueue(self.pickup(state))
        if self.can_putdown(state):
            queue.enqueue(self.putdown(state))

    def state_to_string(self, state):
        # TODO: Convert state to something readable by __main__.py
        return "Bababooey"