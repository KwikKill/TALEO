# imports
import spacy
import json
from tqdm import tqdm

# Configure Spacy
nlp = spacy.load('en_core_web_md')

# Constants
THRESHOLD = 0.2

# read index file "ouput/index.json" and create a list of dictionaries
index = {
}
file = "output/index.json"
with open(file, "r") as f:
    index = json.load(f)

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

for doc_id in tqdm(query_data):
    # For each article, split the abstract into words
    query_data[doc_id]["text"] = \
        query_data[doc_id]["title"] +\
        query_data[doc_id]["author"] +\
        query_data[doc_id]["journal"] +\
        query_data[doc_id]["volume"] +\
        query_data[doc_id]["text"]
    
    # For each article, Convert to lowercase
    query_data[doc_id]["text"] = query_data[doc_id]["text"].lower()
    # For each article, split the abstract into tokens with spacy
    query_data[doc_id]["text"] = nlp(query_data[doc_id]["text"], disable=["parser", "ner"])
    # For each article, Remove punctuation
    query_data[doc_id]["text"] = [token.text for token in query_data[doc_id]["text"] if not token.is_punct and not token.is_space]
    # For each article, Remove stopwords
    query_data[doc_id]["text"] = [word for word in query_data[doc_id]["text"] if not word in nlp.Defaults.stop_words]

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

output = ""
output_file = "output/query_results"

for query_id in query_data:
    for doc_id, score in query_data[query_id]["scores"]:
        if score < THRESHOLD:
            break
        output += f"{query_id} {doc_id} {score}\n"

with open(output_file, "w") as f:
    f.write(output)