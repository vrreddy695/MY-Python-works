
drop table temp.vr_test_2017_07;
create table temp.vr_test_2017_07 as (
select
date(serp_capture_time) as dt,
serp_id,
Query,
engine,
impression_position,
translate(max(case when feature_name='PLA_AdContent' then feature_value else null end), '[comma]', ',')as product,
translate(max(case when feature_name in ('PLA_Ad_PriceContent','PLA_AdPriceContent' ) then feature_value else null end),'[comma]', ',')as price,
translate(max(case when feature_name ='PLA_MerchantContent' then feature_value else null end), '[comma]', ',')as seller
From analysis.features
where date(serp_capture_time) between '2017-01-01' and '2017-06-30'
and device_type='pc'
and feature_name in ('PLA_AdContent', 'PLA_Ad_PriceContent','PLA_MerchantContent', 'PLA_AdPriceContent')
and impression_position like('GridPosition%')
group by 1,2,3,4,5
order by 1,2,3,4,5);

drop table temp.vr_query_cat;
create table temp.vr_query_cat as(
select  
query, 
case when clothesandshoes=1 then 'clothesandshoes' 
     when commerce=1 then 'commerce'
     else 'consumerelectronics' end as category,
     max(load_time) as load_time
from analysis.query_categorization
where clothesandshoes=1 or commerce=1 or consumerelectronics=1
group by 1,2);

create table temp.vr_PLA_listings as (select 
category, a.* 
From temp.vr_test_2017_07 as a
inner join temp.vr_query_cat as b 
on a.query=b.query);

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

example_query = "select * from temp.vr_test_2017_07 order by serp_id"

# using pandas
import pandas as pd
conn = db_connection()
try:
    df = pd.read_sql(example_query, conn)
finally:
    conn.close()

df1=df.drop_duplicates(subset=['dt','serp_id','product_name', 'engine','impression_position', 'feature_name'])
df2=df1.set_index(['dt','serp_id','product_name', 'engine','impression_position', 'feature_name']).unstack('feature_name').reset_index()
df2.columns = df2.columns.droplevel()

df2.columns.values[0]='date'
df2.columns.values[1]='serp_id'
df2.columns.values[2]='product_name'
df2.columns.values[3]='engine'
df2.columns.values[4]='grid_pos'
df2.columns.values[5]='act_product'
df2.columns.values[6]='price'
df2.columns.values[7]='seller'

