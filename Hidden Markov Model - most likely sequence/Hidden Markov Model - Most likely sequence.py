###########################################
# The first code-part (between "#####...") is from a previous post to find the stationary probability of states
import numpy as np
from scipy import linalg
# all states in one list
states = ["cloudy","rainy", "sunny"]
# create transition matrix A - same order as in "states"
# cloudy, rainy, sunny
A = [[0.1, 0.6, 0.3],   # cloudy
     [0.7, 0.1, 0.2],   # rainy
     [0.4, 0.4, 0.2]]   # sunny

# convert matrix to numpy matrix
A = np.array(A)

# calculate eigenvalues and eigenvectors
eigenvalues, eigenvectors = linalg.eig(A, left=True, right=False)

# probability distribution vector should add up to one - same as lambda of eigenvector equation is 1
# -> divide each vector element by the sum of each vector's element
eigenvectors = eigenvectors/eigenvectors.sum()

# transpose eigenvectors matrix to get a vector easily out of the matrix
eigenvectors = eigenvectors.transpose()

# loop through each vector and see if all elements of vector are greater or equal to zero
# (because there are no negative probabilities)
# save valid eigenvectors in "equilibriums
equilibriums = []
for i in range(len(eigenvectors)):
     isGreaterEqualZero = True
     for j in range(len(eigenvectors[i])):
          if eigenvectors[i][j] <= 0:
               isGreaterEqualZero = False
     if isGreaterEqualZero == True:
          equilibriums.append([])
          for j in range(len(eigenvectors[i])):
               equilibriums[-1].append(eigenvectors[i][j])

###########################################
# which sequence is observable of the observable variable?
# This will be the sequence we will compute the most likely Markov chain states sequence from
sequence_of_observable_variable = ["happy", "sad", "sad", "happy", "sad"]

# all observable states in one list
observable_states = ["happy", "sad"]
# Create happy/sad face probabilities dependent on the weather
# cloudy, rainy, sunny
B = [[0.15, 0.05, 0.7],  # happy face
     [0.2, 0.7, 0.1]]    # sad face

# standard library for combination/permutation/product of observable states
import itertools
# create permutation list of states list (each combination of the states given length of the sequence n)
# combination returned in tuples or triples or ... depends on amount of possible states
products = list(itertools.product(states, repeat=len(sequence_of_observable_variable)))

maximum_sequence = () # tuple or triple or ... depends on amount of possible states
# starting probability - will be compared to and changed to maximum probability during the iterations
maximum_probability = 0

for product in products:
     for i in range(len(product)):
          if i == 0:
               # first Markov chain state probability is did not transition from another state -> stationary probability
               # I think there might be several eigenvectors/equilibriums but I do not know whether so
               # and if so, i do not know which one to take to start, so I just take the first eigenvector/equilibrium
               probability = equilibriums[0][states.index(product[i])]
          else:
               # state probability is transition probability from before
               current_state = states.index(product[i])
               previous_state = states.index(product[i-1])
               # multiply with transition probability from step i-1 to i
               probability *= A[previous_state][current_state]
          probability *= B[observable_states.index(sequence_of_observable_variable[i])][states.index(product[i])]

     if probability > maximum_probability:
          maximum_probability = probability
          maximum_sequence = product

print("Maximizing sequence:", maximum_sequence)
print("Sequence's probability:", maximum_probability)