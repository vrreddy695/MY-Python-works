import pandas as pd
import xlsxwriter
daterange = pd.date_range('2015-01-01', '2015-12-31')
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
    df=df.loc[:,['UUID', 'browser', 'deviceId',  'memberId', 'searchEngine','folder']]
    df['searchEngine']=df['searchEngine'].str.extract('\.([^.]*)\.com',expand=True)
    df["Date"] = pd.to_datetime(df['folder'].astype(str), format='%Y%m%d')
    df['mnth_yr'] = df.loc[:,'Date'].apply(lambda x: x.strftime('%Y-%m'))
    df["device_type"] = 'pc'
    df=df.groupby(['mnth_yr','Date','browser']).agg({'UUID':pd.Series.nunique,
                                                     'deviceId':pd.Series.nunique,
                                                     'memberId':pd.Series.nunique
                                                                })
    df=df.reset_index()
    ndf=ndf.append(df, ignore_index=True)
ndf.to_csv('/home/ubuntu/vr/pc_rawserp_counts_2015.csv', sep=',', index=False)
ndf['avge_serps']=ndf.loc[:,'UUID']/ndf.loc[:,'memberId']
summary=ndf[(ndf.browser!='Unknown')].groupby(['mnth_yr','browser']).agg({'avge_serps':{'mean_serps':'mean',
                                                                                  'std_serps':'std'
                                                                                  },
                                                                          'memberId':{'members_mean':'mean',
                                                                                  'members_std':'std'
                                                                                  }
                                                                          })
summary.reset_index()

