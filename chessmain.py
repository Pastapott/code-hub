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
        self.frames = [[None for _ in range(8)] for _ in range(8)]
        self.selected_square = None
        self.original_colors = [[None for _ in range(8)] for _ in range(8)]
        self.pieceSize = (56, 56)
        self.piece_images = {
            "Pawn": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-pawn.png").convert("RGBA").resize(self.pieceSize)),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-pawn.png").convert("RGBA").resize(self.pieceSize)),
            },
            "Rook": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-rook.png").convert("RGBA").resize(self.pieceSize)),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-rook.png").convert("RGBA").resize(self.pieceSize)),
            },
            "Knight": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-knight.png").convert("RGBA").resize(self.pieceSize)),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-knight.png").convert("RGBA").resize(self.pieceSize)),
            },
            "Bishop": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-bishop.png").convert("RGBA").resize(self.pieceSize)),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-bishop.png").convert("RGBA").resize(self.pieceSize)),
            },
            "Queen": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-queen.png").convert("RGBA").resize(self.pieceSize)),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-queen.png").convert("RGBA").resize(self.pieceSize)),
            },
            "King": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-king.png").convert("RGBA").resize(self.pieceSize)),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-king.png").convert("RGBA").resize(self.pieceSize)),
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
                self.original_colors[row][col] = colour
                frame = tk.Frame(
                    self.root,
                    width = 60,
                    height = 60,
                    bg = colour,
                    highlightbackground = "black",
                    highlightthickness = 1
                )
                frame.grid(row=row, column=col)

                self.frames[row][col] = frame
                label = tk.Label(frame, bg = colour)
                label.place(relx=0, rely=0, relwidth=1, relheight=1)
                self.squares[row][col] = label

                frame.bind("<Button-1>", lambda event, r=row, c=col: self.square_clicked(r, c))
                label.bind("<Button-1>", lambda event, r=row, c=col: self.square_clicked(r, c))
        self.update_board()

    def update_board(self):
        #update board to match positions
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                colour = self.original_colors[row][col]
                if piece is None:
                  self.squares[row][col].config(image="", text=" ", bg=colour)
                  self.squares[row][col].image = None
                else:
                  img = self.piece_images[piece.name][piece.colour]
                  self.squares[row][col].config(image=img, text="", bg=colour)
                  self.squares[row][col].image = img
    
    def attempt_move(self,start,end):
      sr, sc = start
      er, ec = end
      piece = self.board[sr][sc]

      if piece is None:
        return False
      
      possible_moves = piece.get_possible_moves((sr, sc), self.board)
      if (er, ec) not in possible_moves:
        return False
      if self.board[er][ec] is not None:
        captured = self.board[er][ec]
        print(f"{captured.colour} {captured.name} captured!")

      self.board[er][ec] = piece
      self.board[sr][sc] = None

      self.update_board()
      return True

    

    def square_clicked(self, row, col):
      print(f"Square clicked:({row}, {col})")

      if self.selected_square is None:
        if self.board[row][col] is not None:
          self.selected_square = (row, col)
          self.highlight_square(row, col, "#6FC0F2")
          print(f"Selected piece: {self.board[row][col].name} at ({row},{col})")
      elif self.selected_square == (row, col):
        self.deselect_square()
      else:
          if self.attempt_move(self.selected_square, (row,col)):
             print(f"moved piece to ({row}, {col})")
          else:
             print("Illegal Move")
          self.deselect_square()

    def highlight_square(self, row, col, highlight_colour):
      self.frames[row][col].config(bg=highlight_colour)
      self.squares[row][col].config(bg=highlight_colour)

    def deselect_square(self):
      if self.selected_square:
        row, col = self.selected_square
        original_colour = self.original_colors[row][col]
        self.frames[row][col].config(bg=original_colour)
        self.squares[row][col].config(bg=original_colour)
        self.selected_square = None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess")

    game_board = Board().board
    gui = chessGUI(root, game_board)

    root.mainloop()

