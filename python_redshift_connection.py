from sqlalchemy import create_engine
import psycopg2
engine = create_engine('redshift://shifu:2Lvgoofy@scooby.cbbirzec93nx.us-east-1.redshift.amazonaws.com:5439/biscuit')

df1.to_sql('vr_GetShoppingSources_06_17', engine, schema='temp', index = False, chunksize=10000)