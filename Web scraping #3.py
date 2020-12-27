#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import pandas as pd
import html.parser 
import urllib.request
import re
import numpy as np
from urllib.parse import urljoin
import pandas as pd


# In[2]:


html_page = urllib.request.urlopen("http://catalog.northeastern.edu/graduate/professional-studies/masters-degree-programs/#programstext")


# In[3]:


soup = BeautifulSoup(html_page, "html.parser")


# In[4]:


test3 = []
for test in soup.findAll("div", {"id": "programstextcontainer"}):
    for test2 in test.findAll('a'):
        test3.append(test2.get('href'))


# In[5]:


url_base = ['http://catalog.northeastern.edu/graduate']


# In[6]:


a =[]
for x in test3:
    for y in url_base:
        url = urljoin(y, x)
        a.append(url)
        print(url)


# In[7]:


urls = a.copy()


# In[8]:


urls


# In[9]:


#results_df = pd.DataFrame() #<-- initialize a results dataframe to dump/store the data you collect after each iteration
for url in urls:   
    my_url = requests.get(url) 
    html = my_url.content
    soup = BeautifulSoup(html,'html.parser')
    for soups in soup:
        test = soup.findAll(re.compile(r'(tr|h1|h2|h3)')) #<-- regular expression https://stackoverflow.com/questions/20648660/python-beautifulsoup-give-multiple-tags-to-findall
        for codecol in test: 
            print(codecol.get_text())


# In[10]:


rows = []
for url in urls:   
    my_url = requests.get(url) 
    html = my_url.content
    soup = BeautifulSoup(html,'html.parser')
    for soups in soup:
        test = soup.findAll(re.compile(r'(tr|h1|h2|h3)')) #<-- regular expression https://stackoverflow.com/questions/20648660/python-beautifulsoup-give-multiple-tags-to-findall
        for codecol in test: 
            rows.append([codecol.get_text()])


# In[11]:


print(rows)


# In[12]:


result = [[rows.strip() for rows in inner] for inner in rows] #<-- https://stackoverflow.com/questions/13071053/python-removing-whitespace-from-string-in-a-list
result


# In[13]:


df = pd.DataFrame(result[1:], columns=test[0])
print(df)


# In[14]:


df.head()


# In[15]:


pd.options.display.max_rows = 100


# In[16]:


df.head(n=100)


# In[17]:


df.columns = ['raw_data']


# In[18]:


df.count


# In[19]:


df.head()


# In[20]:


#df = df.reindex(columns = df.columns.tolist() + ['degree name','crn','units'])


# In[21]:


df['units'] = df["raw_data"].str[-1:]   


# In[22]:


df


# In[23]:


df.dtypes['units']


# In[24]:


#https://datatofish.com/string-to-integer-dataframe/
df['units'] = pd.to_numeric(df['units'],errors='coerce') 


# In[25]:


df


# In[26]:


condition = df['raw_data'].str[0:8]
#https://guillim.github.io/pandas/2018/10/22/Pandas-if-else-on-columns.html


# In[27]:


df['crn'] = np.where(df['units'] >= 1, condition , '')


# In[28]:


df.head(n=50)


# In[29]:


condition_1 = df['raw_data'].str[8:].str[:-1]


# In[30]:


df['course'] = np.where(df['crn'] != '', condition_1, '')


# In[31]:


df.head(n=100)


# In[32]:


condition_2 = df.raw_data.shift(-1)


# In[33]:


df['program_name'] = np.where(df['raw_data']== 'Download Catalog PDF Files', condition_2, '')


# In[34]:


df.drop(df.head(6).index, inplace=True)


# In[35]:


df.head(n=20)


# In[36]:


df['program_name'] = df['program_name'].replace('', np.nan).ffill()
#df1 = df.replace(np.nan, '', regex=True)
#df.replace(r'^\s*$', np.nan, regex=True)


# In[37]:


df.head(n=50)


# In[42]:


crn.str.strip()


# In[41]:


df.head(n=5)


# In[40]:


df.to_csv('cps_webscrap.csv')


# In[ ]:


#https://stackoverflow.com/questions/27905295/how-to-replace-nans-by-preceding-values-in-pandas-dataframe


# In[ ]:





# In[ ]:





# In[ ]:




