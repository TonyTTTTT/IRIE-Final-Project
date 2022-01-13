# Three model for solving document retrieval
Each model's implementation will contain in the directory which named as that model.
## BM25 [鄒咏霖]
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

## Doc2Vec [黃翔偉]
- OS: Window 10
- Python version: 3.10
- requirement file: in ./Doc2Vec/doc2vec.requirements.txt
### how to run the code
just simply type
``` shell
cd Doc2Vec
python3 data_clean.py
python3 doc2vec.py 
```
When the program were finished successfully, it will generate a file named "final_ans.csv".

## Doc2Vec(byJimmy) [陳昕璘]