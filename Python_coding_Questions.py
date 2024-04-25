
#1 Given an array of integers, find the two numbers that sum up to a specific target number.

def number_combinations(lst, tot):
    combs=set()
    for i in lst:
        for j in range(len(lst)):
            if i+lst[j]==tot and i!=lst[j]:
                res=(i, lst[j])
                combs.add(tuple(sorted(res)))
    return combs
aint=[1,2,3,4,5,6,0,4]
number_combinations(aint, 4)


#2 Pandas joins 
import pandas as pd

# Create two sample DataFrames
df1 = pd.DataFrame({'key1': ['A', 'B', 'C', 'D'],
                    'key2': [1, 2, 3, 4],
                    'value1': [10, 20, 30, 40]})
df2 = pd.DataFrame({'key3': ['B', 'D', 'E', 'F'],
                    'key4': [3, 4, 7, 8],
                    'value2': [50, 60, 70, 80]})

# Merge the two DataFrames based on multiple keys and different key names
merged_df = pd.merge(df1, df2, left_on=['key1', 'key2'], right_on=['key3', 'key4'], how='left')[['key1',  'key2',  'value1',  'value2']]

# Display the merged DataFrame
print("Merged DataFrame:")
print(merged_df)



#3 Pandas data transpose using pivot_table method
import pandas as pd
stocks = pd.read_csv('https://gist.githubusercontent.com/alexdebrie/b3f40efc3dd7664df5a20f5eee85e854/raw/ee3e6feccba2464cbbc2e185fb17961c53d2a7f5/stocks.csv')
stocks.head()
stocks_pv=stocks.pivot_table(index='symbol', columns='date', values='volume', aggfunc='sum').reset_index()
stocks_pv.head()


#4 Calculate percentiles using numpy 
import numpy as np

# Sample data
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Calculate the 25th, 50th, and 75th percentiles
percentiles = np.percentile(data, [25, 50, 75])

print("25th percentile:", percentiles[0])
print("50th percentile (median):", percentiles[1])
print("75th percentile:", percentiles[2])

#5 Write a Python function to calculate the root mean square error (RMSE) of a machine learning model.

import numpy as np
def calculate_rmse(x, y):
    x=np.array(x)
    y=np.array(y)
    se=(x - y)**2
    mse=np.mean(se)
    rmse=round(np.sqrt(mse),2)
    return rmse

y_true = [3, -0.5, 2, 7]
y_pred = [2.5, 0.0, 2, 8]

print('RMSE is : ', calculate_rmse(y_true, y_pred))

#6 Pands create a new column using nested condtions like sql case clause 

import pandas as pd
import numpy as np

df=pd.DataFrame({'S':[1,1,2,2],'A':[1,0,1,0]})
df['Result'] = np.where((df.S == 1) & (df.A == 1), 1,   #when... then
                 np.where((df.S == 1) & (df.A == 0), 0,  #when... then
                  np.where((df.S == 2) & (df.A == 1), 0,  #when... then
                    1)))                                  #else
df

#Another way using np.select 
col         = 'consumption_energy'
conditions  = [ df2[col] >= 400, (df2[col] < 400) & (df2[col]> 200), df2[col] <= 200 ]
choices     = [ "high", 'medium', 'low' ]
    
df2["energy_class"] = np.select(conditions, choices, default=np.nan)

#7 count how many times the elment repreated in a list

lst=[1, 2, 3, 2, 1, 3, 2, 4, 5, 4]
freq={}
for i in lst:
    if i in freq:
        freq[i]+=1
    else:
        freq[i]=1

print(freq)

#8 Second largest number in a list
my_list = [10, 5, 8, 12, 7, 3, 15]
srt_list=sorted(my_list)
srt_list[len(srt_list)-2]

#9 string reverse
ch='Venkatramrieddy'
rev=''
for i in ch:
    rev=i+rev
    print(rev)

#10 Output the numbers in Triangle format?
rev=' '
for i in range(6):
    i=i+1
    rev=rev+str(i)+' '
    print(rev)

#11 Python code to print all prime numbers less than or equal to a given number, separated by an ampersand (&):

def prime_numbers(n):
    #2 is a default prime number, so lets initiate a list with 2
    prime_numbers=[2]

    # initially declarign all numbers are prime 
    for i in range(2, n+1):
        prime=True
    
    # declarign the numbers which are divisible by any other nubmer as non-prime
        j=2
        while j*j <= n:
    
            if i%j==0:
                prime=False
            j +=1
       
        if prime:
            prime_numbers.append(i)
    return '&'.join([str(x) for x in prime_numbers])

prime_numbers(20)