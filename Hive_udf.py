import sys 
import datetime
for line in sys.stdin:
	line=line.strip()
	customer_fname, customer_lname=line.split('\t')
	cl_name=customer_lname.upper()
	print '\t'.join([customer_fname, customer_lname, str(cl_name)])
	
> hive add FILE /home/cloudera/hive_udf.py
create table test as 
select 
TRANSFORM(customer_fname, Customer_lname) USING 'python hive_udf.py'  AS (fname, lname, cl_name) 
from udf_customers;
