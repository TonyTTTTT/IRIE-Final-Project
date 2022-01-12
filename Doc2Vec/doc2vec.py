import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd

'''
==============================建立TaggedDocument===================================
'''
def read_corpus(fname, tokens_only=False):
    with open(fname, encoding="utf-8") as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


'''
==============================建立doc2vec訓練模型===================================
'''

def training(sentences):
    # 訓練 Doc2Vec，並保存模型：

    # 建立空模型
    model = gensim.models.doc2vec.Doc2Vec(vector_size=256, window=10, min_count=15, workers=4, epochs=40)
    model.build_vocab(sentences)
    print("開始訓練...")
    model.train(sentences, total_examples = model.corpus_count, epochs=12)

    model.save("doc2vec.model")
    print("model saved")

if __name__ == '__main__':

    # 取得訓練資料及訓練模型
    train_data = "C:/Users/Roy/PycharmProjects/2021IR/train_query.txt"
    train_corpus = list(read_corpus(train_data))
    training(train_corpus)


    # 導入訓練模型及測試資料
    model = Doc2Vec.load("doc2vec.model")
    df_train = pd.read_csv("train_query.csv",index_col=0)
    df_test = pd.read_csv("test_query.csv",index_col=0)

    # 計算 cos 並且記錄所有score
    for i in range(len(df_test["text_body"])):
        test = list(gensim.utils.simple_preprocess(df_test.at[i, "text_body"]))
        num = df_test.at[i, "Number"]

        df_train[num] = ""
        for j in range(len(df_train["text_body"])):
            train = list(gensim.utils.simple_preprocess(df_train.at[j, "text_body"]))

            # 計算 cos
            cos = model.similarity_unseen_docs(test, train)
            df_train.at[j, num] = cos
    # 儲存 cos計算結果
    df_train.to_csv("score.csv", index = False)

    # 建立 threshold 並產出最後的 result
    df_result = pd.DataFrame(columns=["topic", "doc"])
    df_result["topic"] = df_test["Number"]

    score = ""
    for n in range(len(df_test["Number"])):
        target = df_test.at[n, "Number"]
        # 排序
        df_sort = df_train.sort_values(by=[target], ascending=False)
        # 重設 index
        df_sort.reset_index(inplace=True, drop=True)

        # 取前 50 名
        for m in range(50):
            score = score + str(df_sort.at[m, "Number"]) + " "
        df_result.at[n, "doc"] = score
        score = ""
    df_result.to_csv("final_ans.csv", index = False)

