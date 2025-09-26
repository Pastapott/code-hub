def is_on_board(r, c):
    return 0 <= r <= 7 and 0 <= c <= 7
class Piece:
	def __init__(self,colour):
		self.colour = colour
		self.name = "Piece"
		self.has_moved = False
      
	def get_possible_moves(self, position, board):
		pass

class Pawn(Piece):
	def __init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "Pawn"

	def get_possible_moves(self, position, board, last_move=None):
		moves = []
		row,col = position
		if self.colour == "white":
			direction = -1
			starting_row = 6
			en_passant_row = 3
		else:
			direction = 1
			starting_row = 1
			en_passant_row = 4

		if is_on_board(row + direction, col) and board[row + direction][col] is None:
			moves.append((row + direction, col))

		if row == starting_row and board[row + direction][col] is None and board[row + (2 * direction)][col] is None:
			moves.append((row + (2 * direction), col))

		if is_on_board(row + direction, col -1):
			target = board[row + direction][col - 1]
			if target is not None and target.colour != self.colour:
				moves.append((row + direction, col - 1))

		if is_on_board(row + direction, col + 1):
			target = board[row + direction][col + 1]
			if target is not None and target.colour != self.colour:
				moves.append((row + direction, col + 1))

		if last_move and row == en_passant_row:
			(sr, sc), (er, ec), moved_piece = last_move["start"], last_move["end"], last_move["piece"]
			if moved_piece.name == "Pawn" and abs(er - sr) == 2:
				if er == row and abs(ec - col) == 1:
					moves.append((row + direction, ec))
		return moves

class Rook(Piece):
	def __init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "Rook"

	def get_possible_moves(self, position, board, last_move=None):
		moves = []
		row,col = position
		directions = [(1,0),(-1,0),(0,1),(0,-1)] 
		for dr, dc in directions:
			r = row + dr
			c = col + dc
			while is_on_board(r,c):
				if board[r][c] is None:
					moves.append((r,c))
				elif board[r][c].colour != self.colour:
					moves.append((r,c))
					break
				else:
					break
				r += dr
				c += dc
		return moves

	
class Knight(Piece):
	def __init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "Knight"

	def get_possible_moves(self, position, board, last_move=None):
		moves = []
		row,col = position
		directions = [(2,-1),(2,1),(1,2),(1,-2),(-2,1),(-2,-1),(-1,2),(-1,-2)]
		for dr, dc in directions:
			r = row + dr
			c = col + dc
			if is_on_board(r, c):
				if board[r][c] is None:
					moves.append((r,c))
				elif board[r][c].colour != self.colour:
					moves.append((r,c))
		return moves
	
class Bishop(Piece):
	def __init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "Bishop"

	def get_possible_moves(self, position, board, last_move=None):
		moves = []
		row,col = position
		directions = [(1,1),(1,-1),(-1,1),(-1,-1)]
		for dr, dc in directions:
			r = row + dr
			c = col + dc
			while is_on_board(r,c):
				if board[r][c] is None:
					moves.append((r,c))
				elif board[r][c].colour != self.colour:
					moves.append((r,c))
					break
				else:
					break
				r += dr
				c += dc
		return moves


	
class Queen(Piece):
	def __init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "Queen"

	def get_possible_moves(self, position, board, last_move=None):
		moves = []
		row,col = position
		directions = [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]
		for dr, dc in directions:
			r = row + dr
			c = col + dc
			while is_on_board(r,c):
				if board[r][c] is None:
					moves.append((r,c))
				elif board[r][c].colour != self.colour:
					moves.append((r,c))
					break
				else:
					break
				r += dr
				c += dc
		return moves
	
class King(Piece):
	def __init__(self,colour):
		Piece.__init__(self, colour)
		self.name = "King"

	def get_possible_moves(self, position, board, last_move=None):
		moves = []
		row,col = position
		directions = [(1,0),(-1,0),(0,-1),(0,1),(1,1),(1,-1),(-1,1),(-1,-1)]
		for dr, dc in directions:
			r = row + dr
			c = col + dc
			if is_on_board(r,c):
				if board[r][c] is None or board[r][c].colour != self.colour:
					moves.append((r,c))
		return moves
			