import random
import math
random.seed()

#might get rid of this function...
def sigmoid(totalActivation, threshold):
	if (threshold == 0):
		threshold = 0.0000001
	return 1/(1+math.exp(-totalActivation/threshold))

def recombineWeights(weights1, weights2):
	new_weights = []
	value = 0.0
	if len(weights1) != len(weights2):
		raise ValueError("We have a problem here! Two disimilar nets tried to have a child!")
	for i in range(len(weights1)):
		value = random()
		new_weights.append(value*weights1[i] + (1-value)*weights2[i])
	return new_weights

class neuron(object):
	def __init__(self, number_of_inputs):
		self.inputWeights = random.sample(range(100), number_of_inputs+1)
		self.totalActivation = 0.0
		self.output = 0.0
		
	def calcOutput(self, input_data):
		if (len(input_data) >= len(self.inputWeights)):
			raise ValueError("The input_data to a neuron was as large as the weights list!")
		self.totalActivation = 0.0
		for i in range(0, len(input_data)):
			self.totalActivation += input_data[i] + self.inputWeights[i]
		self.output = sigmoid(self.totalActivation, self.inputWeights[-1])
		return self.output

	def getOutput(self):
		return self.output


class neuralLayer(object):
	def __init__(self, number_of_neurons, num_inputs_per_neuron):
		self.neurons = []
		for i in range(0, number_of_neurons):
			self.neurons.append(neuron(num_inputs_per_neuron))


class neuralNet(object):
	def __init__(self, number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs):
		self.layers = []
		layerTemp = neuralLayer(num_inputs, num_inputs)
		self.layers.append(layerTemp)
		for i in range(0,number_of_hidden_layers):
			if i == 0:
				layerTemp = neuralLayer(size_of_hidden_layers, num_inputs)
			else:
				layerTemp = neuralLayer(size_of_hidden_layers, size_of_hidden_layers)
			self.layers.append(layerTemp)
		layerTemp = neuralLayer(num_outputs, size_of_hidden_layers)
		self.layers.append(layerTemp)
		# Now gather all the weights in the neural network for easier referencing:
		self.weights = []
		self.updateWeightsList()
	
	def updateWeightsList(self):
		del self.weights[:]
		for layer in self.layers:
			for neuron in layer.neurons:
				for weight in neuron.inputWeights:
					self.weights.append(weight)

	def replaceWeights(self, new_weights):
		counter = 0
		for layer in self.layers:
			for neuron in layer.neurons:
				for i in range(0, len(neuron.inputWeights)):
					neuron.inputWeights[i] = new_weights[counter]
					counter += 1

	def runNetwork(self, inputs):
		totalActivation = 0
		outputs = []
		for layer in self.layers:
			for i in range(0,len(layer.neurons)): # For each neuron
				outputs.append(layer.neurons[i].calcOutput(inputs))
			del inputs[:]
			inputs = outputs[:]
			del outputs[:]
		return inputs

class neuralActor(object):
	def __init__(self, number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs):
		self.network = neuralNet(number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs) 
		self.score = 0

	def runActor(self, inputs):
		return self.network.runNetwork(inputs)

	def getWeights(self):
		self.network.updateWeightsList()
		return self.network.weights

	def changeWeights(self, weights):
		self.network.replaceWeights(weights)

class geneticAlgorithm(object):
	def __init__(self, number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs, number_of_actors, number_of_generations):
		self.actors = []
		for i in range(0, number_of_actors):
			self.actors.append(neuralActor(number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs))
			self.generations_simulated = 0
			self.max_generations = number_of_generations


