#imports tkinter into file
import tkinter as tk
#imports Board class from board fil
from board import Board
from PIL import Image, ImageTk
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

#class for the display
class chessGUI:
    def __init__(self, root, game: Board):
        self.root = root
        self.game = game
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.frames = [[None for _ in range(8)] for _ in range(8)]
        self.selected_square = None
        self.original_colors = [[None for _ in range(8)] for _ in range(8)]
        self.pieceSize = (56, 56)
        self.current_turn = "white"
        self.highlighted_squares = []
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
                piece = self.game.board[row][col]
                colour = self.original_colors[row][col]
                if piece is None:
                  self.squares[row][col].config(image="", text=" ", bg=colour)
                  self.squares[row][col].image = None
                else:
                  img = self.piece_images[piece.name][piece.colour]
                  self.squares[row][col].config(image=img, text="", bg=colour)
                  self.squares[row][col].image = img


    def open_promotion_popup(self, er, ec, colour):
      popup = tk.Toplevel(self.root)
      popup.geometry("250x100")
      popup.title("Promote Pawn")

      chosen_piece = {"piece": None}

      def choose(piece_class):
        chosen_piece["piece"] = piece_class(colour)
        popup.destroy()

      pieces = [Queen, Rook, Bishop, Knight]

      button_size = (40, 40)
      piece_images = {}
      for piece_class in pieces:
        img_path = f"Pieces/{colour.lower()}-{piece_class.__name__.lower()}.png"
        img = ImageTk.PhotoImage(Image.open(img_path).convert("RGBA").resize(button_size))
        piece_images[piece_class] = img

      for i, piece_class in enumerate(pieces):
        btn = tk.Button(popup, image=piece_images[piece_class],command=lambda p=piece_class: choose(p))
        btn.grid(row=0, column=i, padx=5, pady=20)
                 
        btn.image = piece_images[piece_class]  
        btn.grid(row=0, column=i, padx=5, pady=20)        

      

      popup.update_idletasks()
      popup.grab_set()
      popup.focus_set()
      popup.wait_window()

      return chosen_piece["piece"]
    

    
    def attempt_move(self,start,end):
      result = self.game.move_piece(start, end)

      if isinstance(result, tuple) and result[0] == "promotion_needed":
        er, ec, colour = result[1], result[2], result[3]
        promoted_piece = self.open_promotion_popup(er, ec, colour)
        self.game.board[er][ec] = promoted_piece  # update board manually
        self.update_board()
        return True
      elif result == "move_done" or result is True:
        self.update_board()
        return True
      return False


    def square_clicked(self, row, col):
      print(f"Square clicked:({row}, {col})")
      if self.selected_square is None:
        piece = self.game.board[row][col]
        if piece is not None and piece.colour == self.current_turn:
          self.selected_square = (row, col)
          self.highlight_square(row, col, "#6FC0F2")
          legal_moves = self.game.get_legal_moves_for_square((row, col))
          self.highlight_moves(legal_moves)
          print(f"Selected piece: {piece.name} at ({row},{col}) legal moves: {legal_moves}")
      elif self.selected_square == (row, col):
        self.deselect_square()
      else:
          if self.attempt_move(self.selected_square, (row,col)):
            print(f"moved piece to ({row}, {col})")
            self.current_turn = "black" if self.current_turn == "white" else "white"
          else:
             print("Illegal Move")
          self.deselect_square()

    def highlight_square(self, row, col, highlight_colour):
      self.frames[row][col].config(bg=highlight_colour)
      self.squares[row][col].config(bg=highlight_colour)

    def highlight_moves(self, moves):
       for (r,c) in moves:
          self.frames[r][c].config(bg="#BCE954")
          self.squares[r][c].config(bg="#BCE954")
          self.highlighted_squares.append((r, c))

    def deselect_square(self):
      if self.selected_square:
        row, col = self.selected_square
        original_colour = self.original_colors[row][col]
        self.frames[row][col].config(bg=original_colour)
        self.squares[row][col].config(bg=original_colour)
        self.selected_square = None
      for (r,c) in self.highlighted_squares:
         orig = self.original_colors[r][c]
         self.frames[r][c].config(bg=orig)
         self.squares[r][c].config(bg=orig)
      self.highlighted_squares = []



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess")
    game = Board()
    gui = chessGUI(root, game)
    root.mainloop()

