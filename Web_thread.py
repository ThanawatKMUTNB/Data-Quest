from PyQt5 import QtCore
import DataManager
from pythainlp import word_tokenize
import pandas as pd
import time
import DataManager as data
# import progress
import sys, time
dm = data.DataManager()
class WebThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)
    dm = data.DataManager()
    def __init__(self, parent=None,sdate=None,edate=None,kw=None):
        super(WebThread, self).__init__(parent)
        self.sdate = sdate
        self.edate = edate
        self.keyword = kw
        self.val = 0
        self.FullLen =  1
        self.currentLen = 0
        # self.any_signal = QtCore.pyqtSignal(float)
        self.is_running = True
        
    def getDf(self):
        return self.startSearch([self.sdate,self.edate],self.keyword)
    
    def startSearch(self,Ldate,LWord):# date []
        ListOfDate = dm.date_range(Ldate[0],Ldate[1])
        print("List Of Date : ",ListOfDate)
        print("List Of Word : ",LWord)
        dfResult = []
        self.FullLen =  len(ListOfDate)+1
        self.currentLen = 0
        for j in ListOfDate:
            for kw in LWord:
                # print(kw)
                fileListForSearch = dm.getReadByKeyword(j,kw)
                dfResult += fileListForSearch
                # print(len(fileListForSearch))
                # dfResult.append(fileListForSear0ch)
                # print(fileListForSearch)
                # for path in fileListForSearch:
                # print("------",(self.currentLen/self.FullLen)*100)
            self.currentLen += 1
            self.val = (self.currentLen/self.FullLen)*100
            print("startSearch",self.val)
        try:
            newDf = pd.concat(dfResult,ignore_index=True)
            field_names = ['Date','Keyword','Word Count','Ref','Link','Title','Data','Sentiment','Lang','Ref Link']
            newDf.sort_values(field_names)
            
            self.val = 100
            return newDf.drop_duplicates()
        except :
            print("Don't have dataframe")
            # self.val = 0
            return pd.DataFrame()
    
    def run(self):
        while 1:
            # time.sleep(0.1)
            # print("...",self.val)
            # print("\n",self.currentLen,'/',self.FullLen,'Start Web thread...',self.val)
            self.any_signal.emit(self.val)
        # cnt=0
        # while(True):
        #     cnt+=1
        #     if cnt==99: cnt=0
        #     time.sleep(0.01)
        #     self.any_signal.emit(cnt) 
   
    def stop(self):
        self.is_running = False
        print('Stopping Web thread...')
        self.terminate()
