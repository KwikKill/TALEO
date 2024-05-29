"""
This script is a simple search engine that uses the inverted index created by the index.py script to retrieve the most relevant documents for a given query.
"""

# imports
import spacy
import json
from tqdm import tqdm
import argparse
from numpy.linalg import norm
from numpy import dot


# Configure Spacy
nlp = spacy.load('en_core_web_md')

# Parse command-line arguments
parser = argparse.ArgumentParser()
# Add limit argument to choose the number of documents to retrieve or the minimum score (mutually exclusive)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--limit", type=int, help="Choose the number of documents to retrieve")
group.add_argument("--score", type=float, help="Choose the minimum score to retrieve")
args = parser.parse_args()

# read index file "ouput/index.json" and create a list of dictionaries
index = {}
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

# Precompile stopwords set
stopwords = set(nlp.Defaults.stop_words)

for doc_id in tqdm(query_data):
    # For each article, concatenate the title, author, journal, volume, and text
    query_data[doc_id]["text"] = \
        query_data[doc_id]["title"] +\
        query_data[doc_id]["author"] +\
        query_data[doc_id]["journal"] +\
        query_data[doc_id]["volume"] +\
        query_data[doc_id]["text"]
    
    # For each article, Convert to lowercase
    query_data[doc_id]["text"] = query_data[doc_id]["text"].lower()

# Batch process texts with SpaCy
texts = [doc["text"] for doc in query_data.values()]
processed_texts = list(nlp.pipe(texts, disable=["parser", "ner"]))

for doc_id, doc in zip(query_data.keys(), processed_texts):
    # For each article, Remove punctuation, stopwords, and lemmatize
    query_data[doc_id]["text"] = [token.lemma_ for token in doc if not token.is_punct and not token.is_space and token.text not in stopwords]

# Get the list of document IDs (except "idf")
docs_ids = []
for term in index:
    for doc_id in index[term]:
        if doc_id != "idf" and doc_id not in docs_ids:
            docs_ids.append(doc_id)

# For each query, compute the cosine similarity with each document
for query_id in query_data:
    query = query_data[query_id]["text"]
    query_vector = [index[term]["idf"] if term in index else 0 for term in query]
    scores = {}
    for doc_id in docs_ids:
        doc_vector = [index[term][doc_id]["weight"] if term in index and doc_id in index[term] else 0 for term in query]
        if norm(query_vector) > 0 and norm(doc_vector) > 0:
            scores[doc_id] = dot(query_vector, doc_vector) / (norm(query_vector) * norm(doc_vector))
        else:
            scores[doc_id] = 0
    query_data[query_id]["scores"] = scores

# For each query, sort the documents by score
for query_id in query_data:
    query_data[query_id]["scores"] = sorted(query_data[query_id]["scores"].items(), key=lambda x: x[1], reverse=True)

output = ""
output_file = "output/query_results"

# Keep only the top N documents or the documents with a score above a threshold
if args.limit:
    for query_id in query_data:
        query_data[query_id]["scores"] = query_data[query_id]["scores"][:args.limit]
else:
    for query_id in query_data:
        query_data[query_id]["scores"] = [(doc_id, score) for doc_id, score in query_data[query_id]["scores"] if score >= args.score]

for query_id in query_data:
    for doc_id, score in query_data[query_id]["scores"]:
        output += f"{query_id} {doc_id} {score}\n"

with open(output_file, "w") as f:
    f.write(output)