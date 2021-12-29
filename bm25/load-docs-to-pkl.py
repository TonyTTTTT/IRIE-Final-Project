import os
from DataLoader import DataLoader
import pickle


prefix = '../../'
dataLoader = DataLoader()
print('loading docs...')
docs = []
docsId = []
cnt = 0
for f in os.listdir(prefix + 'ntu-2021fall-ir/doc'):
    # print(f, end=' ')
    docsId.append(f)
    doc = dataLoader.loadDocTxt(prefix + 'ntu-2021fall-ir/doc/' + f)
    docs.append(doc)
    # cnt += 1
    # if cnt == 100:
    #     break
# print()
print('docs loaded.')
with open('docs.pkl', 'wb') as f:
    pickle.dump(docs, f)