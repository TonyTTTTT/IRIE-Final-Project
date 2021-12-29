import xml.etree.ElementTree as ET
import os
from bs4 import BeautifulSoup

class DataLoader:
    def __init__(self):
        self.query = None
        self.doc = None
        self.excludes = ['of', 'with', 'for', 'to', 'A', 'on', 'a', 'and', 'has', 'who', 'was', 'by', 'in', 'or', 'at',
                         'had', 'the', 'An', 'an', 'were', 'The', 'it', 'those', 'when', 'then', 'than', 'that', 'are',
                         'is', 'did', 'be', 'This', 'In', 'which', 'from', 'as', 'they', 'this', 'we', 'can', 'have',
                         'his', 'her', 'he', 'she', 'not', '', 'There', '\n', "a", "about", "above", "above", "across",
                         "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already",
                         "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and",
                         "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",
                         "at", "back","be","became", "because","become","becomes", "becoming", "been", "before",
                         "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill",
                         "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could",
                         "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each",
                         "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even",
                         "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify",
                         "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four",
                         "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he",
                         "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him",
                         "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest",
                         "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less",
                         "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover",
                         "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never",
                         "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing",
                         "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other",
                         "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per",
                         "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming",
                         "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six",
                         "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere",
                         "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves",
                         "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon",
                         "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through",
                         "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve",
                         "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we",
                         "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter",
                         "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while",
                         "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within",
                         "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
        self.intab = '.!?,'
        self.outtab = '    '
        self.trantab = str.maketrans(self.intab, self.outtab)

    def filterFunc(self, s):
        for exclude in self.excludes:
            if s == exclude:
                return False
        return True

    def createRoot(self, path):
        tree = ET.parse(path)
        root = tree.getroot()

        return root

    # return a list of string that is the <summary> in data at path
    def loadQuery(self, path):
        root = self.createRoot(path)
        self.query = root[2].text.split(' ')
        for i in range(len(self.query)):
            self.query[i] = self.query[i].translate(self.trantab).strip()
            # d = d.replace('\n', '')
            # for exclude in self.excludes:
            #     if d == exclude:
            #         self.query.remove(d)
        self.query = list(filter(self.filterFunc, self.query))

        return self.query

    def loadDocTxt(self, path):
        with open(path, 'r') as f:
            txt = f.read()
            cnt = 0
            while True:
                if cnt == len(txt):
                    break
                if txt[cnt] == '<':
                    while txt[cnt] != '>':
                        txt = txt[:cnt] + txt[cnt + 1:]
                    txt = txt[:cnt] + txt[cnt + 1:]
                else:
                    cnt += 1
        txt = txt.replace('\n', '').replace('\t', '')
        self.doc = txt.split(' ')
        # for d in self.doc:
        #     for exclude in self.excludes:
        #         if d == exclude:
        #             self.doc.remove(d)
        self.doc = list(filter(self.filterFunc, self.doc))

        return self.doc

    def loadDoc(self, path):
        root = self.createRoot(path)
        self.doc = []
        for node in root.iter():
            if node.text != None:
                line = node.text.replace('\n', ' ').replace('\t', '')
                for token in line.split(' '):
                    if token != '':
                        self.doc.append(token.translate(self.trantab).strip())
        # for d in self.doc:
        #     for exclude in self.excludes:
        #         if d == exclude:
        #             self.doc.remove(d)
        self.doc = list(filter(self.filterFunc, self.doc))

        return self.doc


prefix = '../../'
if __name__ == '__main__':
    dataLoader = DataLoader()

    queries = []
    for f in os.listdir(prefix + 'ntu-2021fall-ir/test_query'):
        summary = dataLoader.loadQuery(prefix + 'ntu-2021fall-ir/test_query/'+f)
        print('{}: {}'.format(f, summary))
        queries.append(summary)
    # q = dataLoader.loadQuery(prefix + 'ntu-2021fall-ir/test_query/29')
    # doc = dataLoader.loadDoc(prefix + 'ntu-2021fall-ir/doc/13915')
    # docs = []
    # for f in os.listdir(prefix + 'ntu-2021fall-ir/doc'):
    #     doc = dataLoader.loadDoc(prefix + 'ntu-2021fall-ir/doc/'+f)
    #     docs.append(doc)
    doc = dataLoader.loadDoc(prefix + 'ntu-2021fall-ir/doc/29012')
    docTxt = dataLoader.loadDocTxt(prefix + 'ntu-2021fall-ir/doc/29012')
    print('')