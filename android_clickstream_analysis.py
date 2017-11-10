import pandas as pd
import boto3
import botocore
s3 = boto3.client('s3')
obj = s3.get_object(Bucket='serp-analyzer-metadata', Key='android/click-stream/clickstream_20160223.txt')
df = pd.read_csv(obj['Body'], sep='\t', index_col=None, header=0)

#Getting Domain from URL
from urlparse import urlparse
domain = lambda x: urlparse(x)
df['domain']=(df['request_url'].apply(domain))
df['domain']=df['domain'].apply(lambda x: x.netloc)


t=df.groupby(['domain']).member_id.nunique()
t=t.reset_index()
t.to_csv('/home/ubuntu/vr/android_domain.csv', sep=',', index=False)

