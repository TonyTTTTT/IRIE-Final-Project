#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 18:45:49 2021

@author: r09922176
"""
import os
from DataLoader import DataLoader
import pickle
import numpy as np

prefix = '../../'
if __name__ == '__main__':
    dataLoader = DataLoader()

    print('loading queries...')
    queries = {}
    for f in os.listdir(prefix + 'ntu-2021fall-ir/test_query'):
        summary = dataLoader.loadQuery(prefix + 'ntu-2021fall-ir/test_query/'+f)
        # print('{}: {}'.format(f, summary))
        queries[f] = summary
        # queries.append(summary)
    print('queries loaded.')

    print('loading docs...')
    with open('docs-str-wo-filter.pkl', 'rb') as f:
        docs = pickle.load(f)
    with open('docsId.pkl', 'rb') as f:
        docsId = pickle.load(f)
    print('docs loaded.')
    
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import csv

    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    docs_embedding = model.encode(docs)
    f = open('test_predict_SBERT.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(['topic', 'doc'])
    for key in queries:
        print('{}: '.format(key), end=' ')
        sim_ary = []
        query_embedding = model.encode([queries.get(key)])
        for i in range(len(docs_embedding)):
            sim = cosine_similarity(query_embedding.reshape(1,-1), 
                                    docs_embedding[i].reshape(1,-1)).item()
            sim_ary.append(sim)
        sim_ary = np.array(sim_ary)
        sim_arg_sorted = sim_ary.argsort()[::-1][:50]
        predictFile = np.zeros(sim_arg_sorted.shape, dtype=int)
        for i in range(sim_arg_sorted.shape[0]):
            print('{}'.format(docsId[sim_arg_sorted[i]]), end=' ')
            predictFile[i] = docsId[sim_arg_sorted[i]]

        writer.writerow([key, np.array2string(predictFile).replace('\n', '')[1:-1]])
        
    f.close()
