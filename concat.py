import pandas as pd

df1 = pd.read_csv('./crawling_data/ridi_400_20250211_v3.csv')
df2 = pd.read_csv('./crawling_data/ridi_400_20250211_v4.csv')

df = pd.concat([df1, df2], ignore_index=True)
df.to_csv('./crawling_data/last.csv', index=False)