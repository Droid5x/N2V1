import random
import math
random.seed()

boardSize = 100
mutation_prob = 0.1
target_size = 0.5

def sigmoid(totalActivation, threshold):
	if (threshold == 0):
		threshold = 0.0000001
	return 1/(1+math.exp(-(totalActivation-threshold/1.0)))

def recombineWeights(weights1, weights2):
	new_weights = []
	value = 0.0
	if len(weights1) != len(weights2):
		raise ValueError("We have a problem here! The networks are different!")
	for i in range(len(weights1)):
		value = random.random()
		new_weights.append(value*weights1[i] + (1-value)*weights2[i])
	return new_weights

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
		self.updateWeightsList()

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
		self.x = random.uniform(0,boardSize)
		self.y = random.uniform(0,boardSize)
		self.x_look = 1 # Should probably also randomize this
		self.y_look = 0

	def runActor(self, inputs):
		outputs = self.network.runNetwork(inputs)
		#apply a transform here, based on look vector and location
		radians = (math.pi/2)*(outputs[0]-outputs[1])
		temp_x = self.x_look
		temp_y = self.y_look
		self.x_look = temp_x*math.cos(radians) + temp_y*math.sin(radians)
		self.y_look = temp_y*math.cos(radians) - temp_x*math.sin(radians)
		temp_x = self.x_look
		temp_y = self.y_look
		norm = math.sqrt(temp_x**2 + temp_y**2)
		self.x_look /= norm
		self.y_look /= norm
		self.x += self.x_look
		self.y += self.y_look
		return outputs

	def getWeights(self):
		self.network.updateWeightsList()
		return self.network.weights

	def changeWeights(self, weights):
		self.network.replaceWeights(weights)

	def getLocation(self):
		return (self.x, self.y)

	def closestPrize(self, prizes): # takes list of all "prizes" (each has an x and y coord)
		dist = []
		minVal = 0
		indexVal = 0
		for prize in prizes:
			dist.append(math.sqrt(abs(self.x - prize.x)**2 + abs(self.y - prize.y)**2))
		for i in range(len(dist)):
			if dist[i] < minVal:
				minVal = dist[i]
				indexVal = i
		return i

	def mutate(self):
		temp = self.getWeights()
		for weight in temp:
			if random.random() <= mutation_prob:
				weight = random.uniform(-1,1)
		self.network.replaceWeights(temp)

