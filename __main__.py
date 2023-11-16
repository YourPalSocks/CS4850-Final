from tkinter import *
from block import Block

def main():
    root = Tk()
    root.title("CS4850 Final Project - Ethan Heinlein")
    # Configure window properties
    root.configure(background="snow")
    root.geometry("800x500+50+50")
    root.resizable(False, False)
    # Add components
    c = Canvas(root, bg="white", height=300, width=600)
    setupCanvas(c)
    c.pack()

    root.mainloop()

def setupCanvas(canvas):
    # Table line
    b = Block(25,25,"b")
    b.move_block(300, 150)
    canvas.create_line(0, 250, 600, 250, width=5,)
    b.draw_block(canvas)
    pass

if __name__ == "__main__":
    main()