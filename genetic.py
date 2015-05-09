from neural import *
from prize import *
from params import *
from neuralActor import *

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

		if math.floor(self.number_of_actors/2) % 2 != 0:

			temp = self.actors[0:int(math.floor(self.number_of_actors/2))+1]

		else:

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

		i = 0 

		j = 1

		while(len(temp) < len(self.actors)):

			# make a new temporary actor for when new ones are created
			newActor = neuralActor(self.hidden_layers, self.hidden_size, self.input_size, self.output_size)

			weights_list = recombineWeights(self.actors[i].getWeights(), self.actors[j].getWeights())

			newActor.network.replaceWeights(weights_list[0])

			temp.append(newActor)

			newActor = neuralActor(self.hidden_layers, self.hidden_size, self.input_size, self.output_size)

			newActor.network.replaceWeights(weights_list[1])

			temp.append(newActor)

			i += 1

			j += 1

		if len(temp) != self.number_of_actors:

			print("ERROR: We don't have as many actors as we started with!!!\n")

		for actor in temp:

			actor.mutate()

		self.actors = temp[:]

		return (maxScore, minScore, totalScore, totalScorers, totalScore/len(self.actors))

	# simulate an epoch of 1000 ticks (iterations)
	def runEpoch(self):
		self.epoch += 1

		ticks = 0

		while ticks <= max_ticks:

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
	new_weights1 = []

	new_weights2 = []

	switch = random.randint(0, len(weights1) - 1)

	value = 0.0

	if len(weights1) != len(weights2):

		raise ValueError("We have a problem here! The networks are different!")

	for i in range(switch):

		new_weights1.append(weights1[i])

		new_weights2.append(weights2[i])

	for i in range(switch, len(weights1)):

		new_weights2.append(weights1[i])

		new_weights1.append(weights2[i])

	return (new_weights1, new_weights2)




