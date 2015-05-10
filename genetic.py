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

	def makeChildNetworks(self):
		#sort the actors by their scores
		self.actors.sort(key=lambda x: x.score, reverse = 1)

		temp = self.actors[0:num_best]

		# add copies_best number of copies of the num_best actors
		for j in range(copies_best):
		
			for i in range(num_best):

				temp.append(temp[i])

		weights = []

		maxScore = self.actors[0].score

		minScore = self.actors[-1].score

		totalScorers = 0

		totalScore = 0.0

		for actor in self.actors:

			if actor.score > 0:

				totalScorers += 1

				totalScore += actor.score

		while(len(temp) < len(self.actors)):

			# make a new temporary actor for when new ones are created
			newActor = neuralActor(self.hidden_layers, self.hidden_size, self.input_size, self.output_size)

			weights_list = recombineWeights(self.actors[random.randint(0, len(self.actors)-1)].getWeights(), self.actors[random.randint(0, len(self.actors)-1)].getWeights())

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

				# if we get a valid index number, then the actor found the prize
				if k >= 0:	
					# Replace the prize by setting it as a new one (it'll get new x and y coords)				
					self.prizes.pop(k)

					self.prizes.append(prize())

					#increment the actor's score:
					actor.score += 1

			ticks+=1

		# now that the simulation has ended, find the average score, maximum score, and minimum score
		# also mutate and recombine the networks as needed
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




