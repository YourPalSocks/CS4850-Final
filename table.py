class Table:
    __tableoffset__ = 100
    __tablestart__ = 220
    l1_pos = __tablestart__
    l2_pos = __tablestart__
    l3_pos = __tablestart__

    def __init__(self): 
        self.x = 0
        self.y = 250
        self.l1 = 200 - self.__tableoffset__
        self.l2 = 400 - self.__tableoffset__
        self.l3 = 600 - self.__tableoffset__

    def reset_table(self):
        self.l1_pos = self.__tablestart__
        self.l2_pos = self.__tablestart__
        self.l3_pos = self.__tablestart__

    def draw_table(self, canvas):
        canvas.create_line(self.x, self.y, 600, 250, width=5)
        # Draw position labels
        canvas.create_text(self.l1, self.y + 20, text="L1", font=('Helvetica','22','normal'))
        canvas.create_text(self.l2, self.y + 20, text="L2", font=('Helvetica','22','normal'))
        canvas.create_text(self.l3, self.y + 20, text="L3", font=('Helvetica','22','normal'))

    def get_table_position(self, spot):
        pos = [0, 0] # [x, y]
        if (spot == 1):
            pos[0] = self.l1 - 20
            pos[1] = self.l1_pos
            self.l1_pos -= 30
        elif (spot == 2):
            pos[0] = self.l2 - 20
            pos[1] = self.l2_pos
            self.l2_pos -= 30
        elif (spot == 3):
            pos[0] = self.l3 - 20
            pos[1] = self.l3_pos
            self.l3_pos -= 30
        return pos