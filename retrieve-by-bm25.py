from gensim.summarization.bm25 import BM25
import os
import numpy as np
import csv
from DataLoader import DataLoader

if __name__ == '__main__':
    dataLoader = DataLoader()

    queries = {}
    for f in os.listdir('../ntu-2021fall-ir/test_query'):
        summary = dataLoader.loadQuery('../ntu-2021fall-ir/test_query/'+f)
        # print('{}: {}'.format(f, summary))
        queries[f] = summary
        # queries.append(summary)

    docs = []
    docsId = []
    cnt = 0
    for f in os.listdir('../ntu-2021fall-ir/doc'):
        # print(f, end=' ')
        docsId.append(f)
        doc = dataLoader.loadDoc('../ntu-2021fall-ir/doc/'+f)
        docs.append(doc)
        # cnt += 1
        # if cnt == 10:
        #     break
    # print()

    # docsFor11 = []
    # testFor11 = [1892007, 2275746, 2503962, 2516438, 2688349, 2762967, 2774488, 2780824, 2785867, 2796644]
    # for f in testFor11:
    #     doc = dataLoader.loadDoc('../ntu-2021fall-ir/doc/' + str(f))
    #     docsFor11.append(doc)
    # doc = dataLoader.loadDoc('../ntu-2021fall-ir/doc/2740164')

    bm25 = BM25(docs)
    # bm25For11 = BM25(docsFor11)
    csvFile = open('test_predict.csv', 'w', newline='')
    writer = csv.writer(csvFile)
    writer.writerow(['topic','doc'])
    for key in queries:
        score = bm25.get_scores(queries.get(key))
        score = np.array(score)
        # scoreFor11 = bm25For11.get_scores(queries.get(key))
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