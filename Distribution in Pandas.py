
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import re


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[5]:


def get_list_of_university_towns():
    fo = open('university_towns.txt', "r")
    lines = fo.readlines()
    fo.close()

    # remove empty lines
    new_lines = []
    for line in lines:
        if not re.match(r'^\s*$', line):
            new_lines.append(line)

    lines = new_lines.copy()

    # Strip the white space at the beginning and end of each line
    for index, line in enumerate(lines):
        lines[index] = line.strip()

        # Loop through the lines to form a dataframe
    df_result = pd.DataFrame(columns=('State', 'RegionName'))
    i = 0  # counter for each new line in the dataframe
    state_string = ""  # Empty initial state string
    region_string = ""  # Empty initial region string
    for line in lines:
        if '[edit]' in line:
            state_string = line.replace('[edit]', "")
        else:
            region_string = re.sub(r' \(.*', "", line)
            df_result.loc[i] = [state_string, region_string]
            i += 1
    return      
    #return df_result
get_list_of_university_towns()


# In[22]:


def get_recession_start():
    #A recession is defined as starting with two consecutive quarters of GDP decline
   # '''Returns the year and quarter of the recession start time as a 
   # string value in a format such as 2005q3'''
    df = pd.read_excel('gdplev.xls',skiprows=[i for i in range(1,8)])[['Current-Dollar and "Real" Gross Domestic Product','Unnamed: 1','Unnamed: 2','Unnamed: 4','Unnamed: 5','Unnamed: 6']]
    df = df.rename(columns={'Current-Dollar and "Real" Gross Domestic Product':'Annual','Unnamed: 1':'GDP in billions of current dollars (A)','Unnamed: 2':'GDP in billions of chained 2009 dollars (A)','Unnamed: 4':'Quarterly','Unnamed: 5':'GDP in billions of current dollars','Unnamed: 6':'GDP in billions of chained 2009 dollars'})
    dff = df[['Quarterly','GDP in billions of chained 2009 dollars']]
    dff.set_index('Quarterly',inplace=True)
    rec = None
    for i in dff:
        for j in range(1,len(dff)):
            if(dff[i][j-4]<dff[i][j-3] and dff[i][j-3]>dff[i][j-2] and dff[i][j-2]>dff[i][j-1] and dff[i][j-1]>dff[i][j]):
                rec= dff[i][j-2]
    result = dff[dff['GDP in billions of chained 2009 dollars']==rec]
                
    return result.index[0]
get_recession_start()


# In[23]:


def get_recession_end():
   # A recession ending with two consecutive quarters of GDP growth.
   # '''Returns the year and quarter of the recession end time as a 
   # string value in a format such as 2005q3'''
   # Suppose q1 < q2 > q3 > q4 > q5 < q6 < q7 < q8. Then, the recession start is q3, bottom is q5 and end is q7. 
    df = pd.read_excel('gdplev.xls',skiprows=[i for i in range(1,8)])[['Current-Dollar and "Real" Gross Domestic Product','Unnamed: 1','Unnamed: 2','Unnamed: 4','Unnamed: 5','Unnamed: 6']]
    df = df.rename(columns={'Current-Dollar and "Real" Gross Domestic Product':'Annual','Unnamed: 1':'GDP in billions of current dollars (A)','Unnamed: 2':'GDP in billions of chained 2009 dollars (A)','Unnamed: 4':'Quarterly','Unnamed: 5':'GDP in billions of current dollars','Unnamed: 6':'GDP in billions of chained 2009 dollars'})
    dff = df[['Quarterly','GDP in billions of chained 2009 dollars']]
    dff.set_index('Quarterly',inplace=True)
    rec = None
    for i in dff:
        for j in range(1,len(dff)):
            if(dff[i][j-7]>dff[i][j-6] and dff[i][j-6]>dff[i][j-5] and dff[i][j-5]>dff[i][j-4] and dff[i][j-4]<dff[i][j-3] and dff[i][j-3]<dff[i][j-2] and dff[i][j-2]<dff[i][j-1] and dff[i][j-1]<dff[i][j]):
                rec= dff[i][j-2]
    result = dff[dff['GDP in billions of chained 2009 dollars']==rec]
                
    return result.index[0]       
    
get_recession_end()


# In[24]:


def get_recession_bottom():
    #'''Returns the year and quarter of the recession bottom time as a 
    #string value in a format such as 2005q3'''
    #A recession bottom is the quarter within a recession which had the lowest GDP.
    #Suppose q1 < q2 > q3 > q4 > q5 < q6 < q7 < q8. Then, the recession bottom is q5 
    df = pd.read_excel('gdplev.xls',skiprows=[i for i in range(1,8)])[['Current-Dollar and "Real" Gross Domestic Product','Unnamed: 1','Unnamed: 2','Unnamed: 4','Unnamed: 5','Unnamed: 6']]
    df = df.rename(columns={'Current-Dollar and "Real" Gross Domestic Product':'Annual','Unnamed: 1':'GDP in billions of current dollars (A)','Unnamed: 2':'GDP in billions of chained 2009 dollars (A)','Unnamed: 4':'Quarterly','Unnamed: 5':'GDP in billions of current dollars','Unnamed: 6':'GDP in billions of chained 2009 dollars'})
    dff = df[['Quarterly','GDP in billions of chained 2009 dollars']]
    dff.set_index('Quarterly',inplace=True)
    rec = None
    for i in dff:
        for j in range(1,len(dff)):
            if(dff[i][j-6]>dff[i][j-5] and dff[i][j-5]>dff[i][j-4] and dff[i][j-4]>dff[i][j-3] and dff[i][j-3]<dff[i][j-2] and dff[i][j-2]<dff[i][j-1] and dff[i][j-1]<dff[i][j]):
                rec= dff[i][j-3]
    result = dff[dff['GDP in billions of chained 2009 dollars']==rec]
                
    return result.index[0]   
     
get_recession_bottom()


# In[25]:


def convert_housing_data_to_quarters():
    #'''Converts the housing data to quarters and returns it as mean 
    #values in a dataframe. This dataframe should be a dataframe with
    #columns for 2000q1 through 2016q3, and should have a multi-index
    #in the shape of ["State","RegionName"].
    
    #Note: Quarters are defined in the assignment description, they are
    #not arbitrary three month periods.
    
    #The resulting dataframe should have 67 columns, and 10,730 rows.
    #'''
    
 #   housing = pd.read_csv('City_Zhvi_AllHomes.csv')
 #   housing.drop(['RegionID','Metro','CountyName','SizeRank'],axis=1,inplace=True)
 #   housing.set_index(['State','RegionName'],inplace=True)
 #   df = pd.DataFrame()
    
    
  #  for i in housing:
   #     print(i[4:7])
   #     if(i[4:7]=='-01' or i[4:7]=='-02' or i[4:7]=='-03'):
   #         i[4:7].replace('-01','q1')
   #         i[4:7].replace('-02','q1')
   #         i[4:7].replace('-03','q1')
  #      if(i[-1:]=='4' or i[-1:]=='5' or i[-1:]=='6'):
  #          df['Q2'] = housing[i]
  #      if(i[-1:]=='7' or i[-1:]=='8' or i[-1:]=='9'):
  #          df['Q3'] = housing[i]
  #      if(i[-1:]=='10' or i[-1:]=='11' or i[-1:]=='12'):
  #          df['Q4'] = housing[i]
  #  return housing.head()
    house = pd.read_csv('City_Zhvi_AllHomes.csv',header = 0)
    cols = [0]
    a = list(range(3,51))
    house.drop(house.columns[a],axis=1,inplace=True)
    house.drop(house.columns[0],axis=1,inplace=True)
    
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    
    house.replace({'State':states}, inplace = True)
    house.set_index(['State','RegionName'],inplace = True)
    house = house.groupby(pd.PeriodIndex(house.columns, freq='Q'), axis=1).mean()
    
    return house
convert_housing_data_to_quarters()


# In[31]:


def run_ttest():
  #  '''First creates new data showing the decline or growth of housing prices
  #  between the recession start and the recession bottom. Then runs a ttest
  #  comparing the university town values to the non-university towns values, 
  #  return whether the alternative hypothesis (that the two groups are the same)
  #  is true or not as well as the p-value of the confidence. 
    
   # Return the tuple (different, p, better) where different=True if the t-test is
    #True at a p<0.01 (we reject the null hypothesis), or different=False if 
    #otherwise (we cannot reject the null hypothesis). The variable p should
    #be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    #value for better should be either "university town" or "non-university town"
    #depending on which has a lower mean price ratio (which is equivilent to a
    #reduced market loss).
    #'''
    from scipy import stats
    start = pd.Period(get_recession_start()) #represents a period of time 
    bottom = pd.Period(get_recession_bottom())
    house = convert_housing_data_to_quarters().loc[:,[start,bottom]]
    house.columns = ["Start","Bottom"]      v                                                                                                                          
    house = house.dropna(axis=0,how="any")
    collage = get_list_of_university_towns().set_index(["State","RegionName"])
    collage["isUnv"] = "Yes"
    res = pd.merge(house,collage,how="left",left_index=True,right_index=True)
    res.isUnv = res.isUnv.fillna("No")

    res_u = res[res.isUnv == "Yes"].Ratio
    res_n = res[res.isUnv == "No"].Ratio
    #print(res_n)
    _,p = stats.ttest_ind(res_u,res_n)
    different = (True if p < 0.01 else False)
    better = ("university town" if np.nanmean(res_u) < np.nanmean(res_n) else "non-university town")
    return different, p, better
    
run_ttest()


# In[ ]:




