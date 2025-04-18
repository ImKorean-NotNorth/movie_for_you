import pandas as pd
from PIL.GimpGradientFile import linear
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
from gensim.models import Word2Vec



def getRecommendation(cosine_sim):
    simScore = lis(enumerate(cosine_sim[-1])) # sorting 하면 인덱스 섞임 enum으로정렬
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True) # 큰값부터 작은값 정렬
    simScore = simScore[:11] # 그 중 11개 , 자기자신 포함 11개
    movieIdx = [i[0] for i in simScore]
    recmovieList = df_reviews.iloc[movieIdx, 0]
    return recmovieList[1:11] # 0번은 자기자신 1번부터 10번까지 10개

df_reviews = pd.read_csv('./')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

df_reviews.info()

# 영화 index 이용
# ref_idx = 10 # 인덱스 10번
# print(df_reviews.iloc[ref_idx, 0]) # 콜론 번호 영화제목
# conine_sim = linear_kernel(Tfidf_matrix[ref_idx], Tfidf_matrix) # 10번의 벡터값 , 546개의 영화와의 벡터값
# # 코사인 유사도 구해서 -> 프린트해서 라벨에 출력해야함 (앱이니까 )
# print(conine_sim[:5])
# print(len(conine_sim))
# recommendations = getRecommendation(conine_sim)
# print(recommendations)

# key word 이용 (두개 중 하나 써야함) = 유사도 순으로 정렬함
embedding_model = Word2Vec.load('./models/word2vec.model')
keyword = '사랑'
sim_word = embedding_model.wv.most_similar(keyword, topn=10)
words = [keyword]
    for word, _ in sim_word:
        words.append(word)
        print(words)
    else :
        print('not in')
        exit()
sentence = []
count = 10
for word in words:
    sentence = sentence + [word] * count
    count -= 1
sentence = ' '.join(sentence)
print(sentence)

sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix) # Tfidf_matrix 500개의 영화 코사인값
recommendation = getRecommendation(cosine_sim)

print(recommendation)