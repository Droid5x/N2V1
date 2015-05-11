# Here are most of the runtime parameters, which can all be adjusted to some degree
# When the program begins running, it will prompt the user for a filename to which to write the results of each epoch.

# This parameter describes the size (raduis) of a prize on the map
target_size = 2
# This configures the raduis of the actors
actor_size = 5
# This configures the board size. Currently square, as length and width are tied together.
boardSize = 400
# This is the probability that a mutation will occur given a particular weight in a neuron.
mutation_prob = 0.2
#This is the probability that two older networks will create two new ones with parts of the older networks' weights. (It's the probability that they'll have kids)
crossover_prob = 0.7
# This is the maximum value that may be added or subtracted from a network's weights should mutation occur.
max_mutation = 0.15
# This is the number of ticks that will occur during each epoch
max_ticks = 2000
# Maximum linear velocity of an actor on the map
max_linear_velocity = 2
# Maximum rotation that an actor can perform in one tick
max_rotational_velocity = 0.3
# NOTE: num_best should not exceed num_actors!
# This is the number of highest-ranked actors that will be copied into the next population
num_best = 4
# This is the number of copies of the num_best best actors that will be created (if this value is 0, then only the originals will go on and no duplicates will be made)
copies_best = 1
# NOTE: The number of actors must be EVEN!
# This is the total number of actors in the simulation, which remains constant
num_actors = 30
# This is the number of targets on the map
num_targets = 25
# NOTE: The number of hidden layers should be greater than zero!
# This is the number of intermediary layers, which does not include the first (input) layer or the last (output) layer
num_hidden_layers = 1
# This is the size of the hidden layers (currently all are kept to the same size)
size_hidden_layers = 6


''' A note on performance:
The higher the number of actors, targets, hidden layers, and size of hidden layers,
 the slower the program will perform as the epoch() function runs in something like 
 O(num_actors * num_prizes * num_hidden_layers * size_hidden_layers) time. '''

