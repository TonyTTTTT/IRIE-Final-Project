import xml.etree.ElementTree as ET
import os


class DataLoader:
    def __init__(self):
        self.query = None
        self.doc = None
        self.excludes = ['of', 'with', 'for', 'to', 'A', 'on', 'a', 'and', 'has', 'who', 'was', 'by', 'in', 'or', 'at',
                         'had', 'the', 'An', 'an', 'were', 'The', 'it', 'those', 'when', 'then', 'than', 'that', 'are',
                         'is', 'did', 'be', 'This', 'In', 'which', 'from', 'as', 'they', 'this', 'we', 'can', 'have',
                         'his', 'her', 'he', 'she', 'not', '', 'There']
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
        self.query = root[1].text.split(' ')
        for d in self.query:
            d = d.translate(self.trantab).strip()
            if d == '':
                self.query.remove('')
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

    # queries = []
    # for f in os.listdir(prefix + 'ntu-2021fall-ir/train_query'):
    #     summary = dataLoader.loadQuery(prefix + 'ntu-2021fall-ir/train_query/'+f)
    #     print('{}: {}'.format(f, summary))
    #     queries.append(summary)
    q = dataLoader.loadQuery(prefix + 'ntu-2021fall-ir/test_query/29')
    # doc = dataLoader.loadDoc(prefix + 'ntu-2021fall-ir/doc/13915')
    # docs = []
    # for f in os.listdir(prefix + 'ntu-2021fall-ir/doc'):
    #     doc = dataLoader.loadDoc(prefix + 'ntu-2021fall-ir/doc/'+f)
    #     docs.append(doc)
    doc = dataLoader.loadDoc(prefix + 'ntu-2021fall-ir/doc/29012')
    docTxt = dataLoader.loadDocTxt(prefix + 'ntu-2021fall-ir/doc/29012')
    print('')
