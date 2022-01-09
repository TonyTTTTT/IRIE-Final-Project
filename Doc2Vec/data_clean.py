import os.path
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import spacy
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re

'''
===============================消除stopword====================================
'''

tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')
def remove_stopwords(text, is_lower_case=False, stopwords=stopword_list):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopwords]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopwords]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

'''
===============================詞型還原及資料清理===================================
'''
def preprocess(text):
    # 詞型還原
    nlp = spacy.load("en_core_web_sm")
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])

    # 減去stopword
    text = remove_stopwords(text)
    # 減去數字
    text = re.sub(r'[0-9]+', '', text)
    # 減去空白及換行
    text = re.sub(r'[^\w^\s+]', '', text)
    text = re.sub(r"\s+", " ", text)

    return text

'''
===============================執行===================================
'''
# 設定路徑
path = 'C:/Users/Roy/PycharmProjects/2021IR/sample/train_query/'
files = os.listdir(path)

df = pd.DataFrame(columns=['Number', 'text_body'])
num = 0
a = ''

for f in tqdm(files):
    # 匯入並解析 xml 檔案
    with open(path + f, encoding="utf-8") as reader:
        xml = reader.read()

    # 移除 xml 所有標籤
    soup = BeautifulSoup(xml, "html.parser")
    text = soup.get_text()
    text = preprocess(text)

    # 把 xml 資料加入 df 矩陣
    df.loc[num] = [f, text]
    a = (a + text + '\n')

    # 計數器 + 1
    num += 1
with open("try.txt", "w+") as k:
    k.write(a)

df.to_csv("df_result.csv")
