from string import punctuation
from bs4 import BeautifulSoup
import os
from nltk.corpus import stopwords

corpus_file = open("../corpus/all", mode="w+")
map_file = open("../corpus/map", mode="w+")


path = "../data/doc/"
files = os.listdir("../data/doc")

translator = str.maketrans(",().\n\t", "      ")

count = 0
li = []
for w in stopwords.words('english'):
    li.append(" " + w + " ")

for file in files:
    with open(path+file) as fp:
        soup = BeautifulSoup(fp, "xml")
        tr = soup.get_text().translate(translator)
        for w in li:
           tr = tr.replace(w, " ")
        corpus_file.write(tr)
        corpus_file.write('\n')
        map_file.write(file + " " + str(count))
        map_file.write('\n')
    print(count)
    count += 1
