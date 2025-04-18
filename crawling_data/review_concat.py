import pandas as pd

df = pd.read_csv('.combine.csv')
df.dropna(inplace=True)
df.info()
print(df.head())