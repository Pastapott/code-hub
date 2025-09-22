#Imports the pieces from the piece file
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

#creates board class
class Board:
    def __init__(self, setup_default=True):
        #sets all spaces on board to none
        self.board = [[None for _ in range(8)] for _ in range (8)]
        if setup_default:
          self.setup_board()

#setsup board for the start of the game
    def setup_board(self):
        #Black
        self.board[0][0] = Rook("black")
        self.board[0][1] = Knight("black")
        self.board[0][2] = Bishop("black")
        self.board[0][3] = Queen("black")
        self.board[0][4] = King("black")
        self.board[0][5] = Bishop("black")
        self.board[0][6] = Knight("black")
        self.board[0][7] = Rook("black")

        for col in range(8):
          self.board[1][col] = Pawn("black")

            
        #White
        self.board[7][0] = Rook("white")
        self.board[7][1] = Knight("white")
        self.board[7][2] = Bishop("white")
        self.board[7][3] = Queen("white")
        self.board[7][4] = King("white")
        self.board[7][5] = Bishop("white")
        self.board[7][6] = Knight("white")
        self.board[7][7] = Rook("white")

        for col in range(8):
          self.board[6][col] = Pawn("white")

    def copy_board_state(self):
      return [row.copy() for row in self.board]
          
    #function used to always find king, helper to make sure not in check
    def find_king(self, colour, board_state=None):
      if board_state is None:
         board_state = self.board
      for r in range(8):
        for c in range(8):
          piece = board_state[r][c]
          if piece and piece.name == "King" and piece.colour == colour:
             return (r,c)
      return None
    
    def is_in_check(self, colour, board_state=None):
      if board_state is None:
         board_state = self.board
      king_position = self.find_king(colour, board_state)
      if king_position is None:
         return True
      for r in range(8):
        for c in range(8):
           piece = board_state[r][c]
           if piece and piece.colour != colour:
              moves = piece.get_possible_moves((r, c), board_state)
              if king_position in moves:
                 return True
      return False
    
    def get_legal_moves_for_square(self, position):
       r, c = position
       piece = self.board[r][c]
       if piece is None:
          return []
       pseudo = piece.get_possible_moves((r, c), self.board)
       legal = []
       for (er, ec) in pseudo:
          test_board = self.copy_board_state()
          test_board[er][ec] = test_board[r][c]
          test_board[r][c] = None
          moved_piece = test_board[er][ec]
          if moved_piece is not None and moved_piece.name == "Pawn" and (er == 0 or er == 7):
             test_board[er][ec] = Queen(moved_piece.colour)
          if not self.is_in_check(piece.colour, test_board):
             legal.append((er, ec))
       return legal

    def get_all_legal_moves_for_colour(self, colour):
       all_moves = {}
       for r in range(8):
            for c in range(8):
               piece = self.board[r][c]
               if piece is not None and piece == colour:
                 legal = self.get_legal_moves_for_square((r, c))
                 if legal:
                    all_moves[(r, c)] = legal
       return all_moves
    
    def move_piece(self, start, end):
       sr, sc = start
       er, ec = end
       piece = self.board[sr][sc]
       if piece is None:
          return False
       legal_moves = self.get_legal_moves_for_square((sr, sc))
       if (er, ec) not in legal_moves:
          return False
       captured = self.board[er][ec]
       if captured:
          print(f"Captured: {captured.colour} {captured.name} at {(er, ec)}")
       self.board[er][ec] = self.board[sr][sc]
       self.board[sr][sc] = None
       moved_piece = self.board[er][ec]
       if moved_piece.name == "Pawn" and (er == 0 or er == 7):
          self.board[er][ec] = Queen(moved_piece.colour)
          print(f"Pawn promoted to Queen at {(er, ec)}")
       return True