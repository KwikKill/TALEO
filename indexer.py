# imports
import spacy
import json
import math
from tqdm import tqdm
import argparse

# Configure Spacy
nlp = spacy.load('en_core_web_md')

# Parse command-line arguments
parser = argparse.ArgumentParser()
# Add method argument to choose the indexing method (TF IDF or BM25)
parser.add_argument("--method", choices=["tfidf", "bm25", "dirichlet", "jelinek_mercer"], default="tfidf", help="Choose the indexing method (TF IDF or BM25)")
# If BM25 is chosen, add K and B arguments
parser.add_argument("--k", type=float, default=2.2, help="BM25 parameter K")
parser.add_argument("--b", type=float, default=0.75, help="BM25 parameter B")
# If Dirichlet is chosen, add MU argument
parser.add_argument("--mu", type=float, default=2000, help="Dirichlet parameter MU")
# If Jelinek-Mercer is chosen, add LAMBDA argument
parser.add_argument("--lamb", type=float, default=0.1, help="Jelinek-Mercer parameter LAMBDA")
args = parser.parse_args()

# BM25 parameters
BM_K = args.k
BM_B = args.b
# Dirichlet parameter
MU = args.mu
# Jelinek-Mercer parameter
LAMBDA = args.lamb

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

# Precompile stopwords set
stopwords = set(nlp.Defaults.stop_words)

for doc_id in tqdm(data):
    # For each article, Add the title to the abstract
    data[doc_id]["abstract"] = data[doc_id]["title"] + " " + data[doc_id]["abstract"]
    # For each article, Convert to lowercase
    data[doc_id]["abstract"] = data[doc_id]["abstract"].lower()

# Batch process texts with SpaCy
abstracts = [doc["abstract"] for doc in data.values()]
processed_abstracts = list(nlp.pipe(abstracts, disable=["parser", "ner"]))

for doc_id, doc in tqdm(zip(data.keys(), processed_abstracts)):
    # For each article, Remove punctuation, stopwords, and lemmatize
    data[doc_id]["abstract"] = [token.lemma_ for token in doc if not token.is_punct and not token.is_space and token.text not in stopwords]

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

# association d'un poids (BM25 ou TFIDF) à chaque mot
for word in index:
    for doc_id in index[word]:
        if doc_id != "idf":
            if args.method == "tfidf":
                index[word][doc_id]["weight"] = index[word][doc_id]["tf"] * index[word]["idf"]
            elif args.method == "bm25":
                index[word][doc_id]["weight"] = (index[word][doc_id]["tf"] * (BM_K + 1)) / (index[word][doc_id]["tf"] + BM_K * (1 - BM_B + BM_B * len(data[doc_id]["abstract"]) / 100))
            elif args.method == "dirichlet":
                index[word][doc_id]["weight"] = (index[word][doc_id]["tf"] + MU * index[word]["idf"]) / (len(data[doc_id]["abstract"]) + MU)
            elif args.method == "jelinek_mercer":
                index[word][doc_id]["weight"] = (1 - LAMBDA) * (index[word][doc_id]["tf"] / len(data[doc_id]["abstract"])) + LAMBDA * index[word]["idf"]

# get the median at 10% of the weight
#weights = []
#for word in index:
#    for doc_id in index[word]:
#        if doc_id != "idf":
#            weights.append(index[word][doc_id]["weight"])
#weights.sort()

# nettoyer index

index2 = {}

#THRESHOLD = weights[int(len(weights) * MEDIAN_PERCENTAGE)]
#for word in index :
#    for doc_id in index[word] : 
        #if doc_id != "idf" and index[word][doc_id]["weight"] < THRESHOLD :
        #    continue
        #else :
#        if word not in index2 :
#            index2[word] = {}
#        index2[word][doc_id] = index[word][doc_id]    

# For each document, compute the norm of the vector
#index2 = {}

#for word in index:
#    for doc_id in index[word]:
#        if doc_id != "idf":
#            if doc_id not in index2:
#                index2[doc_id] = 0
#            index2[doc_id] += index[word][doc_id]["weight"] ** 2

#for doc_id in index2:
#    index2[doc_id] = math.sqrt(index2[doc_id])

# Save the index to a file
file = "output/index.json"
with open(file, "w") as f:
    json.dump(index, f, indent=4)