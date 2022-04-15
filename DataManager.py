import ast
from csv import DictWriter, writer
import csv
import json
from operator import index
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
import os
import time
import shutil
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
        self.keys = os.listdir("Tweet_Test\collectkeys")
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
        en_stops = set(stopwords.words('english'))
        word = {}
        for index,row in dataframe.iterrows():    #only tweet
            if row['Language'] == 'eng':
                allwords = row['Tweet'].split()
                for w in allwords: 
                    if w not in en_stops:
                        if w in word:
                            word[w] += 1
                        else:
                            word[w] = 1
            elif row['Language'] == 'th':
                allwords = word_tokenize(row['Tweet'], engine='newmm')
                for w in allwords: 
                    if w not in en_stops:
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
    
    # def getReadByDateList(self,Sdate):
    #     DList = []
    #     for root, dirs, files in os.walk(r'WebData'):
    #         for name in files:
    #             if Sdate in str(name): 
    #                 # DList.append(name)
    #                 DList.append(os.path.abspath(os.path.join(root, name)))
    #                 # print(os.path.abspath(os.path.join(root, name)))
    #     return DList
    
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
    
    # def date_range(self,start, end):
    #     print(start, end)
    #     dateS = datetime.strptime(start,'%d-%m-%Y')
    #     dateE = datetime.strptime(end,'%d-%m-%Y')
    #     delta = dateE - dateS  # as timedelta
    #     days = [dateS + timedelta(days=i) for i in range(delta.days + 1)]
    #     resualt = [] 
    #     for i in days:
    #         resualt.append(str(i.day).zfill(2)+"-"+str(i.month).zfill(2)+"-"+str(i.year))
    #     # print(resualt)
    #     return resualt

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
            
    def setDataInfo(self,jsonFile):
        keyword = self.keys
        print(keyword,jsonFile)
        todayByFile = jsonFile.split("_")[0]
        field_names = ['Date','Keyword','Word Count','Ref','Link','Data','Sentiment','Lang','Ref Link']
        # df = {
        #         'Date' : [],
        #         'Keyword' : [],
        #         'Word Count' : [],
        #         "Ref" : [],
        #         "Link" : [],
        #         "Data" : [],
        #         "Sentiment" : [],
        #         'Lang' : [],
        #         "Ref Link" : []
        #         }
        
        data = self.readJson(os.path.join("WebData",jsonFile))
        # print(data)
        for d in data.keys():
            for l in list(data[d].keys()):
                for p in data[d][l]["Data"]:
                    try:
                        wc = self.paragraphToList(p)
                        for t in wc:
                            # df = []
                            for kw in keyword:
                                if t[0] == kw:
                                    df = []
                                    # print(wc)
                                    print("\n\n",kw)
                                    countWord = t[1]
                                    if data[d][l]["Lang"].lower() == 'th':
                                        stm = self.getSentimentTH(p)
                                    else : 
                                        stm = self.getSentimentENG(p)
                                    # stm = "Good"
                                    # df = {
                                    #     'Date' : todayByFile,
                                    #     'Keyword' : keyword,
                                    #     'Word Count' : 0,
                                    #     "Ref" : countWord,
                                    #     "Link" : l,
                                    #     "Data" : p,
                                    #     "Sentiment" : stm,
                                    #     'Lang' : data[d][l]["Lang"],
                                    #     "Ref Link" : data[d][l]["Ref"]
                                    #     }
                                    df = [todayByFile,kw,0,countWord,l,p,stm,data[d][l]["Lang"],data[d][l]["Ref"]]
                                    # print(df)
                                    self.writeCsvByList(os.path.join("web search",todayByFile,kw+'.csv'),df)
                                    # self.append_dict_as_row(os.path.join("web search",todayByFile,kw+'.csv'), df, field_names)
                                    break
                                else:
                                    os.system("CLS")
                    except :
                        pass
        # df=oldDf.append(df, ignore_index = True)
        # return pd.DataFrame.from_dict(df)
    
    def setDataByKeyword(self):
        path = "WebData"
        rawData = os.listdir(path)
        for i in rawData:
            todayByFile = i.split("_")[0]
            print(todayByFile)
            newpath = os.path.join('web search',todayByFile)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                for kw in keyword:
                    df = self.setStartInfo()
                    self.writeCsvByDf(os.path.join(newpath,kw+".csv"),df)
                
            keyword = os.listdir("Tweet_Test\collectkeys")
            # for kw in keyword:
                # df = self.setDataInfo(kw,i)
                # df = self.setStartInfo()
                # self.writeCsvByDf(os.path.join(newpath,kw+".csv"),df)
            self.setDataInfo(i)
                
    # def startSearch(self,Ldate,LWord):# date []
    #     # self.readJson
    #     df = {
    #             'Date' : [],
    #             'Keyword' : [],
    #             'Word Count' : [],
    #             "Link" : [],
    #             "Data" : [],
    #             "Sentiment" : [],
    #             'Lang' : [],
    #             "Ref Link" : []
    #             }
    #     ListOfDate = self.date_range(Ldate[0],Ldate[1])
    #     for j in ListOfDate:
    #         FileByDateList = self.getReadByDateList(j)
    #         # print(j)
    #         # print(FileByDateList)
    #         if FileByDateList != []:
    #             for i in FileByDateList:
    #                 # print("Link : ",i)
    #                 # print(type(i))
    #                 data = self.readJson(i)
    #                 # print(type(data))
    #                 # print(i)
    #                 # print(data[j].keys())
    #                 for d in data.keys():
    #                     # print(d)
    #                     for l in data[d].keys():
    #                         # print(data[d][l]["Data"])
    #                         # for w in LWord:
    #                         # print(w)
    #                         n = 1
    #                         for p in data[d][l]["Data"]:
    #                             try:
    #                                 wc = self.paragraphToList(p)
    #                                 # print(n)
    #                                 # print(wc)
    #                                 for w in LWord:
    #                                     for t in wc:
    #                                         if t[0].lower() == w.lower():
    #                                             # print("-----------------------------------------------------------------")
    #                                             countWord = t[1]
    #                                             if data[d][l]["Lang"].lower() == 'th':
    #                                                 stm = self.getSentimentTH(p)
    #                                             else : stm = self.getSentimentENG(p)
    #                                             df['Date'].append(d)
    #                                             df['Keyword'].append(w)
    #                                             df['Word Count'].append(countWord)
    #                                             df['Link'].append(l)
    #                                             df['Lang'].append(data[d][l]["Lang"])
    #                                             df['Ref Link'].append(data[d][l]["Ref"])
    #                                             df['Data'].append(p)
    #                                             df['Sentiment'].append(stm)
    #                                             # print("-----------",df)
    #                                             n+=1
    #                                             self.writeCsvByDf(os.path.join("WebSearch",'_'.join(Ldate)+"_"+'_'.join(LWord)+".csv"),pd.DataFrame.from_dict(df))
                                    
    #                             except :
    #                                 pass
        
    #     # self.writeCsvByDf(os.path.join("WebSearch",'_'.join(Ldate)+"_"+'_'.join(LWord)+".csv"),pd.DataFrame.from_dict(df))
        
    #     return pd.DataFrame.from_dict(df)