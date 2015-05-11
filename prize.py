import random
random.seed()
from params import *

# Just a small class to describe the class objects

class prize(object):
	def __init__(self):
		self.x = random.uniform(0,boardSize)

		self.y = random.uniform(0,boardSize)