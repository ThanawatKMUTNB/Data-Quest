from PyQt5 import QtCore
import DataManager
from pythainlp import word_tokenize
import pandas as pd
import time
import twitter_scrap

class TwitterThread(QtCore.QThread):
	
    countkeys = QtCore.pyqtSignal(int)
    dataframe = QtCore.pyqtSignal(object)
    def __init__(self, parent=None,df=None,key=None,Ans=None,until=None):
        super(TwitterThread, self).__init__(parent)
        self.tw = twitter_scrap.Twitter_Scrap()
        self.df = df
        self.key = key  #for search
        self.oldkey = self.df['Keyword'].tolist()
        self.oldkey =  list(set(self.oldkey))
        self.until = until
        self.Ans = Ans
    def run(self):
        print('Starting Twitter thread...')
        self.df = self.searchkeys()
        self.dataframe.emit(self.df)            #return df to GUI
    
    def setdataframe(self,df):
        self.df = df
        self.oldkey = self.df['Keyword'].tolist()
        self.oldkey = list(set(self.oldkey))
    
    def savedata(self,keyword,until): #keyword is list
        
        print('\nstart saving @')
        allsearchkeys = len(keyword)
        cnt = 0
        for kw in keyword:
            time.sleep(0.01)
            self.df = pd.concat([self.df,self.tw.get_related_tweets(kw,until)])
            cnt +=1
            count = (cnt/allsearchkeys)*100
            print(count)
            self.countkeys.emit(count)

        self.df.drop_duplicates(keep='last',inplace=True)
        self.df.sort_values(by=['Keyword'],inplace=True)

        print('save complete @')
    

    def searchkeys(self):   #keyword's type is list
        keyword = self.key
        Ans = self.Ans
        until = self.until
        if len(keyword) > 1:            #>1 keyword
            dhave = []
            for key in keyword:
                if key not in self.oldkey:
                    dhave.append(key)
            print(self.oldkey)
            print(dhave)
            if Ans == "real":                 #search old keys real time (until)
                self.savedata(keyword,until)
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
            elif len(dhave) > 0:          
                self.savedata(dhave,until)      #search new keyword
                self.oldkey.extend(dhave)         #add new keys
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
            else:                               #show old keys
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
        elif keyword[0] in self.oldkey:   #1 key in old keys
            if Ans == "real":
                self.savedata(keyword,until)
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
            else:
                return self.df.loc[self.df['Keyword']==keyword[0]]
        else:              #1keyword (new)
            if Ans == 'yes':            #new key 1 key
                self.savedata(keyword,until)
                self.oldkey.extend(keyword)
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
            elif Ans == "real":
                self.savedata(keyword,until)
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])
            else:
                print('You select NO')
                return self.df.loc[self.df['Keyword'].isin(keyword)].sort_values(by=['Keyword'])


    def stop(self):
        print('Stopping Twitter thread...')
        self.terminate()

class CollectWordThread(QtCore.QThread):
	
    dataframe = QtCore.pyqtSignal(object)
    count = QtCore.pyqtSignal(int)
    def __init__(self, parent=None,df=None,en_stops={},th_stopwords={}):
        super(CollectWordThread, self).__init__(parent)
        self.dm = DataManager.DataManager()
        self.df = df
        self.en_stops = en_stops
        self.th_stopwords = th_stopwords
    def run(self):
        print('Starting Collectword thread...')

        dataframe = self.df.reset_index()
        word = {}
        countrow = len(dataframe.index)
        print('start loop collect word')
        for index,row in dataframe.iterrows():    #only tweet
            if int(index) % 3000 == 0:
                time.sleep(0.001)
            cnt = (int(index)/(int(countrow)))*100
            self.count.emit(cnt)
            if row['Language'] == 'en':
                allwords = str(row['Tweet']).split()
                for w in allwords: 
                    if w not in self.en_stops:
                        if w in word:
                            word[w] += 1
                        else:
                            word[w] = 1
            elif row['Language'] == 'th':
                allwords = word_tokenize(row['Tweet'], engine='newmm')
                for w in allwords: 
                    if w not in self.th_stopwords:
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
        print('set to dataframe')
        sortword = sorted(word.items(),key=lambda x:x[1],reverse=True)
        self.df = pd.DataFrame(sortword,columns=['Word','Count'])
        
        cnt = 100
        self.count.emit(cnt)
        self.dataframe.emit(self.df)            #return df to GUI

    def stop(self):
        print('Stopping Collectword thread...')
        self.terminate()
