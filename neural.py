import random
import math
random.seed()

#might get rid of this function...
def sigmoid(totalActivation, threshold):
	if (threshold == 0):
		threshold = 0.0000001
	return 1/(1+math.exp(-totalActivation/threshold))

class neuron(object):
	def __init__(self, number_of_inputs):
		self.inputWeights = random.sample(xrange(100), number_of_inputs+1)
		self.totalActivation = 0.0
		self.output = 0.0
		
	def calcOutput(self, input):
		if (len(input) >= len(self.inputWeights)):
			raise ValueError("The input to a neuron was as large as the weights list!")
		totalActivation = 0.0
		for i in range(0, len(input))
			totalActivation += input[i] + inputWeights[i]
		self.output = sigmoid(totalActivation, inputWeights[-1])
		return self.output

	def getOutput(self):
		return self.output


class neuralLayer(object):
	def __init__(self, number_of_neurons, num_inputs_per_neuron):
		self.neurons = []
		for (i in range(0, number_of_neurons)):
			self.neurons.append(neuron(num_inputs_per_neuron))


class neuralNet(object):
	def __init__(self, number_of_hidden_layers, size_of_hidden_layers, num_inputs, num_outputs):
		self.layers = []
		firstLayer = neuralLayer(num_inputs, num_inputs)
