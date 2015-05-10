from genetic import *
from neural import *
from neuralActor import *
from prize import *
from params import *
import random


def main():
	print("Parameters can be edited in the params.py config file.\n")
	input("Press any key to begin the simulation.\n")
	gen = geneticAlgorithm(1,6,4,2,num_actors,num_targets)
	while(1):
		gen.runEpoch()
		

if __name__ == "__main__":
	main()