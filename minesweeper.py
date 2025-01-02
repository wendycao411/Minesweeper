import tile
import random

class Minesweeper:
	def __init__(self, difficulty):
		if (difficulty == "easy"):
			self.rows = 8
			self.cols = 8
			self.mines = 10
		elif (difficulty == "medium"):
			self.rows = 16
			self.cols = 16
			self.mines = 40
		else:
			self.rows = 16
			self.cols = 30
			self.mines = 99
		self.remaining_flags = self.mines

		#make grid
		self.grid = [[tile.Tile() for col in range(self.cols)] for row in range(self.rows)]
		self.swept = 0

	def check_for_win(self):
		return self.swept == self.rows * self.cols - self.mines
	
	def place_mines(self, row, col):
		placed_mines = 0
		while placed_mines < self.mines:
			#generate random location
			rand_row = random.randint(0, self.rows - 1)
			rand_col = random.randint(0, self.cols - 1)
			#temporary print info for test
			print(placed_mines, rand_row, rand_col)
			#check if location is not near the click or already a mine
			if not (row - 1 <= rand_row <= row + 1 and col -1 <= rand_col <= col + 1) and not self.grid[rand_row][rand_col].mine:
				self.grid[rand_row][rand_col].mine = True
				placed_mines += 1
				#increase the count of nearby mines for nearby tiles
				for r in range (rand_row - 1, rand_row + 2):
					if 0 <= r < self.rows:
						for c in range(rand_col - 1, rand_col + 2):
							if 0 <= c < self.cols:
								self.grid[r][c].nearby_mines += 1

			
	def sweep(self, row, col):
		if self.swept == 0:
			self.place_mines(row, col)
		tile = self.grid[row][col]
		if not tile.flagged and not tile.visible:
			tile.visible = True
			self.swept += 1
			if tile.mine:
				return True
			if tile.nearby_mines ==0:
				for r in range(row-1, row+2):
					if 0 <= r < self.rows:
						for c in range(col-1, col + 2):
							if 0 <= c < self.cols:
								self.sweep(r,c)

	def flag(self,row,col):
		if self.swept > 0:
			tile = self.grid[row][col]
			if not tile.visible:
				tile.flag()
				if tile.flagged:
					self.remaining_flags -= 1
				else:
					self.remaining_flags += 1
		print(self.remaining_flags)
						
	#more to come
			
	#temporary print function
	def print(self):
		for row in range(self.rows):
			for col in range(self.cols):
				print(row, col)
				self.grid[row][col].print()
				





			