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
    any_signal = QtCore.pyqtSignal(float)
    # countkeys = QtCore.pyqtSignal(int)
    # dataframe = QtCore.pyqtSignal(object)
    dm = data.DataManager()
    def __init__(self, parent=None,sdate=None,edate=None,kw=None):
        super(WebThread, self).__init__(parent)
        self.sdate = sdate
        self.edate = edate
        self.keyword = kw
        self.val = 0
        # self.any_signal = QtCore.pyqtSignal(float)
        self.is_running = True
        
    def getDf(self):
        return dm.startSearch([self.sdate,self.edate],[self.keyword])
    
    def run(self):
        # self.val = 0
        # while self.val<100:
        #     # print('Starting Web thread...')
        #     try:
        #         self.val = (dm.currentLen/dm.FullLen)*100
        #     except :
        #         self.val = 0
        #     # print(self.val)
        #     self.any_signal.emit(self.val) 
        cnt=0
        while(True):
            cnt+=1
            if cnt==99: cnt=0
            time.sleep(0.01)
            self.any_signal.emit(cnt) 
   
    def stop(self):
        self.is_running = False
        print('Stopping Web thread...')
        self.terminate()
