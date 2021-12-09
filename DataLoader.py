import xml.etree.ElementTree as ET
import os


class DataLoader:
    def __init__(self):
        self.query = None
        self.doc = None
        self.excludes = ['of', 'with', 'for', 'to', 'A', 'on', 'a', 'and', 'has', 'who', 'was', 'by', 'in', 'or', 'at',
                        'had', 'the', 'An', 'an']
    def createRoot(self, path):
        tree = ET.parse(path)
        root = tree.getroot()

        return root

    # return a list of string that is the <summary> in data at path
    def loadQuery(self, path):
        root = self.createRoot(path)
        self.query = root[2].text.split(' ')
        for d in self.query:
            if d == '':
                self.query.remove('')
            for exclude in self.excludes:
                if d == exclude:
                    self.query.remove(exclude)

        return self.query

    def loadDoc(self, path):
        root = self.createRoot(path)
        self.doc = []
        for node in root.iter():
            if node.text != None:
                line = node.text.replace('\n', ' ').replace('\t', '')
                for token in line.split(' '):
                    if token != '':
                        self.doc.append(token)

        return self.doc


if __name__ == '__main__':
    dataLoader = DataLoader()

    queries = []
    for f in os.listdir('../ntu-2021fall-ir/train_query'):
        summary = dataLoader.loadQuery('../ntu-2021fall-ir/train_query/'+f)
        print('{}: {}'.format(f, summary))
        queries.append(summary)

    # doc = dataLoader.loadDoc('../ntu-2021fall-ir/doc/13915')
    docs = []
    for f in os.listdir('../ntu-2021fall-ir/doc'):
        doc = dataLoader.loadDoc('../ntu-2021fall-ir/doc/'+f)
        docs.append(doc)
