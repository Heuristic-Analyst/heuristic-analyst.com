import numpy as np
from scipy import linalg
# all states in one list
states = ["cloudy","rainy", "sunny"]
# create transition matrix A - same order as in "states"
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

print("Every eigenvector with lambda 1 and elements greater or equal zero:")
print(equilibriums)