
#1 Given an array of integers, find the two numbers that sum up to a specific target number.

def number_combinations(list, target):
    num_combs=set()
    for i in list:
        for j in range(len(list)):
            if i+list[j]==target and i!=list[j]:
                res=(i, list[j])
                num_combs.add(tuple(sorted(res)))
    return num_combs

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
def element_counts(list):
    #create a empty dictionay to hold the elments and their counts
    freq={}
    for i in list:
        if i in freq:
            freq[i]+=1
        else:
            freq[i]=1
    return freq

sample_list=[1, 2, 3, 2, 1, 3, 2, 4, 5, 4]
print(element_counts(sample_list))


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

#12 Given a year, determine whether it is a leap year. If it is a leap year, return the Boolean True, otherwise return False.
# In the Gregorian calendar, three conditions are used to identify leap years:

# The year can be evenly divided by 4, is a leap year, unless:
# The year can be evenly divided by 100, it is NOT a leap year, unless:
# The year is also evenly divisible by 400. Then it is a leap year.
# This means that in the Gregorian calendar, the years 2000 and 2400 are leap years, while 1800, 1900, 2100

def is_leap(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False

year = int(2000)
print(is_leap(year))

#13 Write a function that can take a string and return a list of bigrams.
def string_to_bigrams(string):
    #split the senetence into words list
    words_list=string.split(' ')
    bigrams=[]
    for i in range(len(words_list)-1):
        bigrams.append((words_list[i], words_list[i+1]))
    return bigrams

string='The angry fox jump over the dog'
print(string_to_bigrams(string))

#14  Given two strings A and B, return whether or not A can be shifted some number of times to get B
def is_shifted(a, b):
    #convert string to sets
    # set doesn't allow duplication and oreder deosn't matter in sets
    a=set(a)
    b=set(b)
    if a==b:
        return True
    else:
        return False
    
a='abc'
b='cab'
print('a and b can be shifted : ', is_shifted(a, b))

#15 Given a string, return the first recurring character in it, or “None” if there is no recurring character.
def first_recurring_string(string):
    string=string.lower()
    letter_counts={}
    first_return_char='None'
    for letter in string:
        if letter in letter_counts:
            letter_counts[letter] +=1
        else:
            letter_counts[letter]=1
            
        if letter_counts[letter] > 1:
            first_return_char=letter
            return first_return_char
            break
       
name='Venkatramireddy'    
print('The first returing charector is :', first_recurring_string(name))    

#16 Write a function that takes in a list of dictionaries with both a key and list of integers, and returns a dictionary with the standard deviation of each list.
import numpy as np
def calculate_std_dev(data):
    std_dev_dict = {}
    for entry in data:
        for key, values in entry.items():
            if key=='values':
                v=round(np.std(values),2)
            else:
                k=key
        std_dev_dict[k]=v

    return std_dev_dict
       
input = [
    {
        'key1': 'list1',
        'values': [4,5,2,3,4,5,2,3],
    },
    {
        'key2': 'list2',
        'values': [1,1,34,12,40,3,9,7],
    }
]

print(calculate_std_dev(input))

#17 Given a list of stock prices in ascending order by datetime, write a function that outputs the max profit by buying and selling at a specific interval.
def max_profit(prices, dates):
    price_gain={}
    for i in range(len(prices)):
        for j in  range(len(prices)):
            if j > i:
                price_gain[prices[j] - prices[i]]=(dates[i], dates[j])

    profit_value=max(price_gain.keys())
    profit_days=price_gain[profit_value]
    profit=(profit_value, profit_days)
    return profit

stock_prices = [10,5,20,32,25,12]
dts = [
    '2019-01-01', 
    '2019-01-02',
    '2019-01-03',
    '2019-01-04',
    '2019-01-05',
    '2019-01-06',
]

print('max profit:', max_profit(stock_prices, dts))

#18 Given a dataset of test scores, write pandas code to return the cumulative percentage of students that received scores within the buckets of <50, <75, <90, <100

# Sample dataset
data = {
    'user_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'grade': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A'],
    'test_score': [80, 60, 45, 95, 70, 85, 40, 55, 90, 100]
}

import pandas as pd
df=pd.DataFrame(data)

def bucket_test_scores(df):
    bins = [0, 50, 75, 90, 100]
    labels = ["<50", "<75", "<90", "<100"]

    # converting the scores into buckets
    df["test_score"] = pd.cut(df["test_score"], bins, labels=labels, right=False)

    # Calculate size of each group, by grade and test score
    df = df.groupby(["grade", "test_score"]).size()

    # Calculate numerator and denominator for percentage
    NUM = df.groupby("grade").cumsum()
    DEN = df.groupby("grade").sum()

    # Calculate percentage, multiply by 100, and add %
    percentage = (NUM / DEN).map(lambda x: f"{int(100*x):d}%")

    # reset the index
    percentage = percentage.reset_index(name="percentage")
    return percentage


bucket_test_scores(df)



https://www.interviewquery.com/p/python-data-science-interview-questions
https://www.datacamp.com/blog/data-scientist-interview-questions

# %%
