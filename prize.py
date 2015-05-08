import random
random.seed()

boardSize = 150

class prize(object):
	def __init__(self):
		self.x = random.uniform(0,boardSize)

		self.y = random.uniform(0,boardSize)