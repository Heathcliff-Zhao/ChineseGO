'''
GUI for the Go game.
'''
import tkinter as tk

from go import Go


class GoGUI(tk.Frame):
    def __init__(self, master, game: Go):
        super().__init__(master)
        self.game = game
        self.master = master
        self.master.title('Chinese Go Game')
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg='white', width=600, height=600)
        self.draw_board()
        self.canvas.bind('<Button-1>', self.place_stone)
        self.canvas.grid(row=0, column=0, pady=10)

    def draw_board(self):
        side_margin = 25
        ewe_margin = 25
        box_size = 600 - 2 * side_margin
        cell_size = box_size / (self.game.size - 1)
        for i in range(self.game.size):
            xpos = side_margin + i * cell_size
            ypos = ewe_margin + i * cell_size
            self.canvas.create_line(xpos, side_margin, xpos, 575, fill='black')
            self.canvas.create_line(side_margin, ypos, 575, ypos, fill='black')

    def place_stone(self, event):
        cell_size = (600 - 50) / (self.game.size - 1)
        y = round((event.x - 25) / cell_size)
        x = round((event.y - 25) / cell_size)
        color = self.game.turn
        if self.game.place_stone(x, y, color):
            self.canvas.delete('stone')
            for row in range(self.game.size):
                for col in range(self.game.size):
                    stone = self.game.board[row][col]
                    if stone != '-':
                        c = 'black' if stone == 'black' else 'white'
                        xpos = 25 + col * cell_size
                        ypos = 25 + row * cell_size
                        self.canvas.create_oval(xpos - 10, ypos - 10, xpos + 10, ypos + 10, fill=c, tags='stone')
            if self.game.check_end():
                winner = self.game.find_winner()
                msg = "It's a draw!" if winner == 'draw' else f"{winner.capitalize()} wins!"
                tk.messagebox.showinfo('Game Over', msg)
