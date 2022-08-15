hidden_states = ["cloudy", "rainy", "sunny"]
initial_matrix = {"cloudy":0.396, "rainy":0.368, "sunny":0.239}
transition_matrix = {
    "cloudy": {"cloudy":0.1, "rainy":0.6, "sunny":0.3},
    "rainy": {"cloudy":0.7, "rainy":0.1, "sunny":0.2},
    "sunny": {"cloudy":0.4, "rainy":0.4, "sunny":0.2}
}

emission_states = ["happy", "sad"]
emission_matrix = {
    "happy": {"cloudy": 0.15, "rainy": 0.05, "sunny": 0.8},
    "sad": {"cloudy":0.2, "rainy":0.7, "sunny":0.1}
}

observation_sequence = ["sad", "happy", "sad", "sad", "happy", "sad", "happy"]
nodes = []

# calculate first nodes
nodes.append({})
for current_hidden_state in hidden_states:
    # save information about each node: state, probability and previous maximum node coming from
    nodes[0][current_hidden_state] = {
        "probability": initial_matrix[current_hidden_state]*emission_matrix[observation_sequence[0]][current_hidden_state],
        "previous": None}

# calculate all next nodes
for i in range(1, len(observation_sequence)):
    nodes.append({})
    for current_hidden_state in hidden_states:
        nodes[i][current_hidden_state] = {
            "probability": 0,
            "previous": None}
        # calculate hidden state by choosing maximizing previous state
        # iterate through previous states
        for previous_hidden_state in nodes[i-1].keys():
            # calculate probability with previous state x transition prob.(previous, current) x emission prob.
            prob_tmp = nodes[i-1][previous_hidden_state]["probability"]
            prob_tmp *= transition_matrix[previous_hidden_state][current_hidden_state]
            prob_tmp *= emission_matrix[observation_sequence[i]][current_hidden_state]
            # if prob. > previous calculated hidden state for current state -> substitute
            if prob_tmp > nodes[i][current_hidden_state]["probability"]:
                nodes[i][current_hidden_state]["probability"] = prob_tmp
                nodes[i][current_hidden_state]["previous"] = previous_hidden_state

# choose most probable state: backwards iteration
most_likely_sequence = [["Step: " + str(i+1), 0, 0] for i in range(len(observation_sequence))]
l = len(nodes)-1
for i in range(l, -1, -1):
    if i == l:
        for hidden_states in nodes[i].keys():
            if nodes[i][hidden_states]["probability"] > most_likely_sequence[i][2]:
                most_likely_sequence[i][1] = hidden_states
                most_likely_sequence[i][2] = nodes[i][hidden_states]["probability"]
    else:
        most_likely_sequence[i][1] = nodes[i+1][most_likely_sequence[i+1][1]]["previous"]
        most_likely_sequence[i][2] = nodes[i][most_likely_sequence[i][1]]["probability"]

for i in most_likely_sequence:
    print(i)
