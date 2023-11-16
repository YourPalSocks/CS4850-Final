class Table:
    __tableoffset__ = 100

    def __init__(self): 
        self.x = 0
        self.y = 250
        self.l1 = 200 - self.__tableoffset__
        self.l2 = 400 - self.__tableoffset__
        self.l3 = 600 - self.__tableoffset__

    def draw_table(self, canvas):
        canvas.create_line(self.x, self.y, 600, 250, width=5)
        # Draw position labels
        canvas.create_text(self.l1, self.y + 20, text="L1", font=('Helvetica','22','normal'))
        canvas.create_text(self.l2, self.y + 20, text="L2", font=('Helvetica','22','normal'))
        canvas.create_text(self.l3, self.y + 20, text="L3", font=('Helvetica','22','normal'))