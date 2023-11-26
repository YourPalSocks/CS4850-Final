import time
from copy import deepcopy
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
            above_blocks = []
            for b in list(blocks): # Building bottom-up
                # Fill out block properties
                on = False
                if(index != 0): # Not on table? Must be on top of something
                    on = temp_table["L" + str(spot)][index - 1]
                block = Block_State(above_blocks, on, index == len(list(blocks)) - 1, index == 0, b) # Come back for above
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
        self.current_state = deepcopy(self.initial_state)

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
        self.state_count += 1

    # The actual solver
    def solve(self):
        if(self.state_count != 2): # Make sure initial and final states are loaded
            return
        # Get time of start
        start_time = time.time()
        # Queue up initial set of actions
        st = StateTree(self.initial_state)
        action_queue = Queue()
        self.get_all_actions(self.initial_state, action_queue)
        MAX_DEPTH = 16
        while(action_queue.size() > 0):
            if(st.pointer_depth >= MAX_DEPTH):
                pass # TODO: Move pointer over to adjacent node, or parent if unable to
            # Get all actions of this state, if not done so already
            if not st.pointer.viewed:
                self.get_all_actions(st.pointer.get_data())
                # Add each action to tree
                for i in range(0, action_queue.size()):
                    st.add(action_queue.dequeue())
                    # TODO: Check if any of these states are the goal state
                st.pointer.viewed = True # Can't load this state's actions again
            else:
                pass # TODO: Move pointer down to the right most child
        # Get time of end
        end_time = time.time()

    # Actions
    def can_stack(self, state):
        block = state["Arm"].get_held()
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        return (block != False and stack[-1].clear)
    
    def stack(self, state):
        '''
        PRE:: Arm is holding x; CLEAR(y); y and x at same location
        POST:: ON(x, y); CLEAR(x); !CLEAR(y); ABOVE(x, y); ABOVE(x, y.above)
        '''
        block = state["Arm"].get_held()
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        if self.can_stack(state): # PRECONDITIONS
            state["Arm"].let_go()
            # Adjust block properties
            block.on = stack[-1]
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

    def unstack(self, state):
        '''
        PRE:: Arm is empty; CLEAR(x); ON(x, y); !TABLE(x); !GOAL(x)
        POST:: Arm is holding x; !CLEAR(x); Nothing on x; x above == null
        '''
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        if self.can_unstack(state): # PRECONDITIONS
            block = stack.pop() # Remove block from stack
            # Adjust block properties
            block.clear = False
            block.above = []
            block.on = False
            # Adjust new top block
            stack[len(stack)].clear = True
            # Give block to arm
            state["Arm"].grab(block)
        return state
    
    def can_pickup(self, state):
        pos = state["Arm"].get_location()
        stack = state["Table"].get_stack(pos)
        return (state["Arm"].get_held() == False and stack[-1].clear and stack[-1].table)

    def pickup(self, state):
        '''
        PRE:: Arm is empty; TABLE(x); CLEAR(x); !GOAL(x)
        POST:: Arm is holding x; !TABLE(x); !CLEAR(x); x above == null
        '''
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

    def putdown(self, state):
        '''
        PRE:: Arm is holding x; No blocks at location; Arm at location
        POST:: CLEAR(x); TABLE(x); Arm is empty
        '''
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
        return lk > 0 and lk < 4 and pos != lk

    def move(self, state, lk):
        '''
        PRE:: Arm is at li
        POST:: Arm is at lk
        '''
        if self.can_move(state, lk): # PRECONDITIONS
            state["Arm"].move(lk)
        return state

    def noop(self):
        pass

    # Helper functions
    def is_at_goal(self, state):
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
            queue.enqueue(self.pickup())
        if self.can_putdown(state):
            queue.enqueue(self.putdown())