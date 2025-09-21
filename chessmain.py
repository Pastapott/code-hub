#imports tkinter into file
import tkinter as tk
#imports Board class from board fil
from board import Board

#symbols for each piece
PIECE_SYMBOLS = {
    "Pawn":   {"white": "♙", "black": "♟"},
    "Rook":   {"white": "♖", "black": "♜"},
    "Knight": {"white": "♘", "black": "♞"},
    "Bishop": {"white": "♗", "black": "♝"},
    "Queen":  {"white": "♕", "black": "♛"},
    "King":   {"white": "♔", "black": "♚"},
}

#class for the display
class chessGUI:
    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.create_board()

    def create_board(self):
        #Displays the chessboard and starting pieces
        for row in range(8):
            for col in range(8):
                #alternate square colours
                colour = "#EEEED2" if (row + col) % 2 == 0 else "#769656"
                frame = tk.Frame(
                    self.root,
                    width = 60,
                    height = 60,
                    bg = colour,
                    highlightbackground = "black",
                    highlightthickness = 1
                )
                frame.grid(row=row, column=col)
                label = tk.Label(frame, text=" ", font=("Arial", 32), bg = colour)
                label.pack(expand=True, fill = "both")
                self.squares[row][col] = label
        self.update_board()

    def update_board(self):
        #update board to match positions
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    self.squares[row][col].config(text=" ")
                else:
                    symbol = PIECE_SYMBOLS[piece.name][piece.colour]
                    self.squares[row][col].config(text=symbol)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess")

    game_board = Board().board
    gui = chessGUI(root, game_board)

    root.mainloop()

