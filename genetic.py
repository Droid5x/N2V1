from neural import *
from prize import *

class geneticAlgorithm(object):
	epoch = 0
	def __init__(self, number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs, number_of_actors, number_of_generations, num_targets):
		self.hidden_layers = number_of_hidden_layers
		self.hidden_size = size_of_hidden_layers
		self.input_size = num_inputs
		self.output_size = num_outputs
		self.actors = []
		for i in range(0, number_of_actors):
			self.actors.append(neuralActor(number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs))
		self.generations_simulated = 0
		self.max_generations = number_of_generations
		self.prizes = []
		for i in range(num_targets):
			self.prizes.append(prize())

	# replaces worst 50% of networks with children from the best 50% and mutates the top 50%
	def makeChildNetworks(self):
		#sort the actors by their scores
		self.actors.sort(key=lambda x: x.score, reverse = False)
		temp = self.actors[0:int(len(self.actors)/2)]
		newActor = neuralActor(self.hidden_layers, self.hidden_size, self.input_size, self.output_size)
		weights = []
		maxScore = self.actors[0].score
		minScore = self.actors[-1].score
		avgScore = 0.0
		for actor in self.actors:
			avgScore += actor.score
		for actor in temp:
			actor.mutate()
		for i in range(1,math.floor(len(self.actors)/2)):
			weights = recombineWeights(self.actors[i-1].getWeights(), self.actors[i].getWeights())
			newActor.network.replaceWeights(weights)
			temp.append(newActor)
		return (maxScore, minScore, avgScore/len(self.actors))


	def runEpoch(self):
		self.epoch += 1
		ticks = 0
		while ticks <= 500:
			for actor in self.actors:
				# check if it is near a prize:
				k = actor.closestPrize(self.prizes)
				target = self.prizes[k]
				inputs = [target.x, target.y]
				actor.runActor(inputs)
				if math.sqrt(abs(actor.x - target.x)**2 + abs(actor.y - target.y)**2) <= target_size:
					actor.score += 1
					self.prizes.pop[k]
					#add a new prize since one was taken
					self.prizes.append(prize())



			ticks+=1
		#now that the simulation has ended, find the average score, maximum score, and minimum score
		results = self.makeChildNetworks()
		print("Epoch " + str(self.epoch) + ":\n")




