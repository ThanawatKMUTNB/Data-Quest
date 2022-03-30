import ast
import json
from textblob import TextBlob 
from datetime import datetime
from pythainlp import word_tokenize
from nltk.corpus import stopwords
import nltk
import langdetect
import tweepy as tw
import pandas as pd
import re
import glob
import os
import schedule
import time
import requests
import urllib.robotparser

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
        self.filenames = []

    def getSentimentENG(self,text):
        if TextBlob(text).sentiment.polarity > 0:
            return 'positive'
        elif TextBlob(text).sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def getSentimentTH(self,text):
        text = re.sub(r'[%]',' ',text)
        params = {'text':text}
        response = requests.get(self._url, headers=self._headers, params=params)
        try:
            polarity = str(response.json()['sentiment']['polarity'])
        except (KeyError):
            polarity = 'neutral'
        return polarity

    def formatdatetime(self,column):
        self.df[column] = pd.to_datetime(self.df[column]).dt.strftime('%Y/%m/%d') #dmY ทีหลัง
        self.df[column] = pd.to_datetime(self.df[column])
    
    def sortdf(self,columns):
        self.df.sort_values(by=columns,inplace=True)
        return self.df
        
    # def searchkeys(self,keyword):     #it on GUI
    #     self.keys = self.df['Keyword'].tolist()
    #     self.keys = list(set(self.keys))
    #     keyword = keyword.lower()
    #     if keyword in self.keys:
    #         return self.df.loc[self.df['Keyword']==keyword]
    #     else:
    #         print(f'{keyword} not in Database. Do you want to search?')
    #         Ans = str(input()).lower()
    #         if Ans == 'yes':
    #             self.keys.append(keyword)
    #             # self.savedata()
    #             # return self.df.loc[self.df['Keyword']==keyword]
    #         else:
    #             pass
    def printtest(self):
        print('eiei')

    def unionfile(self,filenames):              #type filename -> list
        self.filenames = filenames
        self._start = 0
        for file in filenames:
            df1 = pd.read_csv(file)
            if self._start != 0:
                self.df = pd.concat([self.df,df1])
                self.df.drop_duplicates(keep='last',inplace=True)
            else:
                self.df = df1
                self._start += 1
        return self.df
    
    def setnewdf(self,dataframe):
        self.df = dataframe
        return self.df
    
    def setdefaultDF(self):
        self.df = self.unionfile(self.filenames)
        return self.df

    def getperiod(self,since,until):  ####column for twitter
        self.formatdatetime('Time')
        dff = self.df
        dff.sort_values(by=['Time','Keyword'],inplace=True)
        if since == None and until != None:
            mask = (dff['Time']<=until)
        elif since != None and until == None:
            mask = (dff['Time']>=since)
        elif since != None and until != None:
            mask = (dff['Time']>=since) & (dff['Time']<=until)
        else:
            return dff
        return dff.loc[mask]

    def getrowwithkeys(self,keys):              #type keys -> list
        df = self.df
        return df.loc[df['Keyword'].isin(keys)]

    def collectwords(self,dataframe):
        nltk.download('stopwords')          #important
        en_stops = set(stopwords.words('english'))
        word = {}
        for i in dataframe['Tweet']:    #only tweet
            if langdetect.detect(i) != 'th':
                allwords = i.split()
                for w in allwords: 
                    if w not in en_stops:
                        if w in word:
                            word[w] += 1
                        else:
                            word[w] = 1
            else:
                allwords = word_tokenize(i, engine='newmm')
                for w in allwords: 
                    if w not in en_stops:
                        if w in word:
                            word[w] += 1
                        else:
                            word[w] = 1
        del word['RT']
        del word[' ']   #for thai language
        sortword = sorted(word.items(),key=lambda x:x[1],reverse=True)
        return sortword     #tuple in list
    
    def convertJsonToDataframe(self,jsonDict):
        df = pd.DataFrame.from_dict({(i,j,k): jsonDict[i][j][k] 
                           for i in jsonDict.keys() 
                           for j in jsonDict[i].keys()
                           for k in jsonDict[i][j].keys()},
                       orient='index')
        return df
    
    
    def readJson(self,path):
        with open(path,encoding = "utf-8") as f:
            # with open("WebData\\27-03-2022_20_WebJsonData.json",encoding = "utf-8") as f:
            data = json.load(f)
        # print(data)
        f.close()
        # data = json.dumps(data, indent=4)
        return data
    
    def writeCsvByDf(self,path,df):
        with open(path, 'w') as f:
            df.to_csv(path,index=True)
        print("... Save Dataframe to ",str(path)," successful.")
        
    def writeJsonByDict(self,path,dictForWrite):
            #Over write
        with open(path,"w") as f:
            json.dump(dictForWrite,f)
        f.close()
    
    def getPathToday(self,path,fileName):
        # path = "WebData"
        # path = "C:\\Users\\tongu\\Desktop\\Web-Scraping\\WebScraping\\Web-Scraping\\WebData"
        fileJsonName = fileName #self.SaveFileName
        path = os.path.join(path,(str(self.getTodayDate())+fileJsonName))
        # print(path)
        return path
    
    def getPath(self,path,fileName):
        # path = "WebData"
        # path = "C:\\Users\\tongu\\Desktop\\Web-Scraping\\WebScraping\\Web-Scraping\\WebData"
        fileJsonName = fileName #self.SaveFileName
        path = os.path.join(path,fileJsonName)
        # print(path)
        return path
    
    def readCsvToDf(self,path):
        df = pd.read_csv(path)
        return df
    
    def strOfListToList(self,strOfList):
        x = ast.literal_eval(strOfList)
        return x
    
    def searchtDF(self,df):
        df[df["Data"].str.contains('foo', regex=False)]
        
    def convertToSearch(self,dataList):
        dataList = " ".join(dataList)
        dataList = dataList.split(" ")
        resalt = []
        for i in dataList:
            # keep only letters
            res = re.sub(r'[^a-zA-Z]', '', i)
            if res != "":
                resalt.append(res)
            # print(resalt)
        return resalt
        
    def search(self,df,listOfWord):
        result = {}
        for i in listOfWord:
            result.update({str(i)+" Word Count" : 0})
        defaltDict = {'Referent' : 0, "Link" : "","Detail":"", "Sentiment" : ""}
        result.update(defaltDict)
        # defaltDict = result.copy()
        # print(defaltDict,result)
        resultdf = pd.DataFrame()
        # for i in range(len(df)):
        for i in range(100):
            defaltDict = result.copy()
            Data =self.strOfListToList(df['Data'][i])
            # print(Data)
            # checkList = self.convertToSearch(df['Data'][i])
            # print(type(df['Unnamed: 2'][i]))
            defaltDict['Referent'] = df['Ref'][i]
            defaltDict['Link'] = df['Unnamed: 2'][i]
            for j in listOfWord:
                for d in Data:
                    checkList = self.convertToSearch(d)
                    n = 1
                    # print(d)
                    # print(checkList)
                    if j in checkList:
                        defaltDict[str(j)+" Word Count"] = checkList.count(j)
                        defaltDict["Detail"] = d[0]+" : "+d[1]
                        defaltDict["Sentiment"] = self.getSentimentENG(' '.join(d))
                        n+=1
                        # print(defaltDict["Link"])
                        resultdf = pd.concat([resultdf,pd.DataFrame(defaltDict,index=[0])], ignore_index=True)
        # print(resultdf)
        return resultdf
    
    def canFetch(self,link): # False - can
        rp = urllib.robotparser.RobotFileParser()
        result = rp.can_fetch("*", link)
        return result