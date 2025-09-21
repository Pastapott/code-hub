#imports tkinter into file
import tkinter as tk
#imports Board class from board fil
from board import Board
from PIL import Image, ImageTk




#class for the display
class chessGUI:
    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.piece_images = {
            "Pawn": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-pawn.png").convert("RGBA").resize((56,56))),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-pawn.png").convert("RGBA").resize((56,56))),
            },
            "Rook": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-rook.png").convert("RGBA").resize((56,56))),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-rook.png").convert("RGBA").resize((56,56))),
            },
            "Knight": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-knight.png").convert("RGBA").resize((56,56))),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-knight.png").convert("RGBA").resize((56,56))),
            },
            "Bishop": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-bishop.png").convert("RGBA").resize((56,56))),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-bishop.png").convert("RGBA").resize((56,56))),
            },
            "Queen": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-queen.png").convert("RGBA").resize((56,56))),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-queen.png").convert("RGBA").resize((56,56))),
            },
            "King": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-king.png").convert("RGBA").resize((56,56))),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-king.png").convert("RGBA").resize((56,56))),
            }
        }
        self.create_board()
        for i in range(8):
            self.root.rowconfigure(i, weight=1)
            self.root.columnconfigure(i, weight=1)

    

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
                    self.squares[row][col].config(text=" ", width = 2, height = 1)
                else:
                    img = self.piece_images[piece.name][piece.colour]
                    self.squares[row][col].config(image=img, text = "")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess")

    game_board = Board().board
    gui = chessGUI(root, game_board)

    root.mainloop()

