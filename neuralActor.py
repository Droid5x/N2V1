import random
import math
from params import *
from neural import *

# A wrapper class for the neural networks so they can function in the simulation
class neuralActor(object):
	def __init__(self, number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs):
		self.network = neuralNet(number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs)

		self.score = 0

		# x and y coordinates
		self.x = random.uniform(0,boardSize)

		self.y = random.uniform(0,boardSize)

		# rotation in radians and components
		self.rotation = 2 * math.pi * random.random()

		self.look_x = -math.sin(self.rotation)

		self.look_y = math.cos(self.rotation)

		# Right and left side velocities
		self.r_velocity = 0.16

		self.l_velocity = 0.16

	# Reset the positional data of the actor, and the score
	def reset():
		self.score = 0

		self.x = random.uniform(0,boardSize)

		self.y = random.uniform(0,boardSize)

		self.rotation = 2 * math.pi * random.random()

	# run the actor given the rotation vector and the position of the nearest prize
	def runActor(self, prizes):
		# get index of closest prize
		k = self.closestPrize(prizes)

		# retrieve the coords of the closest prize
		temp_x = float(prizes[k].x)

		temp_y = float(prizes[k].y)

		# normalize the vector
		norm = math.sqrt(prizes[k].x**2 + prizes[k].y**2)

		temp_x /= norm

		temp_y /= norm

		inputs = [temp_x, temp_y, self.look_x, self.look_y]

		# run the network
		outputs = self.network.runNetwork(inputs)

		# from here, we are just updating positional data and determining if the actor got the prize
		self.r_velocity = outputs[0]

		self.l_velocity = outputs[1]

		rotation_velocity = self.l_velocity - self.r_velocity

		# bounding
		if rotation_velocity > max_rotational_velocity:

			rotation_velocity = max_rotational_velocity

		elif rotation_velocity < -1 * max_rotational_velocity:

			rotation_velocity = -1 * max_rotational_velocity

		self.rotation += rotation_velocity

		linear_velocity = self.l_velocity + self.r_velocity

		# more bounding logic
		if linear_velocity > max_linear_velocity:

			linear_velocity = max_linear_velocity

		elif linear_velocity < -1 * max_linear_velocity:

			linear_velocity = -1 * max_linear_velocity

		self.look_x = -math.sin(self.rotation)

		self.look_y = math.cos(self.rotation)

		self.x += self.look_x * linear_velocity

		self.y += self.look_y * linear_velocity

		self.x += self.look_x

		self.y += self.look_y

		# and more bounding!
		if self.x < 0:

			self.x = boardSize

		elif self.x > boardSize:
			self.x = 0

		if self.y < 0:

			self.y = boardSize

		if self.y > boardSize:

			self.y = 0

		# return the index of the prize if the actor found it
		if math.sqrt(abs(self.x - prizes[k].x)**2 + abs(self.y - prizes[k].y)**2) < target_size + actor_size:

			return k

		return -1

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

	# mutate the weights in the actor based on user's parameters
	def mutate(self):
		temp = self.getWeights()

		for weight in temp:

			if random.random() <= mutation_prob:

				weight += random.uniform(-1,1) * max_mutation

		self.network.replaceWeights(temp)

		self.score = 0

		if temp != self.getWeights():

			print("ERROR: weights did not properly update!")

