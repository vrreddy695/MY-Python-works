import pandas as pd
import xlsxwriter
daterange = pd.date_range('2016-09-17', '2016-11-25')
from ua_parser import user_agent_parser
b_pars = lambda x: user_agent_parser.ParseUserAgent(x)['family']
ndf=pd.DataFrame()
import boto3
s3 = boto3.client('s3')
for i in daterange:
    j=i.strftime("%Y%m%d")
    #pc
    obj = s3.get_object(Bucket='serp-analyzer-metadata', Key='pc/master-metadata/serp_metadata.json_Master_'+j+'.csv1')
    df = pd.read_csv(obj['Body'], sep='\t', index_col=None, header=0)
    df=df.loc[:,['UUID', 'browser','serpUrl' 'deviceId',  'memberId', 'searchEngine','folder']]
    df['searchEngine']=df['searchEngine'].str.extract('\.([^.]*)\.com',expand=True)
    df["Date"] = pd.to_datetime(df['folder'].astype(str), format='%Y%m%d')
    df["device_type"] = 'pc'
    ndf=ndf.append(df, ignore_index=True)
    #android
    obj1 = s3.get_object(Bucket='serp-analyzer-metadata', Key='android/master-metadata/serp_metadata.json_Master_'+j+'.csv')
    df1 = pd.read_csv(obj1['Body'], sep='\t', index_col=None, header=0)
    df1["device_type"] = 'android'
    #iphone
    obj2 = s3.get_object(Bucket='serp-analyzer-metadata', Key='iphone/master-metadata/serp_metadata.json_Master_'+j+'.csv')
    df2 = pd.read_csv(obj2['Body'], sep='\t', index_col=None, header=0)
    df2["device_type"] = 'iphone'
    #ipad
    obj3 = s3.get_object(Bucket='serp-analyzer-metadata', Key='ipad/master-metadata/serp_metadata.json_Master_'+j+'.csv')
    df3 = pd.read_csv(obj3['Body'], sep='\t', index_col=None, header=0)
    df3["device_type"] = 'ipad'
    for k in [df1,df2,df3]:
        k=k.loc[:,['UUID', 'browser', 'serpUrl', 'deviceId',  'memberId', 'searchEngine','folder','device_type']]
        k["browser"] =k.loc[:,"browser"].apply(b_pars)
        k['searchEngine']=k['searchEngine'].str.extract('\.([^.]*)\.com',expand=True)
        k["Date"] = pd.to_datetime(k['folder'].astype(str), format='%Y%m%d')
        ndf=ndf.append(k, ignore_index=True)
    
ndf1=ndf.groupby(['device_type','Date','searchEngine','browser']).UUID.nunique()
ndf1=ndf1.reset_index()yes
writer=pd.ExcelWriter('/home/ubuntu/vr/raw_serp_count.xlsx', engine='xlsxwriter')
ndf1.to_excel(writer, sheet_name='Sheet1', index=False)
writer.close()


vr=ndf1[ndf1['UUID'].isin(['06e6d8d4-94ff-4e89-bfb1-038bced1bb30',
'06f08677-42c6-4dd1-bbba-9af0405b859e',
'b1f6aec2-537b-47b1-92c3-9cc0e879496c',
'84021544-b3b0-437c-83a2-293f747424df',
'8be8bea0-9f87-4878-ae4a-79785c8fc1e8',
'38eee2bc-baad-4a85-9c4a-3f6136326791',
'8bf5b1b6-0211-4947-99d4-e784e727d2b1',
'6b502d95-626c-4f04-a4c4-5b32a07bc0d8',
'6c60f8f0-edf0-4346-beda-5efd1cf7f2fd',
'69d8e6ec-8bba-46da-9dea-d98fab2275cc',
'76290df8-66b6-463f-9383-002cf56e3c3a',
'934476ec-fbe4-4743-b4da-2b89f442babb',
'5812b47c-0283-43c8-92b6-5b1769260dba',
'5ec150f4-3c0c-48d4-a9ad-95e71f441708',
'67327999-f808-4f4f-bf5c-d4844f119a1e',
'68bac40a-5378-4170-9f82-c77465f3b327',
'6c54f698-a23b-4719-bd5c-0bd8e6222f43',
'7047e642-3f78-48e4-b838-538819e58b0c',
'708f36f3-c817-4113-ae28-3d2c4ce9c2ca',
'72003754-6ba0-4a26-acfc-ce02c6247990',
'75f908c5-67c4-4160-906c-39a610155822',
'76a2fc06-f1e9-4fbb-af04-f3bca8a2ea13'])]

vr=ndf1[ndf1['serpUrl'].isnull()]