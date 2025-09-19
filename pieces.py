class Piece:
	def __init__(self,colour):
		self.color = colour
		self.name = "Piece"
      
	def get_possible_moves(self, position, board):
		pass

class Pawn(Piece):
	def _init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "Pawn"

	def get_possible_moves(self, position, board):
		moves = []
		row,col = position
		if self.colour == "white":
			direction = -1
			starting_row = 6
		else:
			direction = 1
			starting_row = 1

		if 0 <= row + direction <=7 and board[row + direction][col] is None:
			moves.append((row + direction, col))

		if row == starting_row and board[row + direction][col] is None and board[row + (2 * direction)][col] is None:
			moves.append((row + (2 * direction), col))

		return moves

class Rook(Piece):
	def _init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "Rook"

	def get_possible_moves(self, position, board):
		#rook logic
		return[]
	
class Knight(Piece):
	def _init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "Knight"

	def get_possible_moves(self, position, board):
		#knight logic
		return[]
	
class Bishop(Piece):
	def _init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "Bishop"

	def get_possible_moves(self, position, board):
		#bishop logic
		return[]
	
class Queen(Piece):
	def _init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "Queen"

	def get_possible_moves(self, position, board):
		#queen logic
		return[]
	
class King(Piece):
	def _init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "King"

	def get_possible_moves(self, position, board):
		#king logic
		return[]



    