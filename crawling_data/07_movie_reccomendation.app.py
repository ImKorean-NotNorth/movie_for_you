import sys
from audioop import reverse
from encodings.punycode import selective_find

from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import QStringListModel

form_window = uic.loadUiType('./ui')

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUI(self)
        self.Tfidf_matrix = mmread('./models/Tf~').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f: # 매트릭스 둘다 불러들임 tfidf
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load(',/models/word2vec_movie_re~~')

        self.df_reviews = pd.read_csv('./review')
        self.titles = list(self.df_reviews.titles)
        self.titles.sort()
        # self.cb_title.addItem('test01')
        # self.cb_title.addItem('test02')
        for title in self.titles:
            self.cb_title.addItem(title)

        self.cb_title.currentIndexChanged.connect(self.combobox_slot)
        self.btn_recommend.clicked.connect(self.btn_slot)

    def btn_slot(self):
        keyword = self.le_keyword.text()
        recommendation = self.recommendation_by_keyword(keyword)
        # self.lbl_recommendation.setText(recommendation) # 확인
        if keyword in titles:
            recommendation = self.recommendation_by_title(keyword)
        else:
            recommendation = self.recommendation_by_keyword(keyword)
        if recommendation:
            self.lbl_recommendation.setText(recommendation)

    def combobox_slot(self):
        title = self.cb_title.currentText()
        print(title)
        recommendation = self.recommendation_by_title(title)
        self.lbl_recommendation.setText(recommendation)

    # title 기반 추천 함수
    def recommendation_by_title(self, title):  # 영화제목 받으면 코사인값 구해서 넘겨줌
        movie_idx = self.df_reviews[self.df_reviews.titles == title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation)) #줄띄우기
        return recommendation

    # keyword 기반 추천 함수
    def recommendation_by_keyword(self, keyword):
        try:
            sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
        except:
            self.lbl_recommend.set_Text('제가 모르는 단어에요 ㅜㅜ')
            return 0

    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        movieIdx = [i[0] for i in simScore]
        recmovieList= self.df_reviews.iloc[movieIdx, 0]
        return recmovieList[1:11]


if __name__ == '__name__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())