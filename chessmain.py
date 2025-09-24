#imports tkinter into file
import tkinter as tk
#imports Board class from board fil
from board import Board
from PIL import Image, ImageTk
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from resize_manager import ResizeManager
from datetime import datetime
import os

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
        self.move_history = []
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
    
    def reset_sidebar(self):
    # Clear the sidebar
      for widget in self.sidebar_frame.winfo_children():
        widget.destroy()
      # Rebuild the default sidebar
      self.create_sidebar()

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
      piece = self.game.board[start[0]][start[1]]
      result = self.game.move_piece(start, end)
      if isinstance(result, tuple) and result[0] == "promotion_needed":
        er, ec, colour = result[1], result[2], result[3]
        promoted_piece = self.open_promotion_popup(er, ec, colour)
        self.game.board[er][ec] = promoted_piece  
        result = "move_done"

      if result == "move_done" or result is True:
        self.update_board()
        #log moves
        move_notation = self.get_move_notation(start, end, piece)
        self.move_history.append(move_notation)

        self.current_turn = "black" if self.current_turn == "white" else "white"

        if self.game.is_checkmate(self.current_turn):
          result = (f"Checkmate! { 'White' if self.current_turn == 'black' else 'Black' } wins.")
          print(result)
          self.end_game(result)
        elif self.game.is_stalemate(self.current_turn):
          result = ("Stalemate! It's a draw.")
          print(result)
          self.end_game(result)
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

    def get_move_notation(self,start,end,piece):
      files = "abcdefgh"
      ranks = "87654321"

      sr, sc = start
      er, ec = end

      lm = getattr(self.game, "last_move", {}) or {}
      is_castling = lm.get("castling")
      is_ep = lm.get("en_passant", False)
      did_promote = lm.get("promotion", False)
      captured = lm.get("captured")

      start_sq = files[sc] + ranks[sr]
      end_sq = files[ec] + ranks[er]

      if is_castling in ("O-O", "O-O-O"):
        return is_castling
      if piece.name == "Pawn":
         symbol = ""
      elif piece.name == "Knight":
         symbol = "N"
      else:
         symbol = piece.name[0].upper()

      if is_ep and piece.name == "Pawn":
        pawn_file = files[sc]
        return f"{pawn_file}x{end_sq} e.p."
      
      if did_promote and piece.name == "Pawn":
        promoted_piece = self.game.board[er][ec]
        promo_map = {
            "Queen": "Q",
            "Rook": "R",
            "Bishop": "B",
            "Knight": "N",
        }
        promo_symbol = promo_map.get(getattr(promoted_piece, "name", ""), "Q")
        
        if captured:
            pawn_file = files[sc]
            return f"{pawn_file}x{end_sq}={promo_symbol}"
        else:
            pawn_file = files[sc]
            rank = ranks[er]
            return f"{pawn_file}{rank}={promo_symbol}"

      if captured:
        return f"{symbol}{start_sq}x{end_sq}"
      else:
        return f"{symbol}{start_sq}->{end_sq}"
    
    def end_game(self, result):
      for widget in self.sidebar_frame.winfo_children():
        widget.destroy()

      msg = (f"Game ended by {result}.\nWould you like to save this game?")
      tk.Label(self.sidebar_frame, text=msg, bg="#2b2b2b", fg="white", wraplength=200).pack(pady=10)

      name_frame = tk.Frame(self.sidebar_frame, bg="#2b2b2b")
      name_frame.pack(pady=5)
      tk.Label(name_frame, text="Save as:", bg="#2b2b2b", fg="white").pack(side="left", padx=5)
      name_entry = tk.Entry(name_frame)
      name_entry.pack(side="left", padx=5)


      def save_game():
        os.makedirs("saved_games", exist_ok=True)

        custom_name = name_entry.get().strip()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

        if custom_name:
          filename = (f"{timestamp}_{custom_name}.txt")
        else:
          filename = f"{timestamp}.txt"
        path = os.path.join("saved_games", filename)  

        with open(path, "w") as f:
          for i, move in enumerate(self.move_history, 1):
            f.write(f"{i}. {move}\n")
          f.write(f"\nResult: {result}\n")
        print(f"Game saved to {path}")
        self.reset_sidebar()

      btn_frame = tk.Frame(self.sidebar_frame, bg="#2b2b2b")
      btn_frame.pack(pady=10)

      tk.Button(btn_frame, text="Yes", command=save_game).pack(side="left", padx=20, pady=20)
      tk.Button(btn_frame, text="No", command=self.reset_sidebar).pack(side="right", padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess")
    game = Board()
    gui = chessGUI(root, game)
    root.mainloop()

