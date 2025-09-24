# Imports the pieces from the piece file
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

# creates board class
class Board:
    def __init__(self, setup_default=True):
        # sets all spaces on board to none
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.last_move = None     
        self.move_stack = [] 
        if setup_default:
            self.setup_board()

    # sets up board for the start of the game
    def setup_board(self):
        # Black
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

        # White
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

    # function used to always find king, helper to make sure not in check
    def find_king(self, colour, board_state=None):
        if board_state is None:
            board_state = self.board
        for r in range(8):
            for c in range(8):
                piece = board_state[r][c]
                if piece and piece.name == "King" and piece.colour == colour:
                    return (r, c)
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

    def is_checkmate(self, colour):
        if not self.is_in_check(colour):
            return False
        all_moves = self.get_all_legal_moves_for_colour(colour)
        return len(all_moves) == 0

    def is_stalemate(self, colour):
        if self.is_in_check(colour):
            return False
        all_moves = self.get_all_legal_moves_for_colour(colour)
        return len(all_moves) == 0

    def get_legal_moves_for_square(self, position):
        r, c = position
        piece = self.board[r][c]
        if piece is None:
            return []
        pseudo = piece.get_possible_moves((r, c), self.board, getattr(self, "last_move", None))
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

        if piece.name == "King":
            if not self.is_in_check(piece.colour):
                row = r
                if self.can_castle_kingside(piece.colour):
                    legal.append((row, 6))
                if self.can_castle_queenside(piece.colour):
                    legal.append((row, 2))
        return legal

    def get_all_legal_moves_for_colour(self, colour):
        all_moves = {}
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece is not None and piece.colour == colour:
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

        captured = None
        castling_flag = None
        en_passant_flag = False

        # Castling
        if piece.name == "King" and abs(ec - sc) == 2:
            row = sr
            if ec == 6:
                self.board[row][5] = self.board[row][7]
                self.board[row][7] = None
                self.board[row][5].has_moved = True
                castling_flag = "O-O"
            elif ec == 2:
                self.board[row][3] = self.board[row][0]
                self.board[row][0] = None
                self.board[row][3].has_moved = True
                castling_flag = "O-O-O"
        else:
            captured = self.board[er][ec]

            if piece.name == "Pawn":
                ep_captured = self._handle_en_passant(sr, sc, er, ec)
                if ep_captured:
                    captured = ep_captured
                    en_passant_flag = True

            if captured:
                print(f"Captured: {captured.colour} {captured.name} at {(er, ec)}")

        # Move the piece
        self.board[er][ec] = self.board[sr][sc]
        self.board[sr][sc] = None
        moved_piece = self.board[er][ec]
        moved_piece.has_moved = True

        # Save move info
        self.last_move = {
            "start": (sr, sc),
            "end": (er, ec),
            "piece": moved_piece,
            "captured": captured,
            "promotion": (moved_piece.name == "Pawn" and (er == 0 or er == 7)),
            "castling": castling_flag,
            "en_passant": en_passant_flag,
        }

        if moved_piece.name == "Pawn" and (er == 0 or er == 7):
            return "promotion_needed", er, ec, moved_piece.colour
        else:
            return "move_done"

    def _handle_en_passant(self, sr, sc, er, ec):
        if not self.last_move:
            return None

        (sr_last, sc_last), (er_last, ec_last), moved_piece = \
            self.last_move["start"], self.last_move["end"], self.last_move["piece"]

        if moved_piece.name == "Pawn" and abs(er_last - sr_last) == 2:
            capturing_pawn = self.board[sr][sc]
            if not capturing_pawn:
                return None
            direction = -1 if capturing_pawn.colour == "white" else 1
            if abs(ec - sc) == 1 and er == sr + direction:
                captured_piece = self.board[er_last][ec_last]
                self.board[er_last][ec_last] = None
                return captured_piece
        return None

    def can_castle_kingside(self, colour):
        row = 7 if colour == "white" else 0
        king = self.board[row][4]
        rook = self.board[row][7]
        if not king or not rook:
            return False
        if king.has_moved or rook.has_moved:
            return False
        if self.board[row][5] or self.board[row][6]:
            return False
        for col in [4, 5, 6]:
            if self.square_under_attack((row, col), colour):
                return False
        return True

    def can_castle_queenside(self, colour):
        row = 7 if colour == "white" else 0
        king = self.board[row][4]
        rook = self.board[row][0]
        if not king or not rook:
            return False
        if king.has_moved or rook.has_moved:
            return False
        if self.board[row][1] or self.board[row][2] or self.board[row][3]:
            return False
        for col in [4, 3, 2]:
            if self.square_under_attack((row, col), colour):
                return False
        return True

    def square_under_attack(self, position, colour):
        r, c = position
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.colour != colour:
                    if position in piece.get_possible_moves((row, col), self.board):
                        return True
        return False