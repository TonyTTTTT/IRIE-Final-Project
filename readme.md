# Three model for solving document retrieval
Each model's implementation will contain in the directory which named as that model.
## BM25
- OS: Ubuntu 20.04.3 LTS (Focal Fossa)
- Python version: 3.8.10
- requirement file: in ./bm25/bm25.requirements.txt
### how to run the code
just simply type
``` shell
cd bm25
python3  reterieve-by-bm25.py
```
and the process will began. At the end of the process, it will output a file named "test_predict_new_stop_word_bXX.csv", where XX is the parameter b in bm25 currently use.
## ML(?
## Doc2Vec
- OS: Window 10
- Python version: 3.10
- requirement file: in ./doc2vec/doc2vec.requirements.txt
### how to run the code
just simply type
``` shell
cd doc2vec
python3 data_clean.py
python3 doc2vec.py 
```
When all of the processes were executed successfully, it will generate a file named "final_ans.csv".
