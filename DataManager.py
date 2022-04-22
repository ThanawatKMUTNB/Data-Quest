import ast
from collections import Counter
from csv import DictWriter, writer
import csv
import json
from operator import index
from unittest import result
from numpy import choose
from textblob import TextBlob 
from datetime import datetime, timedelta
from pythainlp import word_tokenize
from nltk.corpus import stopwords
import nltk
import langdetect
import tweepy as tw
import pandas as pd
import re
import glob
import string
import os
import time
import shutil
import requests
import urllib.robotparser
import webScraping as web
from langdetect import detect
from pythainlp.corpus import thai_stopwords

class DataManager:
    def __init__(self):
        ##-------------------- twitter --------------------##
        self._url = "https://api.aiforthai.in.th/ssense"                     
        self._headers = {'Apikey': "kE7s0TJ00spb9kEPZ1BC7w8A16dpy8Cr"}
        consumer_key = "EaFU9nJw2utR0lo2PUmJE3VZy"
        consumer_secret = "DsZuVw0tEl6GHhyK08tunsOE9ICSfwplEhRDMQwB8VIqngZ6i8"
        access_token = "759317188863897600-nuwQmcYfDX8lvdRyw2eCD6fMRMkLzzZ"
        access_token_secret = 'zFFc5OJywNMBrRAblI7kFV62ZTZPHfTU1Q5kZ1cKzUupD'
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._api = tw.API(auth, wait_on_rate_limit=True)
        self.keys = os.listdir("collectkeys")
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
        # print(text)
        text = re.sub(r'[%]',' ',text)
        # print(text)
        params = {'text':text}
        # print(json.dumps(params, sort_keys=False, indent=4))
        try:
            response = requests.get(self._url, headers=self._headers, params=params)
            try:
                polarity = str(response.json()['sentiment']['polarity'])
            except (KeyError):
                polarity = 'neutral'
        except :
            polarity = 'URI too long'
            pass
        return polarity

    def formatdatetime(self,column):
        self.df[column] = pd.to_datetime(self.df[column]).dt.strftime('%Y/%m/%d')
        self.df[column] = pd.to_datetime(self.df[column])
    
    def sortdf(self,columns):
        self.df.sort_values(by=columns,inplace=True)
        return self.df

    def unionfile(self,filenames):              #type filename -> list
        self._start = 0
        self.filenames = filenames
        for file in filenames:
            df1 = pd.read_csv(file)
            if self._start != 0:
                self.df = pd.concat([self.df,df1])
                self.df.drop_duplicates(keep='last',inplace=True)
            else:
                self.df = df1
                self._start += 1
        self.keys = list(set(self.df['Keyword'].tolist()))
        self.collectfile()
        return self.df
    
    def newUnion(self):
        path=os.getcwd()
        keys = []
        start = 0
        for f in glob.glob(path+'/collectkeys/*'):
            keyname = os.path.split(f)[-1]
            keys.append(keyname)
        for k in keys:
            for file in glob.glob(path+'/collectkeys/'+k+'/*.csv'):
                if start == 0:
                    self.df = pd.read_csv(file)
                    start +=1
                else:
                    dff = pd.read_csv(file)
                    self.df = pd.concat([self.df,dff])
        self.keys = keys
        #self.collectfile()
        return self.df
    
    def setnewdf(self,dataframe):
        self.df = dataframe
        return self.df
    
    def concatfile(self,dataframe):
        self.df = pd.concat([self.df,dataframe])
        self.df.drop_duplicates(keep='last',inplace=True)
        self.df.sort_values(by=['Keyword'],inplace=True)
        self.formatdatetime('Time')
        return self.df
    
    def setdefaultDF(self):
        #self.df = self.unionfile(self.filenames)
        self.df = self.newUnion()
        return self.df
    
    def collectfile(self):
        self.df["Time"] = pd.to_datetime(self.df["Time"]).dt.strftime('%Y-%m-%d')
        keys = list(set(self.df['Keyword'].tolist()))
        folder = "collectkeys"
        if not os.path.exists(folder):
            os.mkdir(folder)    
        for key in keys:
            path = str(folder+'/'+key)
            dff = self.df.loc[self.df['Keyword'].isin([key])]
            days = list(set(dff['Time'].tolist()))
            if not os.path.exists(path):
                os.mkdir(path)
            for d in days:
                dfff = dff.loc[dff['Time'].isin([d])]
                dfff.to_csv(path+'/'+key+'_'+d+'.csv',encoding='utf-8',index=False)
        print('collect complete')

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
        #print(dataframe)
        nltk.download('stopwords')          #important
        dataframe = dataframe.reset_index()
        th_stopwords = list(thai_stopwords())
        en_stops = set(stopwords.words('english'))
        en_stops.update(list(string.ascii_lowercase))
        en_stops.update(list(string.ascii_uppercase))
        en_stops.update(['0','1','2','3','4','5','6','7','8','9'])
        word = {}
        for index,row in dataframe.iterrows():    #only tweet
            if row['Language'] == 'en':
                allwords = str(row['Tweet']).split()
                for w in allwords: 
                    if w not in en_stops:
                        if w in word:
                            word[w] += 1
                        else:
                            word[w] = 1
            elif row['Language'] == 'th':
                allwords = word_tokenize(row['Tweet'], engine='newmm')
                for w in allwords: 
                    if w not in th_stopwords:
                        if w in word:
                            word[w] += 1
                        else:
                            word[w] = 1
            else:
                pass
        if 'RT' in word:
            del word['RT']  #for twitter
        if ' ' in word:
            del word[' ']   #for thai language
        sortword = sorted(word.items(),key=lambda x:x[1],reverse=True)
        worddf = pd.DataFrame(sortword,columns=['Word','Count'])
        return worddf   #word dataframe
        #return sortword     #tuple in list
    
    def deletekeyword(self,keyword):
        path=os.getcwd()
        for k  in keyword:
            shutil.rmtree(path+'//collectkeys//'+k+'//')
            self.keys.remove(k)
            #self.df.drop(self.df[self.df['Keyword']==k].index,inplace = True)
            self.df = self.newUnion()
        return self.df
    
    def convertJsonToDataframe(self,jsonDict):
        df = pd.DataFrame.from_dict({(i,j,k): jsonDict[i][j][k] 
                           for i in jsonDict.keys() 
                           for j in jsonDict[i].keys()
                           for k in jsonDict[i][j].keys()},
                       orient='index')
        return df
    
    def getReadByDateList(self,Sdate):
        DList = []
        for root, dirs, files in os.walk(r'WebData'):
            for name in files:
                if Sdate in str(name): 
                    DList.append(name)
                    # DList.append(os.path.abspath(os.path.join(root, name)))
                    # print(os.path.abspath(os.path.join(root, name)))
        return DList
    
    def readJson(self,path):
        with open(path, 'r') as f:
            contents = json.loads(f.read())
        # data = json.dumps(data, indent=4)
        return contents
    
    def writeCsvByDf(self,path,df):
        with open(path, 'w') as f:
            df.to_csv(path,index=True)
        print("... Save Dataframe to ",str(path)," successful.")
        
    def writeJsonByDict(self,path,dictForWrite):
            #Over write
        with open(path,"w") as f:
            json.dump(dictForWrite,f)
        f.close()
    
    # def getPathToday(self,path,fileName):
    #     # path = "WebData"
    #     # path = "C:\\Users\\tongu\\Desktop\\Web-Scraping\\WebScraping\\Web-Scraping\\WebData"
    #     fileJsonName = fileName #self.SaveFileName
    #     path = os.path.join(path,(str(self.getTodayDate())+fileJsonName))
    #     # print(path)
    #     return path
    
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
        
    # def convertToSearch(self,dataList):
    #     dataList = " ".join(dataList)
    #     dataList = dataList.split(" ")
    #     resalt = []
    #     for i in dataList:
    #         # keep only letters
    #         res = re.sub(r'[^a-zA-Z]', '', i)
    #         if res != "":
    #             resalt.append(res)
    #         # print(resalt)
    #     return resalt
        
    # def search(self,df,listOfWord):
    #     result = {}
    #     for i in listOfWord:
    #         result.update({str(i)+" Word Count" : 0})
    #     defaltDict = {'Referent' : 0, "Link" : "","Detail":"", "Sentiment" : ""}
    #     result.update(defaltDict)
    #     # defaltDict = result.copy()
    #     # print(defaltDict,result)
    #     resultdf = pd.DataFrame()
    #     # for i in range(len(df)):
    #     for i in range(100):
    #         defaltDict = result.copy()
    #         Data =self.strOfListToList(df['Data'][i])
    #         # print(Data)
    #         # checkList = self.convertToSearch(df['Data'][i])
    #         # print(type(df['Unnamed: 2'][i]))
    #         defaltDict['Referent'] = df['Ref'][i]
    #         defaltDict['Link'] = df['Unnamed: 2'][i]
    #         for j in listOfWord:
    #             for d in Data:
    #                 checkList = self.convertToSearch(d)
    #                 n = 1
    #                 # print(d)
    #                 # print(checkList)
    #                 if j in checkList:
    #                     defaltDict[str(j)+" Word Count"] = checkList.count(j)
    #                     defaltDict["Detail"] = d[0]+" : "+d[1]
    #                     defaltDict["Sentiment"] = self.getSentimentENG(' '.join(d))
    #                     n+=1
    #                     # print(defaltDict["Link"])
    #                     resultdf = pd.concat([resultdf,pd.DataFrame(defaltDict,index=[0])], ignore_index=True)
    #     # print(resultdf)
    #     return resultdf
    
    def canFetch(self,link): # False - can
        rp = urllib.robotparser.RobotFileParser()
        result = rp.can_fetch("*", link)
        return result
    
    def date_range(self,start, end):
        print(start, end)
        dateS = datetime.strptime(str(start),'%d-%m-%Y')
        dateE = datetime.strptime(str(end),'%d-%m-%Y')
        delta = dateE - dateS  # as timedelta
        days = [dateS + timedelta(days=i) for i in range(delta.days + 1)]
        resualt = [] 
        for i in days:
            resualt.append(str(i.day).zfill(2)+"-"+str(i.month).zfill(2)+"-"+str(i.year))
        # print(resualt)
        return resualt

    # start_date = datetime(2008, 8, 1)
    # end_date = datetime(2008, 8, 3)
    
    def paragraphToList (self,paragraph):
        nltk.download('stopwords')          #important
        en_stops = set(stopwords.words('english'))
        word = {}
        if langdetect.detect(paragraph) != 'th':
                allwords = paragraph.split()
                for w in allwords: 
                    if w not in en_stops:
                        if w in word:
                            word[w] += 1
                        else:
                            word[w] = 1
        else:
            allwords = word_tokenize(paragraph, engine='newmm')
            for w in allwords: 
                if w not in en_stops:
                    if w in word:
                        word[w] += 1
                    else:
                        word[w] = 1
        # del word['RT']
        # del word[' ']   #for thai language
        sortword = sorted(word.items(),key=lambda x:x[1],reverse=True)
        return sortword     #tuple in list
    
    def getCountCsvLine(self,path):
        file = open(path, encoding="utf8")
        reader = csv.reader(file)
        lines= len(list(reader))
        return lines
    
    def setStartInfo(self):
        df = {
                'Date' : '',
                'Keyword' : '',
                'Word Count' : '',
                "Ref" : 0,
                "Link" : '',
                "Data" : '',
                "Sentiment" : '',
                'Lang' : '',
                "Ref Link" : ''
                }
        return pd.DataFrame(df, index=[0])
    
    def writeCsvByList(self,path,dataList):
        # Open file in append mode
        with open(path, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(dataList)
            print("... Save List to ",path,"  successful.")
    
    def append_dict_as_row(file_name, dict_of_elem, field_names):
        # Open file in append mode
        with open(file_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            dict_writer = DictWriter(write_obj, fieldnames=field_names)
            # Add dictionary as wor in the csv
            dict_writer.writerow(dict_of_elem)
            print("... Save Dict to ",file_name,"  successful.")
            
    def creatNewSearchFile(self,path):
        field_names = ['Date','Keyword','Word Count','Ref','Link','Title','Data','Sentiment','Lang','Ref Link']
        with open(path, 'a+', newline='', encoding="utf8") as f: 
            write = csv.writer(f) 
            write.writerow(field_names)
            f.close()
    
    def addNewWord(self,NewWord,dateAdd): #List NewWord
        print("----------",NewWord,dateAdd)
        startDate = dateAdd[0]
        endDate = dateAdd[1]
        ListOfDate = self.date_range(str(startDate.isoformat()),str(endDate.isoformat()))
        path = "web search"
        todayByFile = os.listdir(path)
        
        #Add new word to all date
        for i in todayByFile:
            for kw in NewWord:
                newpath = os.path.join('web search',i,kw+'.csv')
                self.creatNewSearchFile(newpath)
        
        #Choosed Date
        chooseDate = []
        for i in ListOfDate:
            if i in todayByFile:
                chooseDate.append(i)
        
                
            # self.setDataByAllKeyword(i)
            
    def setDictSentiment(self,soup,link,data,today):
        ex = web.webScraping()
        resualtDict = {}
        keyword = os.listdir("collectkeys")
        try:
            wc = self.paragraphToList(data)
            
            stm = ''
            if detect(data) == 'th':
                stm = self.getSentimentTH(data)
            elif detect(data) == 'en':
                stm = self.getSentimentENG(data)
            
            for tuplew in wc:
                if tuplew[0] in keyword:
                    i = tuplew[0]
                    wcCount = tuplew[1]
                    # print("Lang : ",detect(data))
                    if stm != '':
                        dfdict = {'Date':today,
                            'Keyword':i,
                            'Word Count':wcCount,
                            'Ref':0,'Link': link,
                            'Title':ex.getTitle(soup),
                            'Data':data,
                            'Sentiment':stm,
                            'Lang':ex.getLang(soup),
                            'Ref Link':dict(Counter(ex.getAllRefLink()))}
                        # print(data)
                        print("----------",i,tuplew)
                        
                        # print(df)
                        savePath = os.path.join("web search",today,i+'.csv') 
                        
                        # dataraw = pd.read_csv(newpath)
                        # newdata = dataraw.drop_duplicates()
                        # newdata.to_csv(savePath, encoding='utf-8', index=False)
                        
                        try:
                            filesize = self.getCountCsvLine(savePath)
                        except :
                            filesize = 1000
                            pass
                        if filesize >= 1000:
                            n=1
                            newname = os.path.join("web search",today,i+"("+str(n)+")"+'.csv')
                            while os.path.exists(newname):
                                n+=1
                                newname = os.path.join("web search",today,i+"("+str(n)+")"+'.csv')
                            ex.renameFile(savePath,newname)
                            self.creatNewSearchFile(savePath)
                        field_names = ['Date','Keyword','Word Count','Ref','Link','Title','Data','Sentiment','Lang','Ref Link']
                        ex.writCsvByDict(savePath,field_names,dfdict)
                    
        except langdetect.lang_detect_exception.LangDetectException:
            print("\n******* Error Data : ",data)
            pass
        return resualtDict
    
    def setDataByKeyword(self,fileName,Keyword):
        ex = web.webScraping()
        print("File Name : ",fileName)
        # path = "WebData"
        # rawData = os.listdir(path)
        # for i in rawData:
        keyword = os.listdir("collectkeys")
        todayByFile = fileName.split("_")[0]
        print("Date : ",todayByFile)
        newpath = os.path.join('web search',todayByFile)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        for kw in keyword:
            # df = self.setStartInfo()
            newpath = os.path.join('web search',todayByFile,kw+'.csv')
            if not os.path.exists(newpath):
                self.creatNewSearchFile(newpath)
                # self.writeCsvByDf(os.path.join(newpath,kw+".csv"),df)
        
        data = self.readJson(os.path.join("WebData",fileName))
        for d in data.keys():
            for l in list(data[d].keys()):
                soup = ex.makeSoup(l)
                for p in data[d][l]["Data"]:
                    self.setDictSentiment(soup,l,p,todayByFile)
        
    def setDataByKeywordAllDate(self): #For Old Data
        path = "WebData"
        rawData = os.listdir(path)
        for i in rawData:
            self.setDataByAllKeyword(i)
            
    def setDataByAllKeyword(self,fileName): #All old data
        ex = web.webScraping()
        print("File Name : ",fileName)
        # path = "WebData"
        # rawData = os.listdir(path)
        # for i in rawData:
        keyword = os.listdir("collectkeys")
        todayByFile = fileName.split("_")[0]
        print("Date : ",todayByFile)
        newpath = os.path.join('web search',todayByFile)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        for kw in keyword:
            # df = self.setStartInfo()
            newpath = os.path.join('web search',todayByFile,kw+'.csv')
            if not os.path.exists(newpath):
                self.creatNewSearchFile(newpath)
                # self.writeCsvByDf(os.path.join(newpath,kw+".csv"),df)
        
        data = self.readJson(os.path.join("WebData",fileName))
        for d in data.keys():
            for l in list(data[d].keys()):
                soup = ex.makeSoup(l)
                for p in data[d][l]["Data"]:
                    self.setDictSentiment(soup,l,p,todayByFile)
    
    def getReadByKeyword(self,date,kw):
        DList = []
        path = os.path.join("web search",date)
        for root, dirs, files in os.walk(path):
            # print(root, dirs, files)
            for name in files:
                # print(name)
                nameOnly = name.split(".")
                if kw == nameOnly[0] : 
                    # print(name)
                    DList.append(pd.read_csv(os.path.join(path,name)).drop_duplicates())
                    
                nameOnly = name.split("(")
                if kw == nameOnly[0] : 
                    # print(name)
                    DList.append(pd.read_csv(os.path.join(path,name)).drop_duplicates())
                    # DList.append(len(pd.read_csv(os.path.join(path,name)).drop_duplicates()))
                    # DList.append(os.path.abspath(os.path.join(root, name)))
                    # print(os.path.abspath(os.path.join(root, name)))
        print("File : ",len(DList))
        return DList
    
    def startSearch(self,Ldate,LWord):# date []
        ListOfDate = self.date_range(Ldate[0],Ldate[1])
        print("List Of Date : ",ListOfDate)
        print("List Of Word : ",LWord)
        dfResult = []
        for j in ListOfDate:
            for kw in LWord:
                # print(kw)
                fileListForSearch = self.getReadByKeyword(j,kw)
                dfResult += fileListForSearch
                # print(len(fileListForSearch))
                # dfResult.append(fileListForSear0ch)
                # print(fileListForSearch)
                # for path in fileListForSearch:
        newDf = pd.concat(dfResult,ignore_index=True)
        field_names = ['Date','Keyword','Word Count','Ref','Link','Title','Data','Sentiment','Lang','Ref Link']
        newDf.sort_values(field_names)
        # print(len(dfResult))
        return newDf.drop_duplicates()
                    
#DataManager().startSearch(['17-03-2022', '16-04-2022'],['spy x family'])