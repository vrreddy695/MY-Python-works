

import pandas as pd
import urlparse
import qgrid as v
import re
v.set_grid_option('forceFitColumns', False)
v.set_grid_option('defaultColumnWidth', 200)
import psycopg2
import os

HOST = 'scooby.cbbirzec93nx.us-east-1.redshift.amazonaws.com'
PORT = 5439 # redshift default
USER = 'shifu'
PASSWORD = '2Lvgoofy'
DATABASE = 'biscuit'

def db_connection():
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
    )
    return conn

example_query = "select * from intermediate.BING_CJ_ENCODED_URL where pageviewid='d111bbd4-3824-6cc6-03b4-a7efeceed838';"

# using pandas
import pandas as pd
conn = db_connection()
try:
    clicks = pd.read_sql(example_query, conn)

finally:
    conn.close()




fea=pd.read_excel('C:/Users/v-vekop/Desktop/click_join_investigation.xlsx', sheetname=0)
fea=fea[fea['feature_type']=='Href']



#Extracing query
def query(x):
    if x.startswith('search',1):
        parms=dict(urlparse.parse_qsl(urlparse.urlsplit(x).query))
        if 'q' in parms:
            val=parms['q']
        else:
            val=''
    elif x.startswith('http'):
        val=x.split('?')[0]
    else:
        val=x.split('?')[0]
    return val

p=lambda x:query(x)

#EXtractign FORM IG and IDparameter
f=lambda x: (re.findall(r'(?<=\FORM\%3D)+\w*|(?<=\FORM\=)+\w*',x)[0] if(len(re.findall(r'(?<=\FORM\%3D)+\w*|(?<=\FORM\=)+\w*',x))==1)else '')
g=lambda x: (re.findall(r'\IG=(.*?)\&',x)[0] if(len(re.findall(r'\IG=(.*?)\&',x))==1)else '')
i=lambda x: (re.findall(r'(?<=ID=SERP,)+\d+\.?\d*',x)[0] if(len(re.findall(r'(?<=ID=SERP,)+\d+\.?\d*',x))==1)else '')



fea['q']=fea['feature_value'].apply(p)
fea['FORM']=fea['feature_value'].apply(f)
fea['IG']=fea['feature_value'].apply(g)
fea['feature_value']=fea['feature_value'].str.replace('\[comma\]', ',')
fea['ID']=fea['feature_value'].apply(i)


fea


#Extracing query
def cl_query(x):
    parms=dict(urlparse.parse_qsl(urlparse.urlsplit(x).query))
    if 'q' in parms:
        val=parms['q']
    elif 'url' in parms:
        val=re.findall(r'\q=(.*?)\&', parms['url'])[0]
    else:
        val=''
   
    return val

c_q=lambda x:cl_query(x)



clicks['q']=clicks['header_text_or_referrer_url'].apply(c_q)
clicks['FORM']=clicks['header_text_or_referrer_url'].apply(f)
clicks['IG']=clicks['header_text_or_referrer_url'].apply(g)
clicks['feature_value']=clicks['header_text_or_referrer_url'].str.replace('\[comma\]', ',')
clicks['ID']=clicks['header_text_or_referrer_url'].apply(i)



clicks=clicks[clicks['q']!='']




len(clicks)


# In[ ]:



