# import pandas, numpy
import pandas as pd 
import numpy as np
from datetime import datetime
import matplotlib  
matplotlib.use('TkAgg')   
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
# Create the required data frames by reading in the files
df_sales=pd.read_excel(open('SaleData.xlsx','rb'))
df_imdb=pd.read_csv('imdb.csv',escapechar="\\")
df_diamonds=pd.read_csv('diamonds.csv',error_bad_lines=False)
df_movie=pd.read_csv('movie_metadata.csv',,escapechar="\\")
# Q1 Find least sales amount for each item
# has been solved as an example
def least_sales(df):
    # write code to return pandas dataframe
	ls = df.groupby(["Item"])["Sale_amt"].min().reset_index()
	return ls

# Q2 compute total sales at each year X region
def sales_year_region(df):
    # write code to return pandas dataframe
    df['OrderDate']=[i.year for i in df['OrderDate']]
    ls= df.groupby(["Region","OrderDate"])["Sale_amt"].sum().reset_index()
    return ls

# Q3 append column with no of days difference from present date to each order date
def days_diff(df):
    # write code to return pandas dataframe
    df['dateDiff']=[datetime.now()-i for i in df['OrderDate']]
    return df
    pass

# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
def mgr_slsmn(df):
    # write code to return pandas dataframe
    dfx={}
    for i in range(len(df['Manager'])):
    	if df['Manager'][i] not in dfx:
    		dfx[df['Manager'][i]]=[df['SalesMan'][i]]
    	else:
    		dfx[df['Manager'][i]].append(df['SalesMan'][i])
    keys={}
    keys['manger']=[key for key in dfx]
    keys['listOfSalesPerson']=[dfx[key] for key in dfx]
    dfx=pd.DataFrame(keys)
    return dfx
    pass

# Q5 For all regions find number of salesman and number of units
def slsmn_units(df):
    # write code to return pandas dataframe
    dfx=df.groupby(['Region'])['SalesMan'].nunique().reset_index()
    dfy=df.groupby(['Region'])['Units'].nunique().reset_index()
    return dfx,dfy
    pass

# Q6 Find total sales as percentage for each manager
def sales_pct(df):
    # write code to return pandas dataframe
    dfx=df.groupby(['Manager'])['Sale_amt'].sum().reset_index()
    Xt=[]
    sales=sum(df['Sale_amt'])
    for i in dfx['Sale_amt']:
    	Xt.append(i*100/sales)
    dfx['percentage']=Xt
    return dfx

# Q7 get imdb rating for fifth movie of dataframe
def fifth_movie(df):
	# write code here
	return df['imdbRating'][4]
	pass

# Q8 return titles of movies with shortest and longest run time
def movies(df):
	# write code here
	ls=df['duration'].min()
	hs=df['duration'].max()
	print (df['title'][np.where(df['duration']==ls)[0][0]])
    print(df['title'][np.where(df['duration']==hs)[0][0]])
    
# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
def sort_df(df):
	# write code here
	return df.sort_values(['year','imdbRating'],ascending=[1,0])

# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
def subset_df(df):
	# write code here
    result = df[(df['gross'] > 20000000) & (df['budget'] < 10000000) & (df['duration'] >= 30) & (df['duration'] <= 180)]
    return result
	pass

# Q11 count the duplicate rows of diamonds DataFrame.
def dupl_rows(df):
	# write code here
	dups = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0:'count'})
	return dups['count'].sum() - dups.shape[0]
	pass

# Q12 droping those rows where any value in a row is missing in carat and cut columns
def drop_row(df):
	# write code here
	#df=df[pd.notnull(df['carat'])]
	#df=df[pd.notnull(df['cut'])]
    df2 = df.dropna(axis=0,subset=['carat','cut'])
    return df2
	return df

# Q13 subset only numeric columns
def sub_numeric(df):
	# write code here
    df3 = df._get_numeric_data()
    return df3
	pass

# Q14 compute volume as (x*y*z) when depth > 60 else 8
def volume(df):
	# write code here
    df['z']=pd.to_numeric(df.z,errors='coerce')
    df['volume']=np.where(df['depth']>60,df.x*df.y*df.z,8)
    return df

# Q15 impute missing price values with mean
def impute(df):
	# write code here
	return df['price'].fillna((df['price'].mean()))
	pass

