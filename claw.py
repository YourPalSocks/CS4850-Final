from block import Block

class Claw:

    def __init__(self):
        self.pos = 1 # Which table position are we at?
        self.x = 100
        self.y = 0

    # Move claw to L1, L2, or L3
    def move_claw(self, spot):
        if (spot == 1):
            self.x = 100
        elif (spot == 2):
            self.x = 300
        else:
            self.x = 500

    def get_block_spot(self):
        return [self.x - 15, self.y+45]

    def draw_claw(self, canvas):
        canvas.create_line(self.x, self.y, self.x, self.y + 30, width=2)
        # Create arms of claw
        canvas.create_line(self.x, self.y+30, self.x - 20, self.y+50, width=2)
        canvas.create_line(self.x, self.y+30, self.x + 20, self.y+50, width=2)