#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 18:45:49 2021

@author: r09922176
"""
import os
from DataLoader import DataLoader
import pickle

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
    print('docs loaded.')
    
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    docs_embedding = model.encode(docs)
    
    for query in queries:
        sim_ary = []
        query_embedding = model.encode(query)
        for i in range(len(docs_embedding)):
            sim = cosine_similarity(query_embedding.reshape(1,-1), 
                                    docs_embedding[i].reshape(1,-1))
            sim_ary.append(sim)
        