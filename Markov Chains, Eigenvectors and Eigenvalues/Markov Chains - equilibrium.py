import numpy as np
# all states in one list
states = ["cloudy","rainy", "sunny"]
# create transition matrix A - same order as in "states"
A = [[0.1, 0.6, 0.3],   # cloudy
     [0.7, 0.1, 0.2],   # rainy
     [0.4, 0.4, 0.2]]   # sunny

# start with a random state, lets say rainy
pi = [0, 1, 0]
pi_previous = pi
# convert matrices to numpy matrices
A = np.array(A)
pi = np.array(pi)
pi_previous = np.array(pi_previous)

while True:
     # dot product of pi x A
     pi = pi.dot(A)
     # if pi = pi_previous -> equilibrium found (pi will not change after it)
     if (pi==pi_previous).all():
          break
     else:
          pi_previous = pi
print(states)
print(pi)
