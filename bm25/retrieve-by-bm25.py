import pickle
from gensim.summarization.bm25 import BM25
import os
import numpy as np
import csv
from DataLoader import DataLoader

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
    with open('docs.pkl', 'rb') as f:
        docs = pickle.load(f)
    with open('docsId.pkl', 'rb') as f:
        docsId = pickle.load(f)
    # docs = []
    # docsId = []
    # cnt = 0
    # for f in os.listdir(prefix + 'ntu-2021fall-ir/doc'):
    #     # print(f, end=' ')
    #     docsId.append(f)
    #     doc = dataLoader.loadDocTxt(prefix + 'ntu-2021fall-ir/doc/'+f)
    #     docs.append(doc)
    #     # cnt += 1
    #     # if cnt == 100:
    #     #     break
    # # print()
    print('docs loaded.')

    # dict(sorted(bm25.doc_freqs[0].items(), key=lambda item: item[1], reverse=True))

    print('start matching...')
    bm25 = BM25(docs, b=1, k1=1.5)
    csvFile = open('test_predict_new_stop_word_b1.csv', 'w', newline='')
    writer = csv.writer(csvFile)
    writer.writerow(['topic','doc'])
    for key in queries:
        score = bm25.get_scores(queries.get(key))
        score = np.array(score)
        print('{}: '.format(key), end=' ')
        predict = np.flip(score.argsort())[:50]
        predictFile = np.zeros(predict.shape, dtype=int)
        cnt = 0
        for score in predict:
            print('{}'.format(docsId[score]), end=' ')
            predictFile[cnt] = docsId[score]
            cnt += 1
        print()
        writer.writerow([key, np.array2string(predictFile).replace('\n', '')[1:-1]])
        # print('{}: {}'.format(key, scoreFor11))
    csvFile.close()
    print('complete! ')
