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

    def getheader(self):
        return self.df.columns.tolist()
    
    def getSentiment(self,text):

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

        tweet_keyword = []
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
                                include_entities=True).items(10):
                                
            if(tweet.lang == 'en'or tweet.lang == 'th'):
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
                    text = re.sub(r'[%]',' ',tweet.full_text)
                    params = {'text':text}
                    response = requests.get(self._url, headers=self._headers, params=params)
                    try:
                        polarity = str(response.json()['sentiment']['polarity'])
                        sentiment = str(response.json()['sentiment']['score'])
                    except (KeyError):
                        polarity = 'neutral'
                        sentiment = 0
                    tweet_polarity.append(polarity)
                    tweet_sentiment.append(sentiment)

        self.df = pd.DataFrame({'Keyword':tweet_keyword,'User':twitter_users,'Tweet': tweet_string,'Language':tweet_language, 'Time': tweet_time,'User Location':twitter_users_location,
                            'Hashtag':tweet_hashtag,'Polarity':tweet_polarity,'Likes':tweet_fav,'Retweet':tweet_countRT,'Sentiment':tweet_sentiment})

        self.df['Time'] = pd.to_datetime(self.df['Time']).dt.strftime('%Y/%m/%d')
        #self.df['Time'] = pd.to_datetime(self.df['Time'])

        return self.df

    def savedata(self,keyword,until): #keyword is list

        current_time = datetime.now().strftime("%H:%M:%S")
        print('\nstart saving @',current_time)
        #today = datetime.today()
        #filename = str("tweet_data_"+str(today.day)+str(today.month)+str(today.year)+".csv")

        # if filename not in glob.glob("*.csv"):
        #     self.df = pd.DataFrame(columns=['Keyword','User','Tweet','Language','Time','User Location','Hashtag','Polarity','Likes','Retweet','Sentiment'])
        # else:
        #     self.df = pd.read_csv(filename)

        for kw in keyword:
            self.df = pd.concat([self.df,self.get_related_tweets(kw,until)])

        self.df.drop_duplicates(keep='last',inplace=True)
        self.df.sort_values(by=['Keyword'],inplace=True)
        # if filename in glob.glob("*.csv"):
        #     os.remove(filename)
        # self.df.to_csv(filename,encoding='utf-8',index=False)
        current_time = datetime.now().strftime("%H:%M:%S")
        print('save complete @',current_time)

    def searchkeys(self,keyword,Ans,until):   #keyword's type is list
        #print('keyword',keyword,'\nkeys',self.keys,'\nkeyword in keys?',keyword in self.keys)
        # if "" in keyword:
        #     return self.df
        
        if len(keyword) > 1:            #>1 keyword
            dhave = []
            for key in keyword:
                if key not in self.keys:
                    dhave.append(key)
            print(keyword)
            print(dhave)
            if len(dhave) > 0:          #search new keyword
                self.keys.extend(dhave)
                self.savedata(dhave,until)
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
            elif Ans == "real":
                self.savedata(keyword,until)
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
            else:
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
        elif keyword[0] in self.keys:   #seach 1 key
            if Ans == "real":
                self.savedata(keyword,until)
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
            else:
                return self.df.loc[self.df['Keyword']==keyword[0]]
        else:                           #1keyword (new)
            if Ans == 'yes':            #search new key
                self.keys.extend(keyword)
                self.savedata(keyword,until)
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
            elif Ans == "real":
                self.savedata(keyword,until)
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
            else:
                print('You select NO')
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
            


# df = pd.read_csv('tweet_data_742022.csv')
# twsc = Twitter_Scrap()
# twsc.setdataframe(df)
# print(set(twsc.df['Keyword'].tolist()))
# print(twsc.searchkeys('spy x family','yes'))
# print(set(twsc.df['Keyword'].tolist()))
