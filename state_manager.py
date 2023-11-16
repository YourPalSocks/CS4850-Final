class State_Manager:
    # State format: L1:<blocks>-L2:<blocks>-L3:<blocks>

    # Snapshots of each state
    states = []

    def __init__(self):
        self.initial_state = ""
        self.final_state = ""

    def create_initial_state(self, init):
        # Verify 'init' state is legal
        # TODO
        # Set to first state
        self.states[0] = init
    
    def create_final_state(self, fin):
        # Verify 'fin' state is legal
        # TODO
        # Set to final state
        self.states.append(fin)

    def create_state(self, state_num):
        try:
            print(self.states[state_num])
        except IndexError:
            return 1 # State requested does not exist, send error signal
