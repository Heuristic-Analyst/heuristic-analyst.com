# see here how to sample a random number from a random distribution with Python:
#https://www.adamsmith.haus/python/answers/how-to-sample-a-random-number-from-a-probability-distribution-in-python
import random
# all states in one list
states = ["cloudy","rainy", "sunny"]
# create transition matrix - same order as in "states"
transition_matrix = [[0.1, 0.6, 0.3],   # cloudy
                     [0.7, 0.1, 0.2],   # rainy
                     [0.4, 0.4, 0.2]]   # sunny
# will hold every random walk
random_walk = []
# begin with a random state - I just used 1/n as the probability to start with each state
current_state = random.choices(states, [1/3, 1/3, 1/3])[0]
# run random walk 100.000 times
for i in range(100000):
    # get index of current state in states list
    state_index = states.index(current_state)
    # random selection of a state with the distribution in the transition matrix - current state = new state
    current_state = random.choices(states, transition_matrix[state_index])[0]
    # add current state, which is the new generated state, to the random walk list
    random_walk.append(current_state)

occurrences = [random_walk.count("cloudy"), random_walk.count("rainy"), random_walk.count("sunny")]
print("Verify n:", occurrences[0]+occurrences[1]+occurrences[2])
print("Probabilities:", occurrences[0]/100000, occurrences[1]/100000,occurrences[2]/100000)
print(random_walk)
