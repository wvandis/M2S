# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re #regex
import json
import urllib3
import pandas as pd 
import numpy as np 
from tqdm import tqdm

tqdm.pandas()

def dynamic_combine(row,column,total_columns):
    """dynamically combine from column till end""" 
    text=[]
    while column <= total_columns:
        t=row[column]
        column=column+1
        if len(t)>0:
            text.append(t)
    return text

def remove_df_columns(list_column):
    """remove list of columns"""
    for x in list_column:
        del df[x]
    return

# First, find the race and classes
url = 'https://www.manage2sail.com/nl-NL/search?filterYear=&filterMonth=&filterCountry=&filterClass=&filterClubId=&filterScoring=&paged=false&filterText=' 

# setting https parser
https = urllib3.PoolManager()
content = https.request('GET',url)

# beautifulsoup extracting the tbody part
soup = BeautifulSoup(content.data, "lxml")
soup = soup.tbody

# transforming into pandas df
data_list=[]
for row in soup:
    try:
        line=[]
        for d in row.get_text().splitlines():
            line.append(d)
    except:
        line=[]
    if len(line)>0:
        data_list.append(line)

df=pd.DataFrame(data_list)
df=df.fillna('')

# remove Seminars and reset index
df=df[df[5]==''].copy()
df=df.reset_index(drop=True)

# count amount of columns and dynamically combine column 11 till end
total_columns = len(df.columns)-1
from_column=11 # from which column and after it will be combined into 1 column
df.at[:,10]=df.progress_apply(lambda row: dynamic_combine(row,from_column,total_columns),axis=1)

# clean up dataframe
remove_column=[0,5,6]
while from_column <= total_columns:
    remove_column.append(from_column)
    from_column = from_column+1
remove_df_columns(remove_column)    

# add columns names   
df.columns=['Year','Start',"End",'EventName','Status','Country','City','OrganisingCommittees']


print (df)

df.to_excel('manage2sail.xlsx',sheet_name='all years')
    

