from datetime import datetime
import os
from PyQt5 import QtCore
import DataManager
from pythainlp import word_tokenize
import pandas as pd
import time
import DataManager as data
# import progress
import sys, time
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
dm = data.DataManager()
class WebThread(QThread):
    any_signal = pyqtSignal(int)
    dm = data.DataManager()
    def __init__(self, parent=None,sdate=None,edate=None,kw=None):
        super(WebThread, self).__init__(parent)
        # QThread.__init__(self, parent)
        self.sdate = sdate
        self.edate = edate
        self.keyword = kw
        self.val = 0
        self.FullLen =  1
        self.currentLen = 0
        # self.any_signal = QtCore.pyqtSignal(float)
        self.result = pd.DataFrame()
        self.is_running = True
        
    def getDf(self):
        # return self.startSearch([self.sdate,self.edate],self.keyword)
        return self.result
            
    def run(self):
    
        ListOfDate = dm.date_range(self.sdate,self.edate)
        # print("List Of Date : ",ListOfDate)
        # print("List Of Word : ",self.keyword)
        dfResult = []
        self.FullLen =  len(ListOfDate)+1
        self.currentLen = 0
        path = "C:/Users/tongu/Desktop/Web SC 2/Web-Scraping/web search"
        checkDate = os.listdir(path)
        print("checkDate : ",checkDate)
        for j in ListOfDate:
            print("Date Type",j,type(j))
            if j in checkDate:
                for kw in self.keyword:
                    # print("kw in self.keyword",j,kw)
                    fileListForSearch = dm.getReadByKeyword(j,kw)
                    # print("Return : ",fileListForSearch)
                    if len(fileListForSearch)!=0 :
                        dfResult += fileListForSearch
            self.currentLen += 1
            self.val = (self.currentLen/self.FullLen)*100
            print(self.currentLen,"/",self.FullLen)
            self.any_signal.emit(self.val)
            # print("startSearch",self.val)
        self.val = 100 
        self.any_signal.emit(self.val)
        
        try:
            newDf = pd.concat(dfResult,ignore_index=True)
            field_names = ['Date','Keyword','Word Count','Ref','Link','Title','Data','Sentiment','Lang','Ref Link']
            newDf.sort_values(field_names)
            # return newDf.drop_duplicates()
            self.result = newDf.drop_duplicates()
        except :
            print("Don't have dataframe")
            # self.val = 0
            # return pd.DataFrame()
            self.result = pd.DataFrame()
            
    def stop(self):
        self.is_running = False
        print('Stopping Web thread...')
        self.any_signal.emit(0)    
        self.terminate()
