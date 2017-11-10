import pandas as pd
import csv
df=pd.read_csv('C:/Users/v-vekop/Desktop/data.csv')
len(df)

from string import maketrans
del_chars =  " ".join(chr(i) for i in range(32) + range(127, 256))
trans = maketrans(del_chars, " "*len(del_chars))
df=df.drop_duplicates(subset=['product Name', 'offers_lastupdated','offers_seller_name','offers_price'], keep='last', inplace=False)
df['offers_name'] = df["offers_name"].str.translate(trans)
len(df)

ndf=df[['product Name','offers_lastupdated', 'offers_seller_name','offers_price']].groupby(['product Name','offers_lastupdated']).size()
ndf1=ndf.reset_index()
len(ndf1)

ndf1.columns
ndf1.columns.values[2] = 'cnt' 
ndf1.head()

final= pd.merge(df, ndf1, on=['product Name', 'offers_lastupdated'],how='left')
len(final)

final1=final[final['cnt']>1]
len(final1)

final2=final1.groupby(['product Name','offers_lastupdated','offers_seller_name', 'offers_price']).size()
final2=final2.reset_index()
final2.to_csv('C:/Users/v-vekop/Downloads/results.csv', encoding='utf-8')
df.to_csv('C:/Users/v-vekop/Downloads/deduped_data.csv')