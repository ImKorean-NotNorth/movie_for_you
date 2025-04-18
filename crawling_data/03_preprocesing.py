import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./')
df.info()

#불용어 처리 (stopword)

df_stopwords = pd.read_csv('./')
stopwords = list(df_stopwords['stopword'])

okt = Okt()
print(df.titles[0])
review = df.reviews[0]
review = re.sub('[^가-힣]',' ', review)
print(review)
tokened_review = okt.pos(review, stem=True) #원형을 바꿔줌
print(tokened_review)
df_token = pd.DataFrame(tokened_review, columns=['word','class'])
df_token = df_token[(df_token['class'] == 'Noun') | # 클래스가 명사면
                    (df_token['class'] == 'Verb') |
                    (df_token['class'] == 'Adjective')]
print(df_token)
words = []
for word in df_token.word:
    if 1 < len(word):
        if word not in stopwords:
            words.append(word)
cleaned_sentence = ' '.join(words)
cleaned_sentence.append(cleaned_sentence)

df.reviews = cleaned_sentence
df.dropna(inplace=True)
df.info()
df.to_csv('csv', index=False)