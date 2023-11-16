# A block as defined by the project
class Block:
    def __init__(self, x, y, letter):
        self.x = x
        self.length = 30
        self.y = y
        self.lb = letter

    # Draw the block on a canvas object
    def draw_block(self, canvas):
        # Draw the block
        canvas.create_rectangle(self.x, self.y, self.x + self.length, self.y + self.length, width=2, fill="green")
        # Draw the letter in the block
        canvas.create_text(self.x + self.length / 2, self.y + self.length / 2, text=self.lb, font=('Helvetica','22','bold'))

    # Move the block
    def move_block(self, n_x, n_y):
        self.x = n_x
        self.y = n_y