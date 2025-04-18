import pandas as pd
import glob

from Movie_Crawling import movie_title

data_paths = glob.glob('./crawling_data/movie_reviews_500_movies/*')
print(data_paths)

df = pd.DataFrame()
df_temp = pd.read_csv(data_paths[0])
print(df_temp.head())
titles = []
reviews = []
old_title = ''

for j in range(len(df_temp)):

for i in range(len(df_temp)):

    title = df_temp.iloc[i, 0]
    if title != old_title:
        old_title = title
        df_movie = df_temp[(df_temp.movie_title == title)]
        review = ''.join(df_movie.review)
        reviews.append(review)

        reviews.append(review)
print(titles)
print(reviews)

df_batch = pd.DataFrame({'titles' : titles, 'reviews' : reviews})
df_batch.info()

pd.concat([df, df_batch], ignore_index=True)
df.info()
df.to_csv('./crawling_data/movie_reviews_500_movies/*',index = False)
