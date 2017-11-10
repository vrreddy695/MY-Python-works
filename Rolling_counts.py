import pandas as pd
df = pd.read_csv('/home/vekoppula/sample.gz', compression='gzip', header=0, sep=',', quotechar='"')
df.columns=['slr_id', 'byr_id', 'item_id','site_id', 'rfrl_gnrtn_ts', 'model_score_num', 'min_flagged_dt', 'flagged',  'tm_diff', 'first_flag_yn','final_ms','ck_out_flag']

#rolling coutn function
def rolling_count(val):
    if val == rolling_count.previous:
        rolling_count.count +=1
    else:
        rolling_count.previous = val
        rolling_count.count = 1
    return rolling_count.count
rolling_count.count = 0 #static variable
rolling_count.previous = None #static variable

df1['message_cnt'] = df1['low_thresh_flag'].apply(rolling_count) #new column in dataframe
df1.sort_values(['slr_id', 'byr_id','item_id', 'site_id', 'rfrl_gnrtn_ts'])
df1['count2']=(df1['message_cnt'].shift(1)-df1['message_cnt'] ) 
df1['count3']=df1['count2'].shift(-1)
lst_recs=df1.groupby(['slr_id','byr_id','item_id','site_id']).last().reset_index()
lst_recs=lst_recs[lst_recs['model_score_num'] < 0.5]
df2=df1[df1['count3']>=1]

frames=[df2, lst_recs]
final_data=pd.concat(frames)

final_data.sort_values(['byr_id','slr_id', 'item_id','site_id', 'rfrl_gnrtn_ts']);
final_data=final_data.drop_duplicates()


