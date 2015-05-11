from genetic import *
from neural import *
from neuralActor import *
from prize import *
from params import *
import random

# The sole purpose of this program is to tie all the neural classes
# together and run the resource-gathering demo

def main():
	print("Parameters can be edited in the params.py config file.\n")
	input("Press any key to begin the simulation.\n")
	# For this application, all of the parameters may be adjusted in the params.py 
	# file, except for the number of inputs and outputs to each neural netowrk 
	# (these are permanently set to 4 and 2, respectively)
	gen = geneticAlgorithm(num_hidden_layers,size_hidden_layers,4,2,num_actors,num_targets)
	while(1):
		gen.runEpoch()
		

if __name__ == "__main__":
	main()