class Tile:
	def __init__(self):
		self.mine = False
		self.flagged = False
		self.visible = False 
		self.nearby_mines = 0
	def flag(self):
		if not self.visible:
			self.flagged = not self.flagged
	def sweep(self):
		if self.flagged:
			return -2
		self.visible = True 
		if self.mine: 
			return -1
		return self.nearby_mines

	def print(self):
		print(self.mine, self.flagged, self.visible, self.nearby_mines)

		
