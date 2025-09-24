#imports tkinter into file
import tkinter as tk
#imports Board class from board fil
from board import Board
from PIL import Image, ImageTk
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from resize_manager import ResizeManager

#class for the display
class chessGUI:
    def __init__(self, root, game: Board,window_size=(1000, 700), sidebar_width=260):
        self.root = root
        self.game = game

        self.root.title("Chess")
        self.root.geometry(f"{window_size[0]}x{window_size[1]}")
        self.root.minsize(700,500)

    
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.board_frame = tk.Frame(self.main_frame, bg="#EEEED2")
        self.sidebar_width = sidebar_width
        self.sidebar_frame = tk.Frame(self.main_frame, bg="#2b2b2b", width=self.sidebar_width)

        self.board_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid(row=0, column=1, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=4)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.frames = [[None for _ in range(8)] for _ in range(8)]
        self.selected_square = None
        self.original_colors = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = "white"
        self.highlighted_squares = []
        self.piece_images = {
            "Pawn": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-pawn.png").convert("RGBA")),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-pawn.png").convert("RGBA")),
            },
            "Rook": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-rook.png").convert("RGBA")),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-rook.png").convert("RGBA")),
            },
            "Knight": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-knight.png").convert("RGBA")),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-knight.png").convert("RGBA")),
            },
            "Bishop": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-bishop.png").convert("RGBA")),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-bishop.png").convert("RGBA")),
            },
            "Queen": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-queen.png").convert("RGBA")),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-queen.png").convert("RGBA")),
            },
            "King": {
                "white": ImageTk.PhotoImage(Image.open("Pieces/white-king.png").convert("RGBA")),
                "black": ImageTk.PhotoImage(Image.open("Pieces/black-king.png").convert("RGBA")),
            }
        }
        self.resize_manager = ResizeManager(
          root=self.root,
          board_frame=self.board_frame,
          sidebar_frame=self.sidebar_frame,
          squares=self.squares,
          original_colors=self.original_colors,
          piece_images=self.piece_images,
          update_callback=self.update_board
        )

        self.create_board()
        self.create_sidebar()
        self._last_size = (0, 0)
        self.root.after(100, lambda: self.update_board(preserve_highlights=False))

    def create_board(self):
        #Displays the chessboard and starting pieces
        for row in range(8):
            for col in range(8):
                #alternate square colours
                colour = "#EEEED2" if (row + col) % 2 == 0 else "#769656"
                self.original_colors[row][col] = colour

                frame = tk.Frame(
                    self.board_frame,
                    bg = colour,
                    highlightbackground = "black",
                    highlightthickness = 1
                )
                frame.grid(row=row, column=col, sticky="nsew")  # <-- needed
                self.frames[row][col] = frame

                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=1)

                label = tk.Label(frame, bg = colour)
                label.grid(row=0, column=0, sticky="nsew")
                self.squares[row][col] = label

                frame.bind("<Button-1>", lambda event, r=row, c=col: self.square_clicked(r, c))
                label.bind("<Button-1>", lambda event, r=row, c=col: self.square_clicked(r, c))

        for i in range(8):
           self.board_frame.grid_rowconfigure(i, weight=1)
           self.board_frame.grid_columnconfigure(i, weight=1)

        self.update_board()
        self.resize_manager.initialized = True


    def create_sidebar(self):
      tk.Label(self.sidebar_frame, text="Settings", bg="#2b2b2b", fg="white").pack(pady=10)
      tk.Button(self.sidebar_frame, text="Undo Move").pack(pady=5)
      tk.Button(self.sidebar_frame, text="Reset Board").pack(pady=5)

    def update_board(self, preserve_highlights=False):
        #update board to match positions
      board_size = min(self.board_frame.winfo_width(), self.board_frame.winfo_height())
      cell_size = board_size // 8

      for row in range(8):
        for col in range(8):
            piece = self.game.board[row][col]
            self.resize_manager.resize_piece(row, col, piece, cell_size)

      if preserve_highlights:
        if self.selected_square:
            r, c = self.selected_square
            self.highlight_square(r, c, "#6FC0F2")
        for (r, c) in self.highlighted_squares:
            self.frames[r][c].config(bg="#BCE954")
            self.squares[r][c].config(bg="#BCE954")


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

