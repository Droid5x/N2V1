from neural import *
from prize import *
from neuralActor import *

boardSize = 1000

class geneticAlgorithm(object):
	epoch = 0
	def __init__(self, number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs, number_of_actors, num_targets):
		self.hidden_layers = number_of_hidden_layers

		self.hidden_size = size_of_hidden_layers

		self.input_size = num_inputs

		self.output_size = num_outputs

		self.number_of_actors = number_of_actors

		self.actors = []

		for i in range(0, number_of_actors):

			self.actors.append(neuralActor(number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs))

		self.generations_simulated = 0

		self.prizes = []

		for i in range(num_targets):

			self.prizes.append(prize())
			#going to need to avoid duplicate prizes in the same location...

	# replaces worst 50% of networks with children from the best 50% and mutates the top 50%
	def makeChildNetworks(self):
		#sort the actors by their scores
		self.actors.sort(key=lambda x: x.score, reverse = 1)

		temp = self.actors[0:int(math.floor(self.number_of_actors/2))]

		weights = []

		maxScore = self.actors[0].score

		minScore = self.actors[-1].score

		totalScorers = 0

		totalScore = 0.0

		for actor in self.actors:

			if actor.score > 0:

				totalScorers += 1

				totalScore += actor.score

		for actor in temp:

			actor.mutate()

		for i in range(self.number_of_actors - len(temp)):

			# make a new temporary actor for when new ones are created
			newActor = neuralActor(self.hidden_layers, self.hidden_size, self.input_size, self.output_size)

			weights = recombineWeights(self.actors[0].getWeights(), self.actors[i].getWeights())

			newActor.network.replaceWeights(weights)

			temp.append(newActor)

		if len(temp) != self.number_of_actors:

			print("ERROR: We don't have as many actors as we started with!!!\n")

		self.actors = temp[:]

		return (maxScore, minScore, totalScore, totalScorers, totalScore/len(self.actors))

	# simulate an epoch of 1000 ticks (iterations)
	def runEpoch(self):
		self.epoch += 1

		ticks = 0

		while ticks <= 1000:

			for actor in self.actors:

				# run the actor
				k = actor.runActor(self.prizes)

				if k:

					self.prizes.pop(k)

					#add a new prize since one was taken
					self.prizes.append(prize())

			ticks+=1

		#now that the simulation has ended, find the average score, maximum score, and minimum score
		results = self.makeChildNetworks()

		print("Epoch " + str(self.epoch) + ":\n")

		print("Best Score: " + str(results[0]))

		print("Worst Score: " + str(results[1]))

		print("Total Score: " + str(results[2]))

		print("Total Actors Who Scored: " + str(results[3]))

		print("Average Score: " + str(results[4]) + '\n')


def recombineWeights(weights1, weights2):
	new_weights = []

	value = 0.0

	if len(weights1) != len(weights2):

		raise ValueError("We have a problem here! The networks are different!")

	for i in range(len(weights1)):

		value = random.random()

		new_weights.append(value*weights1[i] + (1-value)*weights2[i])

	return new_weights




