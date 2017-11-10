import os
import pandas as pd
file_names = os.listdir("C:/Users/v-ararun/Desktop/AdCopy_text_files")
for i in file_names:
    j=i.split('.')[0]
    print i
    df = pd.read_excel(open('C:/Users/v-ararun/Desktop/AdCopy_text_files/'+i,'rb'), sheetname='Sheet1')
    for k in range(1,9):
        df.ix[:, k] = df.ix[:, k].str.replace(r'[\n\"\"\b\t\']', '')
    df.to_csv('C:/Users/v-ararun/Desktop/AdCopy_text_files/'+j+'.txt', sep='\t', index=False, encoding='utf-8')
    
mydata <- read.table('C:/vrreddy/R codes/Dec_adcopy-15.txt',  header = TRUE, fill=TRUE, sep='\t',row.names = NULL)
 mydata$ql <- nchar(as.character(mydata$query))
 d <- subset(mydata, mydata$ql > 200)
 head(d)
 
 
