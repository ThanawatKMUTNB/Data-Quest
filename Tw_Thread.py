from PyQt5 import QtWidgets,QtGui,QtCore
import time,sys
import DataManager

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
    def __init__(self, parent=None,df=None):
        super(CollectWordThread, self).__init__(parent)
        self.dm = DataManager.DataManager()
        self.df = df
    def run(self):
        self.df = self.dm.collectwords(self.df)
        self.dataframe.emit(self.df)            #return df to GUI
        print('Starting Collectword thread...')

    def stop(self):
        print('Stopping Collectword thread...')
        self.terminate()
