from PyQt5 import QtWidgets,QtGui,QtCore
import DataManager
from pythainlp.corpus import thai_stopwords
from pythainlp import word_tokenize
from nltk.corpus import stopwords
import nltk
import pandas as pd
import string

class TwitterThread(QtCore.QThread):
	
    #any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(TwitterThread, self).__init__(parent)
    def run(self):
        print('Starting Twitter thread...')

    def stop(self):
        print('Stopping Twitter thread...')
        self.terminate()

class CollectWordThread(QtCore.QThread):
	
    dataframe = QtCore.pyqtSignal(object)
    count = QtCore.pyqtSignal(int)
    def __init__(self, parent=None,df=None):
        super(CollectWordThread, self).__init__(parent)
        self.dm = DataManager.DataManager()
        self.df = df
    def run(self):
        print('Starting Collectword thread...')
        #self.df = self.dm.collectwords(self.df)
        #######################################

        nltk.download('stopwords')          #important
        dataframe = self.df.reset_index()
        th_stopwords = list(thai_stopwords())
        en_stops = set(stopwords.words('english'))
        en_stops.update(list(string.ascii_lowercase))
        en_stops.update(list(string.ascii_uppercase))
        en_stops.update(['0','1','2','3','4','5','6','7','8','9'])
        word = {}
        countrow = len(dataframe.index)
        #print('start loop collect word')
        for index,row in dataframe.iterrows():    #only tweet
            cnt = (int(index)/(int(countrow)*1.1))*100
            self.count.emit(cnt)
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
            
        #print(countrow,index)
        if 'RT' in word:
            del word['RT']  #for twitter
        if ' ' in word:
            del word[' ']   #for thai language
        sortword = sorted(word.items(),key=lambda x:x[1],reverse=True)
        self.df = pd.DataFrame(sortword,columns=['Word','Count'])
        cnt = 100
        self.count.emit(cnt)

        #######################################
        
        self.dataframe.emit(self.df)            #return df to GUI

    def stop(self):
        print('Stopping Collectword thread...')
        self.terminate()
