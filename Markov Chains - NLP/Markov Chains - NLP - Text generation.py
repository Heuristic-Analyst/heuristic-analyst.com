import json
import random
from tqdm import tqdm

# open unique words and calculated transition matrix
with open('unique_words.txt', 'r', encoding='utf-8') as f:
    unique_words = f.read()
with open('transition_matrix.txt', 'r', encoding='utf-8') as f:
    transition_matrix = f.read()

# convert string representation of list to actual list using json.loads()
unique_words = json.loads(unique_words.replace("'", '"'))
print("Unique words:", len(unique_words))
transition_matrix = json.loads(transition_matrix)

# generate random text by giving a start word (must be included in the training text)
starting_phrase = "Sigmund Freud"
length_of_sentences = 20    # words
number_of_sentences = 10
# get "Freud" as the starting word
start_word = starting_phrase.split(" ")[-1]
current_word = start_word.lower()
sentences = [starting_phrase.lower() for i in range(number_of_sentences)]
for i in tqdm(range(number_of_sentences)):
    for j in range(length_of_sentences):
        current_state = unique_words.index(current_word)
        try:
            next_state = random.choices(unique_words, transition_matrix[current_state])[0]
            current_word = next_state
            sentences[i] += " " + current_word
        except:
            break
for i in range(len(sentences)):
    print(str(i+1)+". sentence:", sentences[i])