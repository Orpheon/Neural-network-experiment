from __future__ import division
import math, sys, os, time, random

class NeuralNet(object):

	NUM_NEURONS_PER_HID_LAYER = 6 # Number of neurons per hidden layers
	NUM_HID_LAYERS = 2 # Number of hidden layers

	def __init__(self, weights=[]):

		if weights == []:
			weights = self.get_random_weights()

		self.weights = weights[:]# Only used for breeding and mutation later on; no influence on this network

		# Create the whole neuron network
		self.neuronlist = []

		# Input neurons:
		for i in range(4):
			neuron = Neuron(self)
			self.neuronlist.append(neuron)

		# Hidden layer neurons
		for layer in range(self.NUM_HID_LAYERS):
			for i in range(self.NUM_NEURONS_PER_HID_LAYER):
				neuron = Neuron(self)
				self.neuronlist.append(neuron)

		# Output neurons: Dummy neurons, they don't pass anything on
		self.left_output_neuron = Neuron(self, activated=0)
		self.right_output_neuron = Neuron(self, activated=0)
		self.neuronlist.append(self.left_output_neuron)
		self.neuronlist.append(self.right_output_neuron)


		# Now connect all the nodes to the nodes in front of them, and add weights. http://www.ai-junkie.com/ann/evolved/images/simple_feedforward_network.jpg

		# Input neurons:
		layer_start = 4
		for i in range(4):
			neuron = self.neuronlist[i]
			for position in range(self.NUM_NEURONS_PER_HID_LAYER):
				neuron.connections[layer_start+position] = weights.pop(0) # Take the next weight in line, and attribute it to the connection, and remove it from the list

		# Hidden layers:
		for layer in range(self.NUM_HID_LAYERS-1): # The last hidden layer comes at the end

			for i in range(self.NUM_NEURONS_PER_HID_LAYER):
				neuron = self.neuronlist[layer_start+i]
				for position in range(self.NUM_NEURONS_PER_HID_LAYER):
					neuron.connections[layer_start+self.NUM_NEURONS_PER_HID_LAYER+position] = weights.pop(0)

			layer_start += self.NUM_NEURONS_PER_HID_LAYER

		# The last hidden layer:
		for i in range(self.NUM_NEURONS_PER_HID_LAYER):
			neuron = self.neuronlist[layer_start+i]
			for position in range(2):
				neuron.connections[layer_start+self.NUM_NEURONS_PER_HID_LAYER+position] = weights.pop(0)

	def get_random_weights(self):
		numweights = (4*self.NUM_NEURONS_PER_HID_LAYER) + (self.NUM_HID_LAYERS-1)*(self.NUM_NEURONS_PER_HID_LAYER**2) + (2*self.NUM_NEURONS_PER_HID_LAYER)
		weightlist = []
		for i in range(numweights):
			weightlist.append((random.random()*2)-1)

		return weightlist


	def run(self, inputs=((0, 0), (0, 0)) ):

		for neuron in self.neuronlist:
			neuron.inputbuffer = 0

		self.neuronlist[0].inputbuffer = (inputs[0])[0]# Set the input values to the input neurons
		self.neuronlist[1].inputbuffer = (inputs[0])[1]
		self.neuronlist[2].inputbuffer = (inputs[1])[0]
		self.neuronlist[3].inputbuffer = (inputs[1])[1]

		for neuron in self.neuronlist:
			neuron.run()# Propagate the signal through the network

		# Output value is now stored in self.left_output_neuron/right_output_neuron, respectively
		return self.left_output_neuron.inputbuffer*10, self.right_output_neuron.inputbuffer*10# Return these values


class Neuron(object):

	def __init__(self, neuralnet, activated=1):
		self.inputbuffer = 0
		self.ownernetwork = neuralnet
		self.connections = {}
		self.activated = activated

	def run(self):
		output = self.activation_function(self.inputbuffer)

		if self.activated:
			for index, weight in self.connections.items():
				self.ownernetwork.neuronlist[index].inputbuffer += output*weight

	def activation_function(self, x):
		x = 1/(1+(math.e**(-x)))# Sigmoidal function, x is now between 0 and 1. http://www.ai-junkie.com/ann/evolved/images/sigmoid.jpg
		x = (2*x)-1# We want it between -1 and 1
		return x
