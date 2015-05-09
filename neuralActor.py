import random
import math
from params import *
from neural import *


class neuralActor(object):
	def __init__(self, number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs):
		self.network = neuralNet(number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs)

		self.score = 0

		self.x = random.uniform(0,boardSize)

		self.y = random.uniform(0,boardSize)

		self.rotation = 2 * math.pi * random.random()

		self.r_velocity = 0.16

		self.l_velocity = 0.16

		self.look_x = -math.sin(self.rotation)

		self.look_y = math.cos(self.rotation)

	def reset():
		self.score = 0

		self.x = boardSize * random.random()

		self.y = boardSize * random.random()

		self.rotation = 2 * math.pi * random.random()

	def runActor(self, prizes):
		k = self.closestPrize(prizes)

		temp_x = float(prizes[k].x)

		temp_y = float(prizes[k].y)

		norm = math.sqrt(prizes[k].x**2 + prizes[k].y**2)

		temp_x /= norm

		temp_y /= norm

		inputs = [temp_x, temp_y, self.look_x, self.look_y]

		outputs = self.network.runNetwork(inputs)

		self.r_velocity = outputs[0]

		self.l_velocity = outputs[1]

		rotation_velocity = self.l_velocity - self.r_velocity

		if rotation_velocity > math.pi:

			rotation_velocity = math.pi

		self.rotation += rotation_velocity

		linear_velocity = self.l_velocity + self.r_velocity

		self.look_x = -math.sin(self.rotation)

		self.look_y = math.cos(self.rotation)

		self.x += self.look_x * linear_velocity

		self.y += self.look_y * linear_velocity

		self.x += self.look_x

		self.y += self.look_y

		if self.x < 0:

			self.x = boardSize

		elif self.x > boardSize:

			self.x = 0

		if self.y < 0:

			self.y = boardSize

		if self.y > boardSize:

			self.y = 0

		if math.sqrt(abs(self.x - prizes[k].x)**2 + abs(self.y - prizes[k].y)**2) < target_size:

			print("I found a prize! :D")

			self.score += 1

			return k

		return 0

	def getWeights(self):
		self.network.updateWeightsList()

		return self.network.weights

	def changeWeights(self, weights):
		self.network.replaceWeights(weights)

	def getLocation(self):
		return (self.x, self.y)

	def closestPrize(self, prizes): # takes list of all "prizes" (each has an x and y coord)
	# returns index of closest prize
		dist = []

		minVal = 0

		indexVal = 0

		for prize in prizes:

			dist.append(math.sqrt(abs(self.x - prize.x)**2 + abs(self.y - prize.y)**2))

		for i in range(len(dist)):

			if dist[i] < minVal:

				minVal = dist[i]

				indexVal = i

		return indexVal

	def mutate(self):
		temp = self.getWeights()

		for weight in temp:

			if random.random() <= mutation_prob:

				weight += random.random() * max_mutation

		self.network.replaceWeights(temp)

		self.score = 0

		if temp != self.getWeights():

			print("ERROR: weights did not properly update!")

