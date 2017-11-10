import pandas as pd
import xlsxwriter
daterange = pd.date_range('2016-01-01', '2016-12-31')
from ua_parser import user_agent_parser
b_pars = lambda x: user_agent_parser.ParseUserAgent(x)['family']
ndf=pd.DataFrame()
import boto3
import botocore
s3 = boto3.client('s3')
for i in daterange:
    try:
        j=i.strftime("%Y%m%d")
        #android
        obj = s3.get_object(Bucket='serp-analyzer-metadata', Key='android/master-metadata/serp_metadata.json_Master_'+j+'.csv')
        df = pd.read_csv(obj['Body'], sep='\t', index_col=None, header=0)
        df=df.loc[:,['UUID', 'deviceId',  'memberId', 'searchEngine','folder']]
        df['searchEngine']=df.loc[:,'searchEngine'].str.extract('\.([^.]*)\.com',expand=True)
        df["Date"] = pd.to_datetime(df['folder'].astype(str), format='%Y%m%d')
        df['mnth_yr'] = df.loc[:,'Date'].apply(lambda x: x.strftime('%Y-%m'))
        df["device_type"] = 'Android'
        df=df.groupby(['mnth_yr','Date']).agg({'UUID':pd.Series.nunique,
                                                         'deviceId':pd.Series.nunique,
                                                         'memberId':pd.Series.nunique
                                                                    })
        df=df.reset_index()
        ndf=ndf.append(df, ignore_index=True)
    except botocore.exceptions.ClientError:
        print '%s date file is missing' % j
ndf.to_csv('/home/ubuntu/vr/android_rawserp_counts_2016.csv', sep=',', index=False)