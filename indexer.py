# imports
import spacy
import json
import math
from tqdm import tqdm

# Configure Spacy
nlp = spacy.load('en_core_web_md')

MEDIAN_PERCENTAGE = 0.1

# read file "CISI.ALLnettoye" and create a list of dictionaries
data = {}
file = "input/CISI.ALLnettoye"
with open(file, "r") as f:
    state = 0
    while True:
        line = f.readline()
        if not line:
            break
        if line.startswith(".I"):
            doc_id = line.split()[1]
            # cast to int
            doc_id = int(doc_id)
            data[doc_id] = {}
            data[doc_id]["id"] = doc_id
            data[doc_id]["title"] = ""
            data[doc_id]["abstract"] = ""
            state = 1
        else:
            if state == 1:
                data[doc_id]["title"] = line.strip()
                state = 2
            elif state == 2:
                if data[doc_id]["abstract"] != "":
                    data[doc_id]["abstract"] += " "
                data[doc_id]["abstract"] += line.strip()

for doc_id in tqdm(data):
    # For each article, Add the title to the abstract
    data[doc_id]["abstract"] = data[doc_id]["title"] + " " + data[doc_id]["abstract"]
    # For each article, Convert to lowercase
    data[doc_id]["abstract"] = data[doc_id]["abstract"].lower()
    # For each article, split the abstract into tokens with spacy
    data[doc_id]["abstract"] = nlp(data[doc_id]["abstract"], disable=["parser", "ner"])
    # For each article, Remove punctuation
    data[doc_id]["abstract"] = [token.text for token in data[doc_id]["abstract"] if not token.is_punct and not token.is_space]
    # For each article, Remove stopwords
    data[doc_id]["abstract"] = [word for word in data[doc_id]["abstract"] if not word in nlp.Defaults.stop_words]

print(data[1])

# Create an index
index = {}

for doc_id in tqdm(data):
    for word in data[doc_id]["abstract"]:
        if word not in index:
            index[word] = {}
        if doc_id not in index[word]:
            index[word][doc_id] = {}
            index[word][doc_id]["tf"] = 1
        else:
            index[word][doc_id]["tf"] += 1

# Normalize the index
for word in index:
    for doc_id in index[word]:
        index[word][doc_id]["tf"] /= len(data[doc_id]["abstract"])

# IDF

for word in index:
    index[word]["idf"] = math.log10(len(data) / len(index[word]))

# association d'un poids 
    
for word in index:
    for doc_id in index[word]:
        if doc_id != "idf":
            index[word][doc_id]["weight"] = index[word][doc_id]["tf"] * index[word]["idf"]

# get the median at 10% of the weight
weights = []
for word in index:
    for doc_id in index[word]:
        if doc_id != "idf":
            weights.append(index[word][doc_id]["weight"])
weights.sort()

# nettoyer index

index2 = {}

THRESHOLD = weights[int(len(weights) * MEDIAN_PERCENTAGE)]
for word in index :
    for doc_id in index[word] : 
        if doc_id != "idf" and index[word][doc_id]["weight"] < THRESHOLD :
            continue
        else :
            if word not in index2 :
                index2[word] = {}
            index2[word][doc_id] = index[word][doc_id]
    
# Save the index to a file
file = "output/index.json"
with open(file, "w") as f:
    json.dump(index2, f, indent=4)