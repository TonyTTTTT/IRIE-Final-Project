from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

model = Doc2Vec(corpus_file="../corpus/all", vector_size=100, window=3, min_count=2, workers=24)

model.save("../models/vs100_window3_min2")
