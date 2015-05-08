import random
import math
from copy import deepcopy
random.seed()

mutation_prob = 0.15

class neuron(object):
	def __init__(self, number_of_inputs):
		self.inputWeights = []

		for i in range(0, number_of_inputs+1):

			self.inputWeights.append(random.uniform(-1,1))

		self.totalActivation = 0.0

		self.output = 0.0
		
	def calcOutput(self, input_data):
		if (len(input_data) >= len(self.inputWeights)):

			raise ValueError("The input_data to a neuron was as large as the weights list!")

		self.totalActivation = 0.0

		for i in range(0, len(input_data)):

			self.totalActivation += input_data[i] * self.inputWeights[i]

		self.output = sigmoid(self.totalActivation, self.inputWeights[-1])

		return self.output

	'''def getOutput(self):
		return self.output'''


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
	
	#refresh the object's weights list
	def updateWeightsList(self):
		self.weights = []

		for layer in self.layers:

			for neuron in layer.neurons:

				for weight in neuron.inputWeights:

					self.weights.append(weight)

	# replace the object's weights with new_weights
	def replaceWeights(self, new_weights):
		counter = 0

		for layer in self.layers:

			for neuron in layer.neurons:

				for i in range(0, len(neuron.inputWeights)):

					neuron.inputWeights[i] = new_weights[counter]

					counter += 1

		self.updateWeightsList()

	def runNetwork(self, inputs):
		totalActivation = 0

		outputs = []

		if len(self.layers[0].neurons) != len(inputs):

			print("Error: input size to network is invalid!")

			return outputs

		for layer in self.layers:

			for i in range(0,len(layer.neurons)): # For each neuron

				outputs.append(layer.neurons[i].calcOutput(inputs))

			inputs = []

			inputs = outputs[:]

			outputs = []

		return inputs

def sigmoid(totalActivation, threshold):

	return 1/(1+math.exp(-(totalActivation-threshold/1.0)))

