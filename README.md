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
    python3 search.py indexer.py --score 0.4
    python3 search.py indexer.py --limit 10
    ```

3. Evaluation :
    - Run the following command to evaluate the search results.
    ```
    python3 eval.py example/CISI_dev.REL output/query_results
    ```

4. Best Result :
   - For now, best result is obtained by using :
   ```
   python3 indexer.py
   python3 search.py indexer.py --score 0.4
   python3 eval.py example/CISI_dev.REL output/query_results
   ```
   - We use TF.IDF for `indexer.py` and Cosine for `search.py`, they are set by default, only the threshold of 0.415 is needed for `search.py` (isn't set by default)
## Authors

- [KwikKill](https://github.com/KwikKill)
- [Zalen](https://github.com/SirZalen)
- [Ouiske](https://github.com/ouiske)

## Disclaimer

This project is a school project and don't have a correct files structure or code quality.
Feel free to use the code and improve it as you want under the CC-BY-NC-SA license.
