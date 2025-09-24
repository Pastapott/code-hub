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
				





## TESTING CODE 


board = [[None for _ in range(8)] for _ in range(8)]

board[6][0] = Pawn("white")        
board[0][0] = Rook("black")        
board[0][1] = Knight("black")      
board[0][2] = Bishop("black")      
board[0][3] = Queen("black")       
board[0][4] = King("black")        

# Test pawn
pawn = board[6][0]
pawn_moves = pawn.get_possible_moves((6,0), board)
print(f"White pawn moves from (6,0): {pawn_moves}")

# Test rook
rook = board[0][0]
rook_moves = rook.get_possible_moves((0,0), board)
print(f"Black rook moves from (0,0): {rook_moves}")

# Test knight
knight = board[0][1]
knight_moves = knight.get_possible_moves((0,1), board)
print(f"Black knight moves from (0,1): {knight_moves}")

# Test bishop
bishop = board[0][2]
bishop_moves = bishop.get_possible_moves((0,2), board)
print(f"Black bishop moves from (0,2): {bishop_moves}")

# Test queen
queen = board[0][3]
queen_moves = queen.get_possible_moves((0,3), board)
print(f"Black queen moves from (0,3): {queen_moves}")

# Test king
king = board[0][4]
king_moves = king.get_possible_moves((0,4), board)
print(f"Black king moves from (0,4): {king_moves}")
