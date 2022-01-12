import os.path
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import spacy
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re


#===============================消除stopword====================================


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


#===============================詞型還原及資料清理===================================

def preprocess(text):
    # 詞型還原
    spacy.require_cpu()
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

#==============================執行doc資料前處理==========================

# 設定路徑
path_doc = 'C:/Users/Roy/PycharmProjects/2021IR/sample/doc/'
files_doc = os.listdir(path_doc)

df_doc = pd.DataFrame(columns=['Number', 'text_body'])
num = 0
a = ''

for f in tqdm(files_doc):
    # 匯入並解析 xml 檔案
    with open(path_doc + f, encoding="utf-8") as reader:
        xml = reader.read()

    # 移除 xml 所有標籤
    soup = BeautifulSoup(xml, "html.parser")
    text = soup.get_text()
    text = preprocess(text)

    # 把 xml 資料加入 df 矩陣
    df_doc.loc[num] = [f, text]
    a = (a + text + '\n')

    # 計數器 + 1
    num += 1
with open("train_query.txt", "w+", encoding='UTF-8') as k:
    k.write(a)
df_doc.to_csv("train_query.csv")


#===============================執行test資料前處理===================================

# 設定路徑
path_test = 'C:/Users/Roy/PycharmProjects/2021IR/sample/test_query/'
files_test = os.listdir(path_test)

df_test = pd.DataFrame(columns=['Number', 'text_body'])
num = 0
a = ''

for f in tqdm(files_test):
    # 匯入並解析 xml 檔案
    with open(path_test + f, encoding="utf-8") as reader:
        xml = reader.read()

    # 移除 xml 所有標籤
    soup = BeautifulSoup(xml, "html.parser")
    text = soup.get_text()
    text = preprocess(text)

    # 把 xml 資料加入 df 矩陣
    df_test.loc[num] = [f, text]
    a = (a + text + '\n')

    # 計數器 + 1
    num += 1
with open("test_query.txt", "w+", encoding='UTF-8') as k:
    k.write(a)
df_test.to_csv("test_query.csv")
