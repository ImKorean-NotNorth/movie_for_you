import pandas as pd
from gensim.models import Word2Vec

df_reviews = pd.read_csv('./cleaned_reviews.csv')
df_reviews.info() # db확인
reviews = list(df_reviews.reviews)
print(reviews[0]) # 전처리 데이터 확인
tokens = [] # 형태소 단위로 나눈 리스트 생성
for sentence in reviews:
    token = sentence.split()
    tokens.append(token)
print(tokens[0]) #형태소 단위로 다시 자름

embedding_model = Word2Vec(tokens, vector_size=100, window=4, min_count=20, workers=4, epochs=100, sg=1)
# 형태소 준것, vector_size=100 / 4= 4단어씩 잘라서 workers4=4 ->코어몇개쓸것이냐 / min_count = 최소 20번 중복적으로 나와야 학습
# 맵찍어보면 1192개만 학습!
embedding_model.save('./model/word2vec_moive_review.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))
