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

class DataManager:
    def __init__(self):
        ##-------------------- twitter --------------------##
        self._url = "https://api.aiforthai.in.th/ssense"                     
        self._headers = {'Apikey': "0kFkiFLdf4TAyY3JeUT9WVnB5naP6SjW"}
        consumer_key = "EaFU9nJw2utR0lo2PUmJE3VZy"
        consumer_secret = "DsZuVw0tEl6GHhyK08tunsOE9ICSfwplEhRDMQwB8VIqngZ6i8"
        access_token = "759317188863897600-nuwQmcYfDX8lvdRyw2eCD6fMRMkLzzZ"
        access_token_secret = 'zFFc5OJywNMBrRAblI7kFV62ZTZPHfTU1Q5kZ1cKzUupD'
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self._api = tw.API(auth, wait_on_rate_limit=True)
        self.keys = []
        self.df = None
        self._start = 0

    def getSentiment(self,text):

        if TextBlob(text).sentiment.polarity > 0:
            return 'positive'
        elif TextBlob(text).sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def formatdatetime(self,column):
        self.df[column] = pd.to_datetime(self.df[column]).dt.strftime('%Y/%m/%d')
        self.df[column] = pd.to_datetime(self.df[column])
    
    def sortdf(self,columns):
        self.df.sort_values(by=columns,inplace=True)
        return self.df
        
    def searchkeys(self,keyword):
        self.keys = self.df['Keyword'].tolist()
        self.keys = list(set(self.keys))
        keyword = keyword.lower()
        if keyword in self.keys:
            return self.df.loc[self.df['Keyword']==keyword]
        else:
            print(f'{keyword} not in Database. Do you want to search?')
            Ans = str(input()).lower()                                                  #wait for GUI
            if Ans == 'yes':
                self.keys.append(keyword)
                # self.savedata()
                # return self.df.loc[self.df['Keyword']==keyword]
            else:
                pass

    def unionfile(self,filenames):              #type filename -> list
        for file in filenames:
            df1 = pd.read_csv(file)
            if self._start != 0:
                self.df = pd.concat([self.df,df1])
                self.df.drop_duplicates(keep='last',inplace=True)
            else:
                self.df = df1
                self._start += 1
        return self.df

    def getdate(self,since,until):  ####edit
        self.df.sort_values(by=['Time','Keyword'],inplace=True)
        mask = (self.df['Time']>=since) & (self.df['Time']<=until)
        return self.df.loc[mask]
