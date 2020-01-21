import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans

df = pd.read_csv('imdb.csv',escapechar='\\')
df1=pd.read_csv('diamonds.csv')
df2=pd.read_csv('movie_metadata.csv')

#1. Generate a report that tracks the various Genere combinations for each type year on year. The result data frame should contain type, Genere_combo, year, avg_rating, min_rating, max_rating,total_run_time_mins

def gt_k(my_d):
    for key,value in my_d.items():
        s=[]
        for i,j in value.items():
            if(j>0):
                s.append(i[0])
        genre_dic[key]=s
    return genre_dic


def bonus_01(df):
    grp=df.groupby(['type','year']).agg([np.sum]) 
    grp1=grp.loc[:,"Action":].transpose()
    grp_dict=grp.to_dict()
    genre_dic={}     
    genre_dic=gt_k(grp1)
    s = pd.Series(genre_dic)
    
    movie_data = df.groupby(['type','year']).agg({'imdbRating': [min,max, np.mean],'duration':(sum)})
    movie_data['Genre_combo']= s
    movie_data['duration']=movie_data['duration']/60
    movie_data=movie_data.rename(columns={"min": "min_rating", "max": "max_rating","mean":"avg_rating","duration":
                                          "total_run_time_mins","sum":"","imdbRating":"Rating"})
    return movie_data

#2. Is there a realation between the length of a movie title and the ratings ? Generate a report that captures the trend of the number of letters in movies titles over years. We expect a cross tab between the year of the video release and the quantile that length fall under. The results should contain year, min_length, max_length, num_videos_less_than25Percentile, num_videos_25_50Percentile ,num_videos_50_75Percentile, num_videos_greaterthan75Precentile

def per_25(df,cr):
    res = sum(1 for i in df if i>0 and i<=cr) 
    return res

def per(df,cr1,cr2):
    res = sum(1 for i in df if i>cr1 and i<=cr2) 
    return res

def bonus_02(df):
    df['Length']=df['wordsInTitle'].str.len()
    df2=pd.DataFrame(columns=['Len','Rate'])
    
    df2['Len']=df['Length']
    df2['Rate']=df['imdbRating']
    df2['Rate'].fillna(0,inplace=True)
    df2['Len'].fillna(0,inplace=True)
    df2['Len/10']=df2['Len']/10
    print(df[['Length','imdbRating']].corr())
    print("\n")
    df['quantile']=df['Length'].quantile()
    print(pd.crosstab(df['year'],df['quantile']))
    print("\n")
    d=pd.DataFrame()
    d=df[['year', 'Length']].groupby('year').quantile().reset_index().rename(columns={"Length": "quantile"})
    print(pd.crosstab(d['year'],d['quantile']))
    print("\n")
    kmeans = KMeans(n_clusters=4).fit(df2)
    y_kmeans= kmeans.predict(df2)
    plt.scatter(df2.iloc[:, 2], df2.iloc[:, 1], c=y_kmeans, s=10,cmap='viridis')
    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 2], centers[:, 1], c='black', s=20, alpha=1.0)
    plt.xlabel('Length')
    plt.ylabel('imdbRating')
    plt.title('Length of movie title Vs Its imdbRating')

    b=pd.DataFrame(columns=
                   ['no_of_movies','maximum_length','minimum_length','25_percentile','50_percentile','75_percentile','100_percentile'])
    df['Length'].fillna(0,inplace=True)
    b['no_of_movies']=df.groupby('year')['Length'].count()

    b['maximum_length']=df.groupby('year')['Length'].max()
    b['minimum_length']=df.groupby('year')['Length'].min()
    b['25_percentile']=df.groupby('year')['Length'].apply(lambda x:per_25(x,np.percentile(x,25)))
    b['50_percentile']=df.groupby('year')['Length'].apply(lambda x:per(x,np.percentile(x,25),np.percentile(x,50)))
    b['75_percentile']=df.groupby('year')['Length'].apply(lambda x:per(x,np.percentile(x,50),np.percentile(x,75)))
    b['100_percentile']=df.groupby('year')['Length'].apply(lambda x:per(x,np.percentile(x,75),np.percentile(x,100)))
    
    return b

#3. In diamonds data set Using the volumne calculated above, create bins that have equal population within them. Generate a report that contains cross tab between bins and cut. Represent the number under each cell as a percentage of total.
def volume(df):
    df['z'] = pd.to_numeric(df.z, errors='coerce')
    return np.where(df['depth']>=60,df.x*df.y*df.z,8)

def bonus_03(df):
    a=volume(df)
    df['bin'] = pd.qcut(a, q=6)
    df1=np.array(df['bin'].value_counts())
    t=pd.crosstab(df.bin,df.cut)
    print(t,"\n")
    i=0
    r=pd.DataFrame()
    for i in range(len(df1)):
        r[i]=(t.loc[i]/df1[i])*100
    return r.transpose()

#4. Generate a report that tracks the Avg. imdb rating quarter on quarter, in the last 10 years, for movies that are top performing. You can take the top 10% grossing movies every quarter. Add the number of top performing movies under each genere in the report as well.

def bonus_04(df):
    df1=df.sort_values(by=['title_year','gross'],ascending=False).groupby("title_year").agg({'title_year':'count'})
    df1.columns=['count']
    df1=df1.sort_values(by=['title_year'],ascending=False)
    n = 10
    i=0
    j=0
    result1=pd.DataFrame()
    for i in range(0,10):
        result=pd.DataFrame()
        df2=df.iloc[j:j+int(df1.iloc[i])]
        result['year']=df2.head(int(df1.iloc[i]*(n/100)))['title_year']
        result['movie_name']=df2.head(int(df1.iloc[i]*(n/100)))['movie_title']
        result['genres']=df2.head(int(df1.iloc[i]*(n/100)))['genres']
        result['gross']=df2.head(int(df1.iloc[i]*(n/100)))['gross']
        j=j+int(df1.iloc[i])
        result1=pd.concat([result1,result])
        result2=result1.groupby('year')
    return result1
        

#5. Bucket the movies into deciles using the duration. Generate the report that tracks various features like nomiations, wins, count, top 3 geners in each decile.
def bonus_05(df):
    df['decile']=pd.qcut(df["duration"], 10, labels=False)
    g=df.groupby('decile').agg([np.sum]).loc[:,"Action":]
    
    i=0.0
    li=[]
    for y in range(0,10):
        g1=g.sort_values(by=i,axis=1, ascending=False)
        g1.columns = g1.columns.map('_'.join)
        a=list(g1.columns[:3])
        li.append(a)
        i=i+1
        
    df1=pd.Series(li)

    df2=df.groupby('decile').agg({'nrOfNominations':'sum','nrOfWins':'sum','imdbRating':'count'}).rename(columns={'nrOfNominations':'nomination','nrOfWins':'wins','imdbRating':'count'}) 
    df2['top3_genres']=df1
    return df2
    