# imports
import spacy
import json

# Configure Spacy
nlp = spacy.load('en_core_web_md')

# read index file "ouput/index.json" and create a list of dictionaries
index = {
    "the": {
        1: 0.6,
        27: 0.4,
        3: 0.3,
    },
    "cat": {
        1: 0.4,
        2: 0.3,
        3: 0.2,
    },
    "dog": {
        1: 0.3,
        29: 0.2,
        3: 0.1,
    },
    "database": {
        1: 0.2,
        22: 0.1,
        33: 0.7,
    },
}
#file = "output/index.json"
#with open(file, "r") as f:
#    index = json.load(f)

query_data = {}
# read file "example/CISI_dev.QRY" and create a list of dictionaries
file = "example/CISI_dev.QRY"
with open(file, "r") as f:
    state = 0
    while True:
        line = f.readline()
        if not line:
            break
        if line.startswith(".I"):
            doc_id = line.split()[1]
            doc_id = int(doc_id)
            query_data[doc_id] = {}
            query_data[doc_id]["id"] = doc_id
            query_data[doc_id]["text"] = ""
            query_data[doc_id]["title"] = ""
            query_data[doc_id]["author"] = ""
            query_data[doc_id]["journal"] = ""
            query_data[doc_id]["volume"] = ""
        elif line.startswith(".T"):
            query_data[doc_id]["title"] = f.readline()
        elif line.startswith(".A"):
            query_data[doc_id]["author"] = f.readline()
        elif line.startswith(".B"):
            query_data[doc_id]["journal"] = f.readline()
        elif line.startswith(".N"):
            query_data[doc_id]["volume"] = f.readline()
        elif line.startswith(".W"):
            state = 1
        elif line.strip() != "":
            if state == 1:
                if query_data[doc_id]["text"] != "":
                    query_data[doc_id]["text"] += " "
                query_data[doc_id]["text"] += line.strip()

# For each article, split the abstract into words
for doc_id in query_data:
    query_data[doc_id]["text"] = \
        query_data[doc_id]["title"].split() +\
        query_data[doc_id]["author"].split() +\
        query_data[doc_id]["journal"].split() +\
        query_data[doc_id]["volume"].split() +\
        query_data[doc_id]["text"].split()

# For each query, compute the cosine similarity with each document
for query_id in query_data:
    query = query_data[query_id]["text"]
    scores = {}
    for term in query:
        if term in index:
            for doc_id in index[term]:
                if doc_id not in scores:
                    scores[doc_id] = 0
                scores[doc_id] += index[term][doc_id]
    query_data[query_id]["scores"] = scores

# For each query, sort the documents by score
for query_id in query_data:
    query_data[query_id]["scores"] = sorted(query_data[query_id]["scores"].items(), key=lambda x: x[1], reverse=True)

# For each query, print the top 5 documents
for query_id in query_data:
    print("Query:", query_id)
    for doc_id, score in query_data[query_id]["scores"][:5]:
        print("Document:", doc_id, "Score:", score)
    print()