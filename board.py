#Imports the pieces from the piece file
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

#creates board class
class Board:
    def __init__(self):
        #sets all spaces on board to none
        self.board = [[None for _ in range(8)] for _ in range (8)]
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
            