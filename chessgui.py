#imports tkinter into file
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
#imports Board class from board fil
from board import Board
from PIL import Image, ImageTk
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from resize_manager import ResizeManager
from datetime import datetime
import os
import pygame

#class for the display
class chessGUI(ctk.CTkFrame):
    def __init__(self, parent, game: Board, controller=None, window_size=(1000, 700), sidebar_width=260):
        super().__init__(parent, fg_color="transparent")
        self.game = game
        self.controller = controller

        self.board_frame = tk.Frame(self, bg="#EEEED2")
        self.sidebar_width = sidebar_width
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", width=self.sidebar_width)

        self.board_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid(row=0, column=1, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.frames = [[None for _ in range(8)] for _ in range(8)]
        self.selected_square = None
        self.original_colors = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = "white"
        self.highlighted_squares = []
        self.move_history = []
        self.redo_history = []
        self.white_time = 600
        self.black_time = 600
        self.timer_running = True
        self.timer_job = None

        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound("sounds/move-self.mp3")
        self.capture_sound = pygame.mixer.Sound("sounds/capture.mp3")
        self.check_sound = pygame.mixer.Sound("sounds/check.mp3")
        self.game_end_sound = pygame.mixer.Sound("sounds/game-end.wav")
        self.game_start_sound = pygame.mixer.Sound("sounds/game-start.mp3")
        self.promote_sound = pygame.mixer.Sound("sounds/promote.mp3")
        self.illegal_sound = pygame.mixer.Sound("sounds/illegal.mp3")
        self.settings_icon = CTkImage(Image.open("icons/settings.png"),size=(30, 30))
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
        root_window = self.winfo_toplevel()
        self.resize_manager = ResizeManager(
          root=root_window,
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
        self.game_start_sound.play()
        self.after(100, lambda: self.update_board(preserve_highlights=False))
        self.start_timer_loop()

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
      ctk.CTkLabel(self.sidebar_frame, text="Settings", text_color="white").pack(pady=10)
      ctk.CTkButton(self.sidebar_frame,image=self.settings_icon,text = "", fg_color="transparent",hover_color="#3c3c3c", width=20,height=20, command=lambda: self.controller.show_frame("Settings") if self.controller else None).pack(side="bottom", anchor="w", padx=10, pady=10)


      self.move_history_box = ctk.CTkTextbox(
        self.sidebar_frame,
        width=200,
        height=300,
        corner_radius=10
      )
      self.move_history_box.pack(pady=10, padx=10, fill="both", expand=True)
      self.move_history_box.configure(state="disabled")


      self.white_timer_label = ctk.CTkLabel(self.sidebar_frame, text="White: 05:00", text_color="white")
      self.white_timer_label.pack(pady=5)

      self.black_timer_label = ctk.CTkLabel(self.sidebar_frame, text="Black: 05:00", text_color="white")
      self.black_timer_label.pack(pady=5)

      navigate_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
      navigate_frame.pack(side="bottom", pady=20)

      back_button = ctk.CTkButton(navigate_frame, text="<", width=40, fg_color="transparent",command=self.undo_move)
      back_button.grid(row=0, column=0, padx=15)

      back_label = ctk.CTkLabel(navigate_frame, text="back")
      back_label.grid(row=1, column=0)

      forward_button = ctk.CTkButton(navigate_frame, text=">", width=40, fg_color="transparent", command=self.redo_move)
      forward_button.grid(row=0, column=1, padx=15)

      forward_label = ctk.CTkLabel(navigate_frame, text="forward")
      forward_label.grid(row=1, column=1)

      ctk.CTkButton(self.sidebar_frame, text="Reset Board", command=self.reset_board).pack(pady=10)

    
    def reset_sidebar(self):
    # Clear the sidebar
      for widget in self.sidebar_frame.winfo_children():
        widget.destroy()
      # Rebuild the default sidebar
      self.create_sidebar()

    def update_timer(self):
      if not self.timer_running:
        return
      
      if self.current_turn == "white":
         self.white_time -=1
         if self.white_time <=0:
            self.end_game("Black wins on time")
            return
      else:
         self.black_time -=1
         if self.black_time <= 0:
            self.end_game("White wins on time")
            return
         
      self.white_timer_label.configure(text=(f"white: {self.format_time(self.white_time)}"))
      self.black_timer_label.configure(text=(f"black: {self.format_time(self.black_time)}"))

      self.timer_job = self.after(1000, self.update_timer)

    def format_time(self,seconds):
       m, s = divmod(max(0, seconds), 60)
       return (f"{m:02d}:{s:02d}")

      



    def reset_board(self):
      self.game.reset_board()
      self.move_history = []
      self.redo_history = []
      self.current_turn = "white"
      self.white_time = 600
      self.black_time = 600
      self.timer_running = True
      self.start_timer_loop()
      self.update_board()
      self.reset_sidebar()
      self.move_history_box.delete("1.0", "end")

    def undo_move(self):
      if self.game.undo_last_move():
          if self.move_history:
            undone = self.move_history.pop()  
            self.redo_history.append(undone)

            self.move_history_box.configure(state="normal")
            self.move_history_box.delete("1.0", "end")
            for i, move in enumerate(self.move_history, 1):
                self.move_history_box.insert("end", f"{i}. {move}\n")
            self.move_history_box.configure(state="disabled")
          self.current_turn = "black" if self.current_turn == "white" else "white"
          self.update_board()

    def redo_move(self):
        if not self.redo_history:
           return

        expected_turn = "white" if len(self.move_history) % 2 == 0 else "black"
        if self.current_turn != expected_turn:
           return

        if self.game.redo_last_move():
          redone = self.redo_history.pop()
          self.move_history.append(redone)
          self.move_history_box.configure(state="normal")
          self.move_history_box.delete("1.0", "end")
          for i, move in enumerate(self.move_history, 1):
            self.move_history_box.insert("end", f"{i}. {move}\n")
          self.move_history_box.configure(state="disabled")

        self.current_turn = "black" if self.current_turn == "white" else "white"
        self.update_board()

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
      popup = tk.Toplevel(self.winfo_toplevel())
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
    
    def start_timer_loop(self):
      if self.timer_job is not None:
          try:
              self.after_cancel(self.timer_job)
          except Exception:
              pass
      self.timer_job = self.after(1000, self.update_timer)

    def stop_timer_loop(self):
      if self.timer_job is not None:
          try:
              self.after_cancel(self.timer_job)
          except Exception:
              pass
      self.timer_job = None
    
    def attempt_move(self,start,end):
      piece = self.game.board[start[0]][start[1]]
      result = self.game.move_piece(start, end)
      sound_to_play = None
      if isinstance(result, tuple) and result[0] == "promotion_needed":
        er, ec, colour = result[1], result[2], result[3]
        promoted_piece = self.open_promotion_popup(er, ec, colour)
        self.game.board[er][ec] = promoted_piece  
        sound_to_play = self.promote_sound
        result = "move_done"

      if result == "move_done" or result is True:
        self.update_board()
        #log moves
        move_notation = self.get_move_notation(start, end, piece)
        self.move_history.append(move_notation)
        self.redo_history.clear()
        self.move_history_box.configure(state="normal")
        self.move_history_box.insert("end", f"{len(self.move_history)}. {move_notation}\n")
        self.move_history_box.see("end")
        self.move_history_box.configure(state="disabled")

        last_move = getattr(self.game, "last_move", {})
        if sound_to_play is None:
          if last_move.get("captured"):
              sound_to_play = self.capture_sound
          else:
              sound_to_play = self.move_sound


        self.current_turn = "black" if self.current_turn == "white" else "white"

        if self.game.is_checkmate(self.current_turn):
          sound_to_play = self.game_end_sound
          result = (f"Checkmate! { 'White' if self.current_turn == 'black' else 'Black' } wins.")
          print(result)
          self.end_game(result)
        elif self.game.is_stalemate(self.current_turn):
          result = ("Stalemate! It's a draw.")
          print(result)
          self.end_game(result)
        elif self.game.is_in_check(self.current_turn):   
           if sound_to_play not in [self.promote_sound, self.game_end_sound]:
              sound_to_play = self.check_sound
        if sound_to_play:
            sound_to_play.play()
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
             self.illegal_sound.play()
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
      self.timer_running = False
      self.stop_timer_loop()
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

#TODO
#Create a start screen with options to play new game, Load Saved Game and Quit Game
#Create settings page, diff board, diff pieces, sound on/off, timer options
#Bots & PVP