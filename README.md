### Documents search engine

This project is a simple search engine for documents made for a INSA Rennes practical work.

## How to run the project

1. Indexing :
    - Run the following command to index the documents:
    ```
    python3 indexer.py
    ```
    - The indexed documents will be stored in the `output/index.json` file. 
    It's format is a term weight dictionary for each document.
    - Optionally, you can specify the algorithm to use for indexing and it's options if needed. 
    ```
    python3 indexer.py --method bm25 --k 10 --b 0.1
    python3 indexer.py --method tfidf
    python3 indexer.py --method dirichlet --mu 2000
    python3 indexer.py --method jelinek_mercer --lambda 0.7
    python3 indexer.py --method absolute_discounting --delta 0.7
    ```

2. Searching :
    - Run the following command to search for the queries in the indexed documents.
    ```
    python3 search.py
    ```
    - The search results will be stored in the `output/query_results` file.
    - Like indexer.py, you can specify a method to check vector similarities, using cosine by default
    - Optionally, you can specify the the filtering method to use for searching and it's options if needed. 
    ```
    python3 search.py --method cosine --score 0.4
    python3 search.py --method pearson
    python3 search.py --method euclidean
    python3 search.py --method jensenshannon
    python3 search.py --method manhattan
    ```

3. Evaluation :
    - Run the following command to evaluate the search results.
    ```
    python3 eval.py example/CISI_dev.REL output/query_results
    ```

4. Best Result :
   - For now, best result is obtained by using :
   ```
   indexer : dirichlet, MU = 2000 | search : cosine, 0.41 (22.5%)
   indexer : jelinek_mercer, lambda = 0.1 | search : cosine, 0.41 (22.5%)
   indexer : jelinek_mercer, lambda = 0.01 | search : cosine 0.41 (22.6%)
   indexer : absolute_discounting | search : cosine, 0.415 (22.6%)
   ```
   Those results are obtained on the 
## Authors

- [KwikKill](https://github.com/KwikKill)
- [Zalen](https://github.com/SirZalen)
- [Ouiske](https://github.com/ouiske)

## Disclaimer

This project is a school project and don't have a correct files structure or code quality.
Feel free to use the code and improve it as you want under the CC-BY-NC-SA license.
