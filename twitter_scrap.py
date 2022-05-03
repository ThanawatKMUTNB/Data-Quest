from textblob import TextBlob 
from datetime import datetime
import tweepy as tw
import pandas as pd
import re
import glob
import os
import schedule
import time
import requests
from tqdm import tqdm

class Twitter_Scrap:
    def __init__(self):

        #twitter api
        consumer_key = "EaFU9nJw2utR0lo2PUmJE3VZy"
        consumer_secret = "DsZuVw0tEl6GHhyK08tunsOE9ICSfwplEhRDMQwB8VIqngZ6i8"
        access_token = "759317188863897600-nuwQmcYfDX8lvdRyw2eCD6fMRMkLzzZ"
        access_token_secret = 'zFFc5OJywNMBrRAblI7kFV62ZTZPHfTU1Q5kZ1cKzUupD'
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._api = tw.API(auth, wait_on_rate_limit=True)

        #thai api
        self._url = "https://api.aiforthai.in.th/ssense"                     
        self._headers = {'Apikey': "vIQAf35aRkc7QUbR1fTPvzvtkqtSKAaz"}

        self.df = None
        self.keys = []

    def setdataframe(self,df):
        self.df = df
        self.keys = self.df['Keyword'].tolist()
        self.keys = list(set(self.keys))

    
    def getSentiment(self,text):                #sentiment english from score

        if TextBlob(text).sentiment.polarity > 0:
            return 'positive'
        elif TextBlob(text).sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def extract_hashtags(self,text):
        regex = "#(\w+)" 
        hashtag_list = re.findall(regex, text)
        return hashtag_list

    def remove_url(self,txt):
        return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())
    
    def remove_url_th(self,txt):
        return " ".join(re.sub("([^\u0E00-\u0E7Fa-zA-Z' ]|^'|'$|''|(\w+:\/\/\S+))", "", txt).split())

    def get_related_tweets(self,key_word,until):

        tweet_keyword = []                          #set list
        twitter_users = []
        twitter_users_location = []
        tweet_hashtag = []
        tweet_time = []
        tweet_string = [] 
        tweet_countRT = []
        tweet_fav = []
        tweet_sentiment = []
        tweet_polarity = []
        tweet_language = []
        for tweet in tw.Cursor(self._api.search_tweets,
                                q=key_word,
                                tweet_mode="extended",
                                until=until,
                                include_entities=True).items(10):                           #loop cursor each keyword (get 10 tweet)
                                
            if(tweet.lang == 'en'or tweet.lang == 'th'):                                    #collect only english and thai language
                twitter_users.append(tweet.user.screen_name)
                twitter_users_location.append(tweet.user.location)
                tweet_time.append(tweet.created_at)
                tweet_countRT.append(tweet.retweet_count)
                tweet_fav.append(tweet.favorite_count)
                tweet_keyword.append(key_word)
                tweet_hashtag.append(str(self.extract_hashtags(tweet.full_text)))
                tweet_language.append(tweet.lang)
                if tweet.lang == 'en':
                    tweet_string.append(self.remove_url(tweet.full_text))
                    tweet_polarity.append(self.getSentiment(tweet.full_text))
                    tweet_sentiment.append(TextBlob(tweet.full_text).sentiment.polarity)
                elif tweet.lang == 'th':
                    tweet_string.append(self.remove_url_th(tweet.full_text))
                    text = re.sub(r'[%]',' ',tweet.full_text)                                   #remove % in tweet
                    params = {'text':text}
                    response = requests.get(self._url, headers=self._headers, params=params)
                    try:
                        polarity = str(response.json()['sentiment']['polarity'])                #get polarity from api for thai
                        sentiment = str(response.json()['sentiment']['score'])
                    except (KeyError):
                        polarity = 'neutral'
                        sentiment = 0
                    tweet_polarity.append(polarity)
                    tweet_sentiment.append(sentiment)

        self.df = pd.DataFrame({'Keyword':tweet_keyword,'User':twitter_users,'Tweet': tweet_string,'Language':tweet_language, 'Time': tweet_time,'User Location':twitter_users_location,
                            'Hashtag':tweet_hashtag,'Polarity':tweet_polarity,'Likes':tweet_fav,'Retweet':tweet_countRT,'Sentiment':tweet_sentiment})       #set dataframe

        
        self.df['Time'] = pd.to_datetime(self.df['Time']).dt.strftime('%Y-%m-%d')
        #self.df['Time'] = pd.to_datetime(self.df['Time'])
        folder = "collectkeys"
        path = str(folder+'/'+key_word)
        days = list(set(self.df['Time'].tolist()))
        if key_word not in self.keys:
            
            if not os.path.exists(path):    
                os.mkdir(path)              #create floder for keyword
            for d in days:
                dfff = self.df.loc[self.df['Time'].isin([d])]
                dfff.to_csv(path+'/'+key_word+'_'+d+'.csv',encoding='utf-8',index=False)
            print('save new file complete')
        else:
            print('save old key')
            allfilepath = glob.glob(str(str(os.getcwd())+"\\collectkeys\\"+key_word+"\\*.csv"))
            filenames = []
            for filepath in allfilepath:                                            #get all filenames
                filenames.append(os.path.basename(filepath))                        
            for d in days:
                dfff = self.df.loc[self.df['Time'].isin([d])]                       #get row range this date
                csvname = str(path+'/'+key_word+'_'+d+'.csv')                       #file path
                if str(key_word+'_'+d+'.csv') in filenames:                         #duplicate file
                    print('have this file')
                    olddf = pd.read_csv(csvname)
                    newdf = pd.concat([dfff,olddf])
                    newdf.drop_duplicates(keep='last',inplace=True)
                    os.remove(csvname)
                    newdf.to_csv(csvname,encoding='utf-8',index=False)
                else:
                    dfff.to_csv(csvname,encoding='utf-8',index=False)                #create new file
            print('save file complete')
        return self.df

