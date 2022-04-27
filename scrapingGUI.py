from ast import keyword
import encodings
from msilib.schema import ListView
from tabnanny import check
from typing_extensions import Self
from xml.etree.ElementTree import tostring
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import Qt, QDate
import pandas as pd
import os
import sqlite3
import glob
from os.path import dirname, realpath, join
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidget, QTableWidgetItem,QMessageBox, QProgressBar
import numpy as np
from datetime import datetime, timedelta
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import functools
import numpy as np
from regex import W
from tqdm import tqdm
from requests import delete
import importWin as windo 
import time
import threading
import nltk
import string
from nltk.corpus import stopwords
from pythainlp.corpus import thai_stopwords

import Web_thread as webTread

import DataManager 
import twitter_scrap
import webNewNew
from Tw_Thread import *

#Test        
#ยังไม่แก้ช่วงวันที่ที่เลือกได้ใน tab 2 และ 3
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class Ui_MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.calendarDateClick = cn.qDateBegin()
        self.table = QtWidgets.QTableView()
        self.filename = glob.glob(str(str(os.getcwd())+"\\Backup_Data\\*.csv"))
        #self.df = dm.unionfile(self.filename) #win.readFile(win.path) save tweet file
        self.df = dm.newUnion()
        
        #tw.setdataframe(self.df)
        #tw.setdataframe(self.dt)
        self.dt = None
        #tw.setdataframe(self.dt)
        #self.data = win.OpenFile()
        #pd.read_csv("tweet_data_2032022.csv", encoding='utf8',index_col=False)
        self.getSince = str
        self.getUntil = str
        '''self.getSince_2 = str
        self.getUntil_2 = str'''
        self.getSince_3 = str
        self.getUntil_3 = str
        self.earliest = None
        self.lasted = None
        self.getDataDate1 = None
        self.getDataDate2 = None
        self.model = TableModel(self.df)
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.processWord = str

        #self.modelWeb = TableModel(dm.startSearch(["16-04-2022","17-04-2022"],['anime','animation']))
        self.modelWeb = None
        self.tableWeb = QtWidgets.QTableView()
        self.tableWeb.setModel(self.modelWeb)
        #self.maxDate()
        #self.setDate()
        self.keywords = self.df['Keyword'].tolist()
        self.keywords = list(set(self.keywords))
        self.tw_worddf = None

        self.th_stopwords = list(thai_stopwords())
        nltk.download('stopwords')
        self.en_stops = set(stopwords.words('english'))
        self.en_stops.update(list(string.ascii_lowercase))
        self.en_stops.update(list(string.ascii_uppercase))
        self.en_stops.update(['0','1','2','3','4','5','6','7','8','9'])

    def showCalenderWin(self):
        self.MainWindow2 = QtWidgets.QMainWindow()
        self.ui2 = webNewNew.Ui_MainWindowSecond()
        self.ui2.setupUi(self.MainWindow2)
        self.MainWindow2.show()
        
    def dateSet(self) :
        #date = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        dm.formatdatetime('Time')
        since = dm.df['Time'].min().strftime('%Y/%m/%d')
        date = (datetime.strptime(since,'%Y/%m/%d')).date()
        self.dateEdit_1.setDate(date) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_1.dateChanged.connect(self.dateSinceReturn) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

        #date2 = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        until = dm.df['Time'].max().strftime('%Y/%m/%d')
        date2 = (datetime.strptime(until,'%Y/%m/%d')).date()
        self.dateEdit_2.setDate(date2) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_2.dateChanged.connect(self.dateUntilReturn) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช

    def dateSet_3(self) :
        #date = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        dm.formatdatetime('Time')
        since = dm.df['Time'].min().strftime('%Y/%m/%d')
        date = (datetime.strptime(since,'%Y/%m/%d')).date()
        self.dateEdit_5.setDate(date) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_5.dateChanged.connect(self.dateSinceReturnWeb) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

        #date2 = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        until = dm.df['Time'].max().strftime('%Y/%m/%d')
        date2 = (datetime.strptime(until,'%Y/%m/%d')).date()
        self.dateEdit_6.setDate(date2) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_6.dateChanged.connect(self.dateUntilReturnWeb) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช

    '''def dateSet_3(self) :
        #date = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        dm.formatdatetime('Time')
        since = dm.df['Time'].min().to_pydatetime()#.date()#.strftime('%Y/%m/%d')
        print(type(since))
        #date = (datetime.strptime(since,'%Y-%m-%d %H:%M:%S')).date()
        date = since.date()
        self.dateEdit_5.setDate(date) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_5.dateChanged.connect(self.dateSinceReturnWeb) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

        #date2 = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        until = dm.df['Time'].max().to_pydatetime()#.strftime('%Y/%m/%d')
        #date2 = (datetime.strptime(str(until),'%Y-%m-%d %H:%M:%S')).date()
        date2 = until.date()
        self.dateEdit_6.setDate(date2) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_6.dateChanged.connect(self.dateUntilReturnWeb) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้'''

    def dateSinceReturn(self) :
        self.getSince = self.dateEdit_1.date().toPyDate() #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getSince)
        return self.getSince

    def dateUntilReturn(self) :
        self.getUntil = self.dateEdit_2.date().toPyDate() #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getUntil)
        return self.getUntil

    def dateSinceReturnWeb(self) :
        dateChange = self.dateEdit_5.date().toPyDate()
        self.getSince_3 = dateChange.strftime('%d-%m-%Y') #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getSince)
        return self.getSince_3

    def dateUntilReturnWeb(self) :
        dateChange = self.dateEdit_6.date().toPyDate()
        self.getUntil_3 = dateChange.strftime('%d-%m-%Y') #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getUntil)
        return self.getUntil_3

    def showRealtime(self) : #BUTTON search key in this time
        self.progressTime(0)
        print('real time')
        if self.dateSinceReturn()>self.dateUntilReturn():
            self.showErrorDialog()
            return
        if datetime.now().date() <= self.dateUntilReturn():
            pass
        elif int(str(datetime.now().date()-self.dateUntilReturn())[0]) > 7:
            self.showErrorDialog2()
            return
        keywords = self.SearchBox1.text()
        keywords = keywords.split(',')
        keywords = list(map(lambda x: x.lower(), keywords))   #change to lower
        self.df = dm.getperiod(str(self.dateSinceReturn()),str(self.dateUntilReturn()))
        self.t1 = TwitterThread(parent=None,df=self.df)
        tw.setdataframe(self.df)
        self.t1.setdataframe(self.df)
        #self.t1.oldkey = self.keywords
        self.t1.until = str(self.dateUntilReturn())
        self.t1.Ans = 'real'
        if "" not in keywords:
            if self.showDialog() == 'Yes':
                #self.t1 = TwitterThread(parent=None,df=self.df,key=keywords,Ans='real',until=str(self.dateUntilReturn()))
                self.t1.key = keywords
                dhave = []
                for keyword in keywords:
                    if keyword not in self.keywords:
                        dhave.append(keyword)
                self.keywords.extend(dhave)
                self.t1.start()
                self.t1.countkeys.connect(self.progressTime)
                self.t1.dataframe.connect(self.setTableTab1)
                #self.df = tw.searchkeys(keywords,'real',str(self.dateUntilReturn()))
                
                # self.model = TableModel(self.df) 
                # self.table = QtWidgets.QTableView()
                # self.table.setModel(self.model)
                # self.tableView.setModel(self.model)
            else:
                return
        else:
            print('search new all keys')
            if self.showDialog() == 'Yes':
                self.t1.key = self.keywords
                #self.t1 = TwitterThread(parent=None,df=self.df,key=self.keywords,Ans='real',until=str(self.dateUntilReturn()))
                self.t1.start()
                self.t1.countkeys.connect(self.progressTime)
                self.t1.dataframe.connect(self.setTableTab1)
                #self.df = tw.searchkeys(self.keywords,'real',str(self.dateUntilReturn()))
                
                # self.model = TableModel(self.df) 
                # self.table = QtWidgets.QTableView()
                # self.table.setModel(self.model)
                # self.tableView.setModel(self.model)
                #self.dateSet() 
                
            else:
                return
        #self.progressTime.value(0)

    def showDefaultFileTweetW(self) : #Refresh BUTTON for show collectkey(Tab2)
        self.model = TableModel(self.tw_worddf) 
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.tableView_2.setModel(self.model)
        return

    # def button1(self) :     #Search BUTTON
        
    #     #self.ShowdfTab1()
    #     self.t1 = TwitterThread(parent=None)        #for can use GUI while data processing
    #     self.t1.start()
    #     self.t1.finished.connect(self.ShowdfTab1)


    def button1(self):          #Search BUTTON Tab1
        print("\n\n")
        self.progressTime(0)
        print(len(self.df.index),'rows')
        print(self.dateSinceReturn(),self.dateUntilReturn())
        if self.dateSinceReturn()>self.dateUntilReturn():
            self.showErrorDialog()
            return
        self.df = dm.getperiod(str(self.dateSinceReturn()),str(self.dateUntilReturn())) #set day range dataframe 
        #print(list(set(self.df['Keyword'].tolist())))
        tw.setdataframe(self.df)        #set same dataframe for search 
        self.t1 = TwitterThread(parent=None,df=self.df)
        self.t1.setdataframe(self.df)
        self.t1.oldkey = self.keywords
        self.t1.until = str(self.dateUntilReturn())
        

        keywords = self.SearchBox1.text()
        keywords = keywords.split(',')
        keywords = list(map(lambda x: x.lower(), keywords))   #change to lower
        if "" not in keywords:
            self.t1.key = keywords
            print(len(keywords),keywords)
            dhave = []
            for keyword in keywords:
                if keyword not in self.keywords:
                    dhave.append(keyword)
            if len(dhave) > 0:      #new keyword
                if datetime.now().date() <= self.dateUntilReturn():         #for search until day greater than today
                    pass
                elif int(str(datetime.now().date()-self.dateUntilReturn())[0]) > 7:     #cannot search twitter new keyword greater than 7 day
                    self.showErrorDialog2()
                    return
                if self.showDialog() == 'Yes':      #search new 
                    self.t1.Ans = 'yes'
                    self.keywords.extend(dhave)
                    #self.df = tw.searchkeys(keywords ,'yes',str(self.dateUntilReturn()))
                    self.t1.start()
                    self.t1.countkeys.connect(self.progressTime)#
                    self.t1.dataframe.connect(self.setTableTab1)
                    
                else:
                    #self.df = tw.searchkeys(keywords,'no',str(self.dateUntilReturn()))
                    return
                    
            else:       #have key
                #self.df = tw.searchkeys(keywords,'no',str(self.dateUntilReturn()))
                self.t1.start()
                #self.t1.countkeys.connect(self.progressTime)
                self.t1.dataframe.connect(self.setTableTab1)
                
            self.t1.setdataframe(self.df)       #add new key to oldkey ??
            tw.setdataframe(self.df)
        else:
            #self.t1 = TwitterThread(parent=None,df=self.df,key=self.keywords,until=str(self.dateUntilReturn()))
            self.setTableTab1(self.df)
            # self.t1.key = self.keywords
            # self.t1.start()
            # self.t1.countkeys.connect(self.progressTime)
            # self.t1.dataframe.connect(self.setTableTab1)
        

        print(len(self.df.index),tw.keys)

        # self.model = TableModel(self.df) 
        # self.table = QtWidgets.QTableView()
        # self.table.setModel(self.model)
        # self.tableView.setModel(self.model)
        # self.labelShowKeywords()
        # print('tab1 finish')
                    
        #self.t2.count.connect(self.progressTime)
    def setPolarityTab1(self,df):
        polarity = df['Polarity'].value_counts()
        allrow = df.shape[0]
        self.Tw_Positive = (polarity['positive']/allrow)*100
        self.Tw_Negative = (polarity['negative']/allrow)*100
        self.Tw_Neutral = (polarity['neutral']/allrow)*100
        #print(self.Tw_Neutral,self.Tw_Positive,self.Tw_Negative)
    
    def setTableTab1(self,df):
        self.setPolarityTab1(df)
        self.model = TableModel(df) 
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.tableView.setModel(self.model)
        self.labelShowKeywords()
        dm.concatfile(df)
        self.addlist()
        self.progressTime(100)
        self.t1.stop()
        time.sleep(1)
        self.t2 = CollectWordThread(parent=None,df=df,en_stops=self.en_stops,th_stopwords=self.th_stopwords)         #use df from tab1 to data processing tab2
        self.t2.start()
        self.t2.count.connect(self.progressTime_2)
        self.t2.dataframe.connect(self.CollectwordTab2)             #use dataframe from ThreadClass to setupDataframe
        #self.progressTime(0)
         
    
    def CollectwordTab2(self,df):
        self.tw_worddf = df
        self.addlist_2()
        self.model2 = TableModel(self.tw_worddf) 
        self.table2 = QtWidgets.QTableView()
        self.table2.setModel(self.model2)
        self.tableView_2.setModel(self.model2)
        #print('tab2 finish')
        self.t2.stop()
        self.progressTime_2(0)
        
    def button2(self) : # TAB2 BUTTON for seach collect word[:10]
        # if self.tw_worddf == None:
        #     return
        tw.setdataframe(dm.df)
        tenwords = self.tw_worddf['Word'].tolist()[:10]  #only top ten words
        tenwords = list(map(lambda x: x.lower(), tenwords))
        self.t1 = TwitterThread(parent=None,df=self.df)
        self.t1.until = str(self.dateUntilReturn())
        self.t1.Ans = 'yes'
        if self.showDialog() == 'Yes':
            
            self.dateSet()
            dhave = []
            for keyword in tenwords:
                if keyword not in self.keywords:
                    dhave.append(keyword)
            if len(dhave) > 0:
                self.keywords.extend(dhave)
                #self.df = tw.searchkeys(tenwords,'yes',str(self.dateUntilReturn()))
                self.t1.key = tenwords
                self.t1.start()
                self.t1.countkeys.connect(self.progressTime_2)
                self.t1.dataframe.connect(self.searchCollectTab)
                
                
                
            else:
                self.t1.Ans = 'no'
                self.t1.key = tenwords
                self.t1.start()
                self.t1.dataframe.connect(self.searchCollectTab)
        else:
            return
        #self.addlist_2()    
        self.addlist() 
        self.model = TableModel(self.df) 
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.tableView_2.setModel(self.model)
    
    def searchCollectTab(self,df):
        dm.concatfile(df)
        self.addlist() 
        self.t1.stop()
        self.model2 = TableModel(df) 
        self.table2 = QtWidgets.QTableView()
        self.table2.setModel(self.model2)
        self.tableView_2.setModel(self.model2)

    def refreshButton_1(self) :#
        self.progressTime(0)
        print('refresh')
        self.SearchBox1.clear()
        self.dateSet()
        self.df = dm.setdefaultDF()
        #self.df = dm.unionfile(self.filename)
        #self.df = dm.getperiod(str(self.dateSinceReturn()),str(self.dateUntilReturn()))
        print(len(self.df.index),tw.keys)
        self.model = TableModel(self.df) 
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model) #เอา df แปลงเป็นตารางเรียบร้อย
        self.tableView.setModel(self.model) #เอาตารางไปโชว์เลย
        self.progressTime(100)
        return


    def deleteButton_1(self) : #สำหรับปุ่ม delete tab tweet
        if self.showDeleteDialog() == "Yes":
            keywords = self.SearchBox1.text()
            keywords = keywords.split(',')
            keywords = list(map(lambda x: x.lower(), keywords))
            if "" not in keywords:
                self.progressTime(0)
                self.dateSet()
                self.SearchBox1.clear()
                self.df = dm.deletekeyword(keywords)
                self.keywords = self.df['Keyword'].tolist()
                self.keywords = list(set(self.keywords))
                self.addlist()
                self.model = TableModel(self.df) 
                self.table = QtWidgets.QTableView()
                self.table.setModel(self.model) #เอา df แปลงเป็นตารางเรียบร้อย
                self.tableView.setModel(self.model) #เอาตารางไปโชว์เลย
                self.progressTime(100)
            else:
                print('nonKeyword')
                return
        return 

    def refreshButton_2(self) : 
        return
    

    def labelShowKeywords(self) :  #เอาไว้โชว์ label ตาม keyword ที่ใส่เข้าไปในตัว entry
        keywordShow = self.SearchBox1.text().lower()
        _translate = QtCore.QCoreApplication.translate
        self.labelShow.setText(_translate("MainWindow", keywordShow)) #ให้โชว์ข้อความ
        

    def addKeywordToList(self,listName) : #วน add keywords 
        for i in range(len(self.keywords)) :
            item = QtWidgets.QListWidgetItem(self.keywords)
            listName.addItem(item[i])

    def readFile(self,path):
        #path = win.path
        isdir = os.path.isdir(path)
        if isdir == False:
            fileExtension = path.split(".")
            # print(fileExtension[-1])
            if fileExtension[-1] == "csv":
                df = pd.read_csv(path)
            else:
                print("Excel ",path)
                #print(fileExtension[-1])
                df = pd.read_excel(path, engine = "openpyxl")
            return df

    def showDialog(self): #ไว้เด้งข้อความขึ้นมา ถ้าตัวที่ป้อนเข้ามาใน entry ไม่มีอยู่ใน keywords ที่กำหนด
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Do you want to search?") #แสดงข้อความ
        msgBox.setWindowTitle("Warning") #Title
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No) #มีปุ่ม yes และ no
        #ถ้าอยากเปลี่ยนปุ่ทเป็นแบบอื่น เปลี่ยนจากพวก yes หรือ no ได้เลย เช่น Save Cancel Ok Close Open
        #msgBox.buttonClicked.connect(msgButtonClick) ไม่มีไร เป็นการเชื่อมเวลากดปุ่ม ซึ่งในตอนนี้ไม่ได้เชื่อมฟังก์ชั่นอะไรไว้ 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes: #ถ้ากด yes จะทำอะไร
            return 'Yes'
        elif returnValue == QMessageBox.No: #ถ้ากด no จะทำอะไร
            return 'No'
    
    def showDeleteDialog(self): #ไว้เด้งข้อความขึ้นมา ถ้าตัวที่ป้อนเข้ามาใน entry ไม่มีอยู่ใน keywords ที่กำหนด
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure?") #แสดงข้อความ
        msgBox.setWindowTitle("Warning") #Title
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No) #มีปุ่ม yes และ no
        #ถ้าอยากเปลี่ยนปุ่ทเป็นแบบอื่น เปลี่ยนจากพวก yes หรือ no ได้เลย เช่น Save Cancel Ok Close Open
        #msgBox.buttonClicked.connect(msgButtonClick) ไม่มีไร เป็นการเชื่อมเวลากดปุ่ม ซึ่งในตอนนี้ไม่ได้เชื่อมฟังก์ชั่นอะไรไว้ 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes: #ถ้ากด yes จะทำอะไร
            return 'Yes'
        elif returnValue == QMessageBox.No: #ถ้ากด no จะทำอะไร
            return 'No'

    def showSearchDialogWeb(self): #ไว้เด้งข้อความขึ้นมา ถ้าตัวที่ป้อนเข้ามาใน entry ไม่มีอยู่ใน keywords ที่กำหนด
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Do you want to search?") #แสดงข้อความ
        msgBox.setWindowTitle("Warning") #Title
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No) #มีปุ่ม yes และ no
        #ถ้าอยากเปลี่ยนปุ่ทเป็นแบบอื่น เปลี่ยนจากพวก yes หรือ no ได้เลย เช่น Save Cancel Ok Close Open
        #msgBox.buttonClicked.connect(msgButtonClick) ไม่มีไร เป็นการเชื่อมเวลากดปุ่ม ซึ่งในตอนนี้ไม่ได้เชื่อมฟังก์ชั่นอะไรไว้ 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes: #ถ้ากด yes จะทำอะไร
            return 'Yes'
        elif returnValue == QMessageBox.No: #ถ้ากด no จะทำอะไร
            return 'No'
    
    def showDialogWebForNew(self): #ไว้เด้งข้อความขึ้นมา ถ้าตัวที่ป้อนเข้ามาใน entry ไม่มีอยู่ใน keywords ที่กำหนด
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Do you want to search?") #แสดงข้อความ
        msgBox.setWindowTitle("Warning") #Title
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No) #มีปุ่ม yes และ no
        #ถ้าอยากเปลี่ยนปุ่ทเป็นแบบอื่น เปลี่ยนจากพวก yes หรือ no ได้เลย เช่น Save Cancel Ok Close Open
        #msgBox.buttonClicked.connect(msgButtonClick) ไม่มีไร เป็นการเชื่อมเวลากดปุ่ม ซึ่งในตอนนี้ไม่ได้เชื่อมฟังก์ชั่นอะไรไว้ 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes: #ถ้ากด yes จะทำอะไร
            return 'Yes'
        elif returnValue == QMessageBox.No: #ถ้ากด no จะทำอะไร
            return 'No'
            
    def showTableWeb(self) :
        # self.wt = webTread.WebThread()
        # self.wt.start()
        # self.wt.sdate = self.dateSinceReturnWeb()
        # self.wt.edate = self.dateUntilReturnWeb()
        # print("\n\n")
        # print(len(self.dt.index),'rows')
        # print(self.dateSinceReturnWeb(),self.dateUntilReturnWeb())
        '''if self.dateSinceReturnWeb()>self.dateUntilReturnWeb():
            self.showErrorDialog()
            return'''
        self.dt = dm.getperiod(str(self.dateSinceReturnWeb()),str(self.dateUntilReturnWeb()))
        print(list(set(self.dt['Keyword'].tolist())))
        tw.setdataframe(self.dt)
        keywords = self.SearchBox_3.text()
        keywords = keywords.split(',')
        keywords = list(map(lambda x: x.lower(), keywords))   #change to lower
        if "" not in keywords:
            print(len(keywords),keywords)
            dhave = []
            for keyword in keywords:
                if keyword not in self.keywords:
                    dhave.append(keyword)
            if len(dhave) > 0:
<<<<<<< HEAD
=======
                '''if int(str(datetime.now().date()-self.dateUntilReturnWeb())[0]) > 7:
                    self.showErrorDialog2()
                    return'''
                
>>>>>>> 900483a863a583d43fe83fe4d211b7e296062a09
                if self.showDialogWebForNew() == 'Yes':      #search new 
                    self.keywords.extend(dhave)
                    # self.wt.keyword = self.keywords
                    # self.dt = self.wt.getDf()
                    self.dt = dm.startSearch([self.dateSinceReturnWeb(),self.dateUntilReturnWeb()],[keyword])
                    dm.concatfile(self.dt)
                    self.addlist()
                else:
                    # self.wt.keyword = self.keyword
                    # self.dt = self.wt.getDf()
                    self.dt = dm.startSearch([self.dateSinceReturnWeb(),self.dateUntilReturnWeb()],[keyword])
                #dm.concatfile(self.dt)
            else:
                self.wt.keyword = keyword
                # self.
                self.dt = self.wt.getDf()
                self.wt.start()
                # self.dt = dm.startSearch([self.dateSinceReturnWeb(),self.dateUntilReturnWeb()],[keyword])
            #self.dateSet()    
            #tw.setdataframe(self.dt)
        self.wt.stop()
        print(self.SearchBox_3.text())
        print(len(self.dt.index),tw.keys)
        
        self.modelNew = TableModel(self.dt) 
        self.table2 = QtWidgets.QTableView()
        self.table2.setModel(self.modelNew)
        self.tableView_3.setModel(self.modelNew)

        #self.labelShowKeywords()
        #dm.startSearch(["16-04-2022","17-04-2022"],['anime','animation'])

    def searchNewWebButton(self) :
        tenwords = self.tw_worddf['Word'].tolist()[:10]  #only top ten words
        tenwords = list(map(lambda x: x.lower(), tenwords))
        if self.showDialogWebForNew() == 'Yes':
            self.keywords.extend(tenwords)
            self.dateSet_3()
            dhave = []
            for keyword in tenwords:
                if keyword not in self.keywords:
                    dhave.append(keyword)
            if len(dhave) > 0:
                self.keywords.extend(dhave)
                self.dt = dm.startSearch([self.dateSinceReturnWeb(),self.dateUntilReturnWeb()],[keyword])
                dm.concatfile(self.dt)
                
            else:
                self.dt = dm.startSearch([self.dateSinceReturnWeb(),self.dateUntilReturnWeb()],[keyword])
            # self.df = tw.savedata(tenwords)
            # print(self.df)
            # dm.concatfile(self.df)
            # self.addlist()
        else:
            return
        #self.addlist_2()    
        self.addlist() 
        self.modelNew = TableModel(self.dt) 
        self.table2 = QtWidgets.QTableView()
        self.table2.setModel(self.modelNew)
        self.tableView_3.setModel(self.modelNew)

    def showErrorDialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Since date less than Until date")
        #msg.setInformativeText('More information')
        msg.setWindowTitle("Period time Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def showErrorDialog2(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Can not search new keyword after 7 days")
        #msg.setInformativeText('More information')
        msg.setWindowTitle("Period time Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    

    def addlist(self): #ของ tab Tweet
        self.listView.clear()
        self.listView_3.clear()
        self.keywords = list(set(np.array(self.keywords,dtype=str)))
        self.keywords.sort()
        print(self.keywords)
        for i in range(len(self.keywords)) :
            item = QtWidgets.QListWidgetItem(self.keywords[i])
            self.listView.addItem(item)
        for i in range(len(self.keywords)) :
            item = QtWidgets.QListWidgetItem(self.keywords[i])
            self.listView_3.addItem(item)
            #self.listView_3.addItem(item)

    def addlist_2(self): #ไว้ add ค่าลงในตารางทางซ้าย (ที่ไว้โชว์ keyword) ของ tab TweetW
        self.listView_2.clear()
        words = self.tw_worddf['Word'].tolist()
        for i in words:
            self.listView_2.addItem(i)
        # for i in range(len(self.keywords)) :
        #     item = QtWidgets.QListWidgetItem(self.keywords[i])
        #     self.listView_2.addItem(item)

    def addlist_3(self): #ของ tab Web scraping
        self.addlist()
        self.listView_3.clear()
        #self.keywords.sort()
        for i in range(len(self.keywords)) :
            item = QtWidgets.QListWidgetItem(self.keywords[i])
            self.listView_3.addItem(item)
        return              

    def deleteButton_3(self) : #สำหรับปุ่ม delete tab web
        deleteKey = self.SearchBox_3.text()
        dm.deletekeyword(deleteKey)
        return
    
    

        

    def progressTime(self,counter): #สำหรับให้ Progress bar ทำงานในช่วงฟังก์ชั่นไหนทำงาน #
                            #ฉะนั้นเวลากดปุ่ม ก็จะเรียกใช้ฟังก์ชั่นนี้แทนการเรียกฟังก์ชั่นปกติตรงๆแทน
        self.progressBar.setValue(counter) #ให้ Progress bar เป็น 100 เมื่อมีการทำงานของฟังก์ชั่นนั้น
        #self.progressBar.setValue(0)
    
    def progressTime_2(self,counter) : #For Tab 2
        self.progressBar_2.setValue(counter)

    def progressTimeWeb(self) :
<<<<<<< HEAD
        #self.percentProgress()
        self.progressBar_3.setValue(100)
        self.showTableWeb()
        self.progressBar_3.setValue(0)


=======
        keywords = self.SearchBox_3.text()
        keywords = keywords.split(',')
        keywords = list(map(lambda x: x.lower(), keywords)) 
        self.progressBar_3.setValue(0)
        sd = self.dateSinceReturnWeb()
        ed = self.dateUntilReturnWeb()
        self.wt = webTread.WebThread(None,sd,ed,keywords)
        self.wt.start()
        self.showTableWeb()
        self.wt.any_signal.connect(self.upgradeProgressWeb)
        
        self.wt.stop()
        self.progressBar_3.setValue(0)
        
    def upgradeProgressWeb(self,val):
        print("upgradeProgressWeb : ",val)
        # val = dm.test()
        self.progressBar_3.setValue(val)
        
>>>>>>> 900483a863a583d43fe83fe4d211b7e296062a09
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 8, 1, 1)
        self.dateEdit_1 = QtWidgets.QDateEdit(self.tab)
        self.dateEdit_1.setObjectName("dateEdit_1")
        self.gridLayout.addWidget(self.dateEdit_1, 0, 7, 1, 1)
        self.dateEdit_2 = QtWidgets.QDateEdit(self.tab)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.gridLayout.addWidget(self.dateEdit_2, 0, 9, 1, 1)

        #self.settime = self.df['Keywords'].apply(lambda x:x**3) #มันเรียกเอา column ทั้งหมดมานับแล้วำนวณเป็นเวลาออกมา
        self.progressBar = QProgressBar(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 7, 5, 1, 5) 

        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 3, 1, 1, 9)
        self.tableView.setModel(self.model) #show table in pyqt5
        #self.progressBar.setMaximum(1)

        self.line = QtWidgets.QFrame(self.tab)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 3, 3, 1)
        self.line_2 = QtWidgets.QFrame(self.tab)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 4, 6, 3, 1)
        self.labelPosTotal = QtWidgets.QLabel(self.tab)
        self.labelPosTotal.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPosTotal.setObjectName("labelPosTotal")
        self.gridLayout.addWidget(self.labelPosTotal, 6, 1, 1, 2)
        self.labelPos = QtWidgets.QLabel(self.tab)
        self.labelPos.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPos.setObjectName("labelPos")
        self.gridLayout.addWidget(self.labelPos, 4, 1, 1, 2)
        self.pushButtonPos = QtWidgets.QPushButton(self.tab)
        self.pushButtonPos.setObjectName("pushButtonPos")
        self.gridLayout.addWidget(self.pushButtonPos, 5, 1, 1, 2)
        self.pushButtonNeu = QtWidgets.QPushButton(self.tab)
        self.pushButtonNeu.setObjectName("pushButtonNeu")
        self.gridLayout.addWidget(self.pushButtonNeu, 5, 7, 1, 3)
        self.pushButtonNega = QtWidgets.QPushButton(self.tab)
        self.pushButtonNega.setObjectName("pushButtonNega")
        self.gridLayout.addWidget(self.pushButtonNega, 5, 4, 1, 2)
        self.labelNega = QtWidgets.QLabel(self.tab)
        self.labelNega.setAlignment(QtCore.Qt.AlignCenter)
        self.labelNega.setObjectName("labelNega")
        self.gridLayout.addWidget(self.labelNega, 4, 4, 1, 2)
        self.labelNegaTotal = QtWidgets.QLabel(self.tab)
        self.labelNegaTotal.setAlignment(QtCore.Qt.AlignCenter)
        self.labelNegaTotal.setObjectName("labelNegaTotal")
        self.gridLayout.addWidget(self.labelNegaTotal, 6, 4, 1, 2)
        self.labelNeutral = QtWidgets.QLabel(self.tab)
        self.labelNeutral.setAlignment(QtCore.Qt.AlignCenter)
        self.labelNeutral.setObjectName("labelNeutral")
        self.gridLayout.addWidget(self.labelNeutral, 4, 7, 1, 3)
        self.labelNeutralTotal = QtWidgets.QLabel(self.tab)
        self.labelNeutralTotal.setAlignment(QtCore.Qt.AlignCenter)
        self.labelNeutralTotal.setObjectName("labelNeutralTotal")
        self.gridLayout.addWidget(self.labelNeutralTotal, 6, 7, 1, 3)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.PushButton_2 = QtWidgets.QPushButton(self.tab)
        self.PushButton_2.setObjectName("PushButton_2")
        self.PushButton_2.clicked.connect(self.showRealtime)

        self.gridLayout.addWidget(self.PushButton_2, 2, 9, 1, 1)
        self.PushButton_1 = QtWidgets.QPushButton(self.tab)
        self.PushButton_1.setObjectName("PushButton_1")
        self.gridLayout.addWidget(self.PushButton_1, 2, 7, 1, 1)
        

        #เป็นวิธีการใส่พารามิเตอร์ลงไปในฟังก์ชั่นที่ต้องการเชื่อมกับปุ่ม
        #คือเวลาเชื่อมกับปุ่มมันใส่พารามิเตอร์ลงไปแบบ self.PushButton_1.clicked.connect(self.showSecondFile("WebScrapingData24.csv")) 
        #ถ้าใส่แบบนั้นมันจะบัค เลยต้องใช้ functools มาช่วย
        #btm1 = functools.partial()
        #self.PushButton_1.clicked.connect(self.progressTime)
        self.PushButton_1.clicked.connect(self.button1)

        #สร้างไว้สำหรับรีเฟรช
        btmRefresh_1 = functools.partial(self.refreshButton_1)   
        self.PushButtonRefresh = QtWidgets.QPushButton(self.tab)
        self.PushButtonRefresh.setObjectName("PushButtonRefresh")
        self.PushButtonRefresh.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.PushButtonRefresh.setIcon(QtGui.QIcon('reload_update_refresh_icon_143703.png')) #ไว้เชือมรูป
        self.PushButtonRefresh.clicked.connect(btmRefresh_1) #เชื่อมปุ่มได้แบบปกติเลย

        self.PushButtonDelete = QtWidgets.QPushButton(self.tab)
        self.PushButtonDelete.setObjectName("PushButtonDelete")
        self.PushButtonDelete.setGeometry(QtCore.QRect(50, 10, 30, 30))
        self.PushButtonDelete.setIcon(QtGui.QIcon('3481306.png')) #ไว้เชือมรูป
        self.PushButtonDelete.clicked.connect(self.deleteButton_1) #เชื่อมปุ่มได้แบบปกติเลย

        self.listView = QtWidgets.QListWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setMidLineWidth(0)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 3, 0, 4, 1)
        #self.addlist()

        self.SearchBox1 = QtWidgets.QLineEdit(self.tab)
        self.SearchBox1.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchBox1.sizePolicy().hasHeightForWidth())
        self.SearchBox1.setSizePolicy(sizePolicy)
        self.SearchBox1.setObjectName("SearchBox1")
        self.gridLayout.addWidget(self.SearchBox1, 2, 1, 1, 6)
        #test = self.SearchBox1.text() #text
        #checkNew1 = functools.partial(self.checkInput,self.SearchBox1.text())
        #self.PushButton_1.clicked.connect(checkNew1)

        self.label_1 = QtWidgets.QLabel(self.tab)
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 1, 2, 1, 1)
        #self.processBarGUI()
        self.tabWidget.addTab(self.tab, "")
        

        #tab2 
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        
        '''self.dateEdit_3 = QtWidgets.QDateEdit(self.tab_2)
        self.dateEdit_3.setObjectName("dateEdit_3")
        self.gridLayout.addWidget(self.dateEdit_3, 0, 3, 1, 1)
        self.dateEdit_4 = QtWidgets.QDateEdit(self.tab_2)
        self.dateEdit_4.setObjectName("dateEdit_4")
        self.gridLayout.addWidget(self.dateEdit_4, 0, 5, 1, 1)'''
        #เผื่อใช้ เป็นวันที่ของ tab tweetw

        self.tableView_2 = QtWidgets.QTableView(self.tab_2)
        self.tableView_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_2.sizePolicy().hasHeightForWidth())
        self.tableView_2.setSizePolicy(sizePolicy)
        self.tableView_2.setObjectName("tableView_2")
        self.gridLayout.addWidget(self.tableView_2, 3, 1, 1, 5)
        ################# โชว์ df ใน tab tweetw
        self.tableView_2.setModel(self.model) #show table in pyqt5
        #################

        self.progressBar_2 = QProgressBar(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar_2.sizePolicy().hasHeightForWidth())
        self.progressBar_2.setSizePolicy(sizePolicy)
        self.progressBar_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar_2.setTextVisible(True)
        self.progressBar_2.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_2.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_2.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar_2, 4, 4, 1, 2)

        self.label_4 = QtWidgets.QLabel(self.tab_2) #แสดงคำว่า "Tweeter keyword"
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label1")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 6)
        self.label_5 = QtWidgets.QLabel(self.tab_2) #แสดงคำว่า "Keyword"
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label2")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        '''self.label_6 = QtWidgets.QLabel(self.tab_2) #แสดงคำว่า "to"
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 4, 1, 1, QtCore.Qt.AlignHCenter)'''

        self.PushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.PushButton_4.setObjectName("PushButton_4")
        self.PushButton_4.clicked.connect(self.showDefaultFileTweetW)

        self.gridLayout.addWidget(self.PushButton_4, 2, 5, 1, 1)
        self.PushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.PushButton_3.setObjectName("PushButton_3")
        self.gridLayout.addWidget(self.PushButton_3, 2, 4, 1, 1)
        

        #เป็นวิธีการใส่พารามิเตอร์ลงไปในฟังก์ชั่นที่ต้องการเชื่อมกับปุ่ม
        #คือเวลาเชื่อมกับปุ่มมันใส่พารามิเตอร์ลงไปแบบ self.PushButton_1.clicked.connect(self.showSecondFile("WebScrapingData24.csv")) 
        #ถ้าใส่แบบนั้นมันจะบัค เลยต้องใช้ functools มาช่วย
        btm2 = functools.partial(self.button2)   
        self.PushButton_3.clicked.connect(btm2)

        self.listView_2 = QtWidgets.QListWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_2.sizePolicy().hasHeightForWidth())
        self.listView_2.setSizePolicy(sizePolicy)
        self.listView_2.setMidLineWidth(0)
        self.listView_2.setObjectName("listView_2")
        self.gridLayout.addWidget(self.listView_2, 3, 0, 1, 1)
        #self.addlist_2()
        
        self.labelShow = QtWidgets.QLabel(self.tab_2)
        self.labelShow.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelShow.sizePolicy().hasHeightForWidth())
        self.labelShow.setSizePolicy(sizePolicy)
        self.labelShow.setObjectName("labelShow")
        self.gridLayout.addWidget(self.labelShow, 2, 1, 1, 3, QtCore.Qt.AlignHCenter)
        #test = self.SearchBox1.text() #text
        #checkNew1 = functools.partial(self.checkInput,self.SearchBox1.text())
        #self.PushButton_1.clicked.connect(checkNew1)
        self.tabWidget.addTab(self.tab_2, "")


        #tab3 
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout.setObjectName("gridLayout")
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 4, 1, 1, QtCore.Qt.AlignHCenter)
        self.dateEdit_5 = QtWidgets.QDateEdit(self.tab_3)
        self.dateEdit_5.setObjectName("dateEdit_5")
        self.gridLayout.addWidget(self.dateEdit_5, 0, 3, 1, 1)
        self.dateEdit_6 = QtWidgets.QDateEdit(self.tab_3)
        self.dateEdit_6.setObjectName("dateEdit_6")
        self.gridLayout.addWidget(self.dateEdit_6, 0, 5, 1, 1)

        self.tableView_3 = QtWidgets.QTableView(self.tab_3)
        self.tableView_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_3.sizePolicy().hasHeightForWidth())
        self.tableView_3.setSizePolicy(sizePolicy)
        self.tableView_3.setObjectName("tableView_3")
        self.gridLayout.addWidget(self.tableView_3, 3, 1, 1, 5)
        self.tableView_3.setModel(self.modelWeb) #show table in pyqt5

        self.label_8 = QtWidgets.QLabel(self.tab_3)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label2")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)

        self.PushButton_6 = QtWidgets.QPushButton(self.tab_3)
        self.PushButton_6.setObjectName("PushButton_6")
        self.PushButton_6.clicked.connect(self.showCalenderWin)

        self.gridLayout.addWidget(self.PushButton_6, 2, 5, 1, 1)
        self.PushButton_5 = QtWidgets.QPushButton(self.tab_3)
        self.PushButton_5.setObjectName("PushButton_5")
        self.gridLayout.addWidget(self.PushButton_5, 2, 4, 1, 1)
        self.PushButton_5.clicked.connect(self.progressTimeWeb)
        

        #เป็นวิธีการใส่พารามิเตอร์ลงไปในฟังก์ชั่นที่ต้องการเชื่อมกับปุ่ม
        #คือเวลาเชื่อมกับปุ่มมันใส่พารามิเตอร์ลงไปแบบ self.PushButton_1.clicked.connect(self.showSecondFile("WebScrapingData24.csv")) 
        #ถ้าใส่แบบนั้นมันจะบัค เลยต้องใช้ functools มาช่วย
        #btm1 = functools.partial(self.button1)   
        #self.PushButton_6.clicked.connect(btm1)

        self.progressBar_3 = QProgressBar(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar_3.setSizePolicy(sizePolicy)
        self.progressBar_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar_3.setTextVisible(False)
        self.progressBar_3.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_3.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_3.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar_3, 4,4, 1, 2) 

        self.listView_3 = QtWidgets.QListWidget(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_3.sizePolicy().hasHeightForWidth())
        self.listView_3.setSizePolicy(sizePolicy)
        self.listView_3.setMidLineWidth(0)
        self.listView_3.setObjectName("listView_3")
        self.gridLayout.addWidget(self.listView_3, 3, 0, 1, 1)
        #self.addlist_3()
        self.addlist()
        self.SearchBox_3 = QtWidgets.QLineEdit(self.tab_3)
        self.SearchBox_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchBox_3.sizePolicy().hasHeightForWidth())
        self.SearchBox_3.setSizePolicy(sizePolicy)
        self.SearchBox_3.setObjectName("SearchBox1")
        self.gridLayout.addWidget(self.SearchBox_3, 2, 1, 1, 3)
        #test = self.SearchBox1.text() #text
        #checkNew1 = functools.partial(self.checkInput,self.SearchBox1.text())
        #self.PushButton_1.clicked.connect(checkNew1)

        self.PushButtonRefresh_3 = QtWidgets.QPushButton(self.tab_3)
        self.PushButtonRefresh_3.setObjectName("PushButtonRefresh_3")
        self.PushButtonRefresh_3.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.PushButtonRefresh_3.setIcon(QtGui.QIcon('reload_update_refresh_icon_143703.png')) #ไว้เชือมรูป
        #btmRefresh_2 = functools.partial(self.refreshButton)   
        #self.PushButtonRefresh_3.clicked.connect(btmRefresh_2)

        self.PushButtonDelete_3 = QtWidgets.QPushButton(self.tab_3)
        self.PushButtonDelete_3.setObjectName("PushButtonDelete_3")
        self.PushButtonDelete_3.setGeometry(QtCore.QRect(50, 10, 30, 30))
        self.PushButtonDelete_3.setIcon(QtGui.QIcon('3481306.png')) #ไว้เชือมรูป
        self.PushButtonDelete_3.clicked.connect(self.deleteButton_3) 

        self.label_7 = QtWidgets.QLabel(self.tab_3)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label1")
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 6)
        self.dateSet_3()
        self.dateSet() #เรียกใช้ฟังก์ชั่นที่ตัดเวลาออก และคืนค่าวันที่ออกมา หากมีการเปลี่ยนแปลงวันที่ผ่านตัว GUI
        
        self.tabWidget.addTab(self.tab_3, "")


        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Main"))
        self.label_1.setText(_translate("MainWindow", "Twitter keyword"))
        self.label_2.setText(_translate("MainWindow", "Keyword"))
        self.label_3.setText(_translate("MainWindow", "to"))
        self.labelPosTotal.setText(_translate("MainWindow", "Total 100 tweets"))
        self.labelPos.setText(_translate("MainWindow", "Positive"))
        self.labelNega.setText(_translate("MainWindow", "Negative"))
        self.labelNeutral.setText(_translate("MainWindow", "Neutral"))
        self.labelNegaTotal.setText(_translate("MainWindow", "Total 200 tweets"))
        self.labelNeutralTotal.setText(_translate("MainWindow", "Total 300 tweets"))
        self.PushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButtonPos.setText(_translate("MainWindow", "Pos"))
        self.pushButtonNeu.setText(_translate("MainWindow", "Neu"))
        self.pushButtonNega.setText(_translate("MainWindow", "Nega"))
        self.PushButton_1.setText(_translate("MainWindow", "Search"))
        self.PushButton_2.setText(_translate("MainWindow", "Search new"))
        self.PushButtonRefresh.setText(_translate("MainWindow", ""))
        self.PushButtonDelete.setText(_translate("MainWindow", ""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tweet"))

        self.PushButton_3.setText(_translate("MainWindow", "Search"))
        self.PushButton_4.setText(_translate("MainWindow", "Default"))
        self.label_4.setText(_translate("MainWindow", "Twitter keyword"))
        self.label_5.setText(_translate("MainWindow", "Keyword"))
        #self.label_6.setText(_translate("MainWindow", "to"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "TweetW"))

        self.PushButton_5.setText(_translate("MainWindow", "Search"))
        self.PushButton_6.setText(_translate("MainWindow", "Search new"))
        self.PushButtonRefresh_3.setText(_translate("MainWindow", ""))
        self.PushButtonDelete_3.setText(_translate("MainWindow", ""))
        self.label_7.setText(_translate("MainWindow", "Web scraping"))
        self.label_8.setText(_translate("MainWindow", "Keyword"))
        self.label_9.setText(_translate("MainWindow", "to"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Webscraping"))

        self.dateEdit_1.setDisplayFormat(_translate("MainWindow", "yyyy/M/d")) #format ของวันที่ที่แสดง
        self.dateEdit_2.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))
        self.dateEdit_5.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))
        self.dateEdit_6.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))


if __name__ == "__main__":
    dm = DataManager.DataManager()
    tw = twitter_scrap.Twitter_Scrap()
    #Dialog = QtWidgets.QDialog()
    cn = webNewNew.Ui_MainWindowSecond()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
