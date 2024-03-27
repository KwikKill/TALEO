# imports
import spacy
import json

# Configure Spacy
nlp = spacy.load('en_core_web_md')

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

# For each article, split the abstract into words
for doc_id in data:
    data[doc_id]["abstract"] = data[doc_id]["title"].split() + data[doc_id]["abstract"].split()

# Create an index
index = {}

for doc_id in data:
    for word in data[doc_id]["abstract"]:
        if word not in index:
            index[word] = {}
        if doc_id not in index[word]:
            index[word][doc_id] = 1
        else:
            index[word][doc_id] += 1

# Normalize the index
for word in index:
    for doc_id in index[word]:
        index[word][doc_id] /= len(data[doc_id]["abstract"])

# Save the index to a file
file = "output/index.json"
with open(file, "w") as f:
    json.dump(index, f, indent=4)