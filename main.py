'''
Main application script. This is where the game starts.
'''
import tkinter as tk

from go import Go
from gui import GoGUI


def main():
    root = tk.Tk()
    GoGUI(root, Go(19))
    root.mainloop()


if __name__ == "__main__":
    main()
