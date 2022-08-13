import re
from tqdm import tqdm

# open text file with gathered wiki text
with open('wiki_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# get only words out of it - replaces all symbols like !,? etc...
# first substitute every non-alphanumeric character with " ", then:
# if double, triple, ... spaces exist just replace them with one space, afterwards split text into a list
text = re.sub(" +", " ", re.sub(r"[^a-zA-Z0-9]", " ", text)).split(" ")
# delete all "" in list
text = list(filter(lambda a: a != "", text))
# make every word lowercase
text = [x.lower() for x in text]
# get every word one time and sort the list alphabetically
unique_words = sorted(list(set(text)))

# create transition matrix - square matrix
transition_matrix = [[0 for j in range(len(unique_words))] for i in range(len(unique_words))]
# add each occurrence of state transition into the transition matrix
for i in tqdm(range(len(text)-1)):
    # current word in text (index in unique word list)
    current_state = unique_words.index(text[i])
    # next word in text (index in unique word list)
    future_state = unique_words.index(text[i+1])
    # add 1 to state transition in matrix
    transition_matrix[current_state][future_state] += 1

# divide each row by the sum of each row
for i in tqdm(range(len(transition_matrix))):
    if text[-1] != unique_words[i]:
        sum_row = 0
        for number_of_occurrences in transition_matrix[i]:
            sum_row += number_of_occurrences
        for j in range(len(transition_matrix[i])):
            transition_matrix[i][j] /= sum_row

# save unique words and transition matrix
with open('unique_words.txt', 'w', encoding='utf-8') as f:
    f.write(str(unique_words))
with open('transition_matrix.txt', 'w', encoding='utf-8') as f:
    f.write(str(transition_matrix))
