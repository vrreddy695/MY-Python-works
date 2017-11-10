
import pandas as pd
df=pd.DataFrame({'name':['venkat','narsi', 'reddy'],
                 'no':[1,2,3]})
for i in range(3):
    globals()["df" + str(i+1)] = df[df['no']==(i+1)]