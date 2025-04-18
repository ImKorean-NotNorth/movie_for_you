from multiprocessing.connection import families

import pandas as pd
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc('font', family='NanumBrunGothic') # 공짜폰트!

df = pd.read.csv(./craw)
words = df.iloc[0, 1].split() # 문자열 함수중 스플릿함수 띄워쓰기 기준으로 잘라서 단어들의 리스트를 만들어줌
print(words)

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict) #몇번 반복되는지... 키 벨류 쌍으로 딕셔너리 형태로 만들어줌 그러나 딕셔너리는 아님

wordcloud_img = WordCloud(
    background_color = 'white',)
