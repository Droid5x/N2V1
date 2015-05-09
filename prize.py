import random
random.seed()
from params import *

class prize(object):
	def __init__(self):
		self.x = random.uniform(0,boardSize)

		self.y = random.uniform(0,boardSize)