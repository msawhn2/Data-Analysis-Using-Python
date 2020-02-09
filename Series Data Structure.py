
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[1]:


import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[2]:


# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]
    # You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 


# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[3]:


def answer_one():
    #df['country'] = df.index
    g = df['Gold']
    r = g.max()
    max_gold = (df[df['Gold'] ==r])
    return (max_gold.index[0])
answer_one()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[4]:


def answer_two():
    g = df['Gold'] - df['Gold.1']
    r = g.max()
    max_diff = (df[df['Gold'] - df['Gold.1'] == r])
    return (max_diff.index[0])
answer_two()


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[5]:


def answer_three():
    a_c=(df[(df['Gold']>0) & (df['Gold.1']>0)])
    g = (a_c['Gold'] - a_c['Gold.1']) / a_c['Gold.2']
    r = g.max()
    new_series = (((a_c['Gold'] - a_c['Gold.1']) / a_c['Gold.2'])==r)
    
    return a_c[new_series].index[0]

answer_three()
    
    


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created, with the country names as indices.
# 
# *This function should return a Series named `Points` of length 146*

# In[77]:


import pandas as pd
def answer_four():
    points = df['Gold.2']*3 + df['Silver.2']*2 + df['Bronze.2']*1    
    return points
answer_four()


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2015/co-est2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[7]:


census_df = pd.read_csv('census.csv')
census_df.head()


# In[8]:


def answer_five():
    df_filtered = census_df[census_df['SUMLEV'] == 50]
    state_df = pd.DataFrame()
    state_df['State'] = df_filtered['STNAME'].unique()
    state_df['CountyCnt'] = 0
    #state_df.set_index('State',inplace=True)
    
    for st in df_filtered['STNAME'].unique() :
    
    #This is counting the number of counties for each state name in df_filtered equal to state
        stcount = len(df_filtered['CTYNAME'][df_filtered['STNAME'] == st]) 
    #This is adding to the county count column of state_df with matching states and assigning it a value of stcount
        state_df['CountyCnt'].loc[st] =stcount
    
    return state_df['CountyCnt'].argmax()    #returns the row label of the max column 

answer_five()


# ### Question 6
# **Only looking at the three most populous counties for each state**, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 
# *This function should return a list of string values.*

# In[ ]:


def answer_six():
    df=census_df[census_df['SUMLEV'] == 50]
    df1=df.sort(['STNAME','POPESTIMATE2015'],ascending=False).groupby('STNAME').head(3).copy()
    df2 = df1.reset_index().groupby("STNAME").sum().sort(['POPESTIMATE2015'],ascending=False).head(3).copy()
    return list(df2.index.values)
        
        
        
        
    return county_df
answer_six()


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

# state_df = pd.DataFrame(census_df['STNAME'].unique())
#     pop = census_df['CENSUS2010POP']
#     #make one column of the state_df to be "state names " that you can get from census_df
#   #make another column for "Total_top_3" counties
# 
# 
#     for state in state_df.index: 
#      find the 3 most populous counties
# 
#     #find all counties in that state
#     #sort those counties by pop
#      add the top 3 counties
#     store that in "Total_top_3" 
#     
# #after you do this for each state, sort the state_df by "Total_top_3", then find the corresponding state name

# In[9]:


import numpy as np
def answer_seven():
    
    df_filtered =  census_df[census_df['SUMLEV'] == 50]
    
    state_df = pd.DataFrame()
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    state_df['CTYNAME'] = df_filtered['CTYNAME']
    state_df['pop10'] = df_filtered['POPESTIMATE2010']
    state_df['pop11'] = df_filtered['POPESTIMATE2011']
    state_df['pop12'] = df_filtered['POPESTIMATE2012']
    state_df['pop13'] = df_filtered['POPESTIMATE2013']
    state_df['pop14'] = df_filtered['POPESTIMATE2014']
    state_df['pop15'] = df_filtered['POPESTIMATE2015']
    for i in state_df:
        df = state_df.T.loc['pop10':]
        df['max10'] = state_df['pop10'].max()
        df['max11'] = state_df['pop11'].max()
        df['max12'] = state_df['pop12'].max()
        df['max13'] = state_df['pop13'].max()
        df['max14'] = state_df['pop14'].max()
        df['max15'] = state_df['pop15'].max()
        df['min10'] = state_df['pop10'].min()
        df['min11'] = state_df['pop11'].min()
        df['min12'] = state_df['pop12'].min()
        df['min13'] = state_df['pop13'].min()
        df['min14'] = state_df['pop14'].min()
        df['min15'] = state_df['pop15'].min()
        df2['max'] = df.max()
        df2['min'] = df.min()
        df2['diff'] = df2['max'] - df2['min']
        df2['CTYNAME'] = state_df['CTYNAME']
        
    #The code below is is finding the index where the difference is maximum and returning thee county name and since 
    # we just want the string another max() is used outside
    return  df2.loc[df2["diff"] == df2["diff"].max(), "CTYNAME"].max() 
    
answer_seven()


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# 
# 
# 
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[24]:


def answer_eight():
    df_filtered = census_df[census_df['SUMLEV'] == 50]
    state_df = df_filtered[(df_filtered['REGION']==2) | (df_filtered['REGION']==1)]
    state_filtered = state_df[state_df['CTYNAME']=='Washington County']
    popestimate = state_filtered[state_filtered['POPESTIMATE2015']> state_filtered['POPESTIMATE2014']]
    popestimate.set_index('STNAME')
    return popestimate[['STNAME','CTYNAME']]
answer_eight()

