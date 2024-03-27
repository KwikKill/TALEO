# imports
import spacy

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

print(data[1])