import pandas as pd
import xlsxwriter
import requests
from bs4 import BeautifulSoup
dates = []
entry_authors = []
titles = []
urls = []
category =[]
next_page = 'https://www.analyticsvidhya.com/blog/'
while True:
    soup = BeautifulSoup((requests.get(next_page).content),"lxml")

    # scrap the info
    v=soup.find(class_="cur-page-item row block-streams el-block-3")
    for i in v.find_all(class_="entry-date"):
        date = (i.text.strip()).encode('utf-8')
        dates.append(date)
    for i in v.find_all(class_="entry-author"):
        author = (i.text.strip()).encode('utf-8')
        entry_authors.append(author)
    for i in v.find_all('span',attrs={'class':'i-category'}):
        cat=(i.text.strip()).encode('utf-8')
        category.append(cat)
    for i in v.find_all('h3'):
        title=i.a.get('title')
        titles.append(title)
        url=i.a.get('href')
        urls.append(url)
    try:
        p=soup.find(class_="pagination")
        next_page=p.find(class_="next").get('href')
    except (AttributeError,IndexError):
        break  # exiting the loop if "Next" link not found

data=zip(dates,entry_authors,category, titles,urls)
headers=['date','author','category','title','link']
blogs=pd.DataFrame.from_records(data,columns=headers)

#converting a Pandas dataframe to an xlsx file using Pandas and XlsxWriter.
writer = pd.ExcelWriter('C:/Users/v-vekop/OneDrive/Python codes/Analytics_vidya_blogposts.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
blogs.to_excel(writer, sheet_name='Sheet1',index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.close()
