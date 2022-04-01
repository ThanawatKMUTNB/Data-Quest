from ast import keyword
import encodings
from msilib.schema import ListView
from xml.etree.ElementTree import tostring
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import Qt, QDate
import pandas as pd
import os
import sqlite3
import glob
from os.path import dirname, realpath, join
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidget, QTableWidgetItem,QMessageBox
import numpy as np
from datetime import datetime, timedelta
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import functools
import importWin as windo 

import DataManager
import twitter_scrap 
#class SearchKeyTweet() :
#class SearchLinkWeb() :
    #def getDate(self) :
        #Ui_MainWindow().__init__()
        #       
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
        self.table = QtWidgets.QTableView()
        self.filename = glob.glob(str(str(os.getcwd())+"\\Backup_Data\\*.csv"))
        self.df = dm.unionfile(self.filename) #win.readFile(win.path) save tweet file
        tw.setdataframe(self.df)
        
        #self.data = win.OpenFile()
        #pd.read_csv("tweet_data_2032022.csv", encoding='utf8',index_col=False)
        self.getSince = str
        self.getUntil = str
        self.earliest = None
        self.lasted = None
        self.getDataDate1 = None
        self.getDataDate2 = None
        self.model = TableModel(self.df)
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        

        #self.maxDate()
        #self.setDate()
        self.keywords = self.df['Keyword'].tolist()
        self.keywords = list(set(self.keywords))

    def dateSet(self) :
        date = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        self.dateEdit.setDate(date) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit.dateChanged.connect(self.dateSinceReturn) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

        date2 = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        self.dateEdit_2.setDate(date2) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_2.dateChanged.connect(self.dateUntilReturn) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

    def dateSinceReturn(self) :
        self.getSince = self.dateEdit.date().toPyDate() #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getSince)
        return self.getSince

    def dateUntilReturn(self) :
        self.getUntil = self.dateEdit_2.date().toPyDate() #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getUntil)
        return self.getUntil

    def showDefaultFile(self) :
        self.df = dm.setdefaultDF()
        #self.df = dm.unionfile(self.filename)
        self.df = dm.getperiod(str(self.dateSinceReturn()),str(self.dateUntilReturn()))
        print(len(self.df.index),tw.keys)
        self.model = TableModel(self.df) 
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model) #เอา df แปลงเป็นตารางเรียบร้อย
        self.tableView.setModel(self.model) #เอาตารางไปโชว์เลย

    def button1(self) :
        print("\n\n")
        print(len(self.df.index))
        print(self.dateSinceReturn(),self.dateUntilReturn())
        self.df = dm.getperiod(str(self.dateSinceReturn()),str(self.dateUntilReturn()))
        
        tw.setdataframe(self.df)
        keyword = self.SearchBox1.text()
        if not(keyword == None or keyword == ""):
            self.dateSet()
            self.df = tw.searchkeys(keyword)
            dm.concatfile(self.df)
            if (keyword not in self.keywords):
                #dm.concatfile(self.df)
                print(len(self.df.index))
                print(len(dm.df.index))
                self.keywords.append(keyword)
                self.addlist()
            tw.setdataframe(self.df)
        #print(self.SearchBox1.text())
        print(len(self.df.index),tw.keys)
        self.model = TableModel(self.df) 
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.tableView.setModel(self.model)

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

    def showDialog(self,keys): #ไว้เด้งข้อความขึ้นมา ถ้าตัวที่ป้อนเข้ามาใน entry ไม่มีอยู่ใน keywords ที่กำหนด
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure?") #แสดงข้อความ
        msgBox.setWindowTitle("Warning") #Title
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No) #มีปุ่ม yes และ no
        #ถ้าอยากเปลี่ยนปุ่ทเป็นแบบอื่น เปลี่ยนจากพวก yes หรือ no ได้เลย เช่น Save Cancel Ok Close Open
        #msgBox.buttonClicked.connect(msgButtonClick) ไม่มีไร เป็นการเชื่อมเวลากดปุ่ม ซึ่งในตอนนี้ไม่ได้เชื่อมฟังก์ชั่นอะไรไว้ 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes: #ถ้ากด yes จะทำอะไร
            self.keywords.append(keys)
            print(keys)
            return self.keywords
        #if returnValue == QMessageBox.No: #ถ้ากด no จะทำอะไร

    def checkInput(self,keys) :
        if keys not in self.keywords :
            self.showDialog(self.SearchBox1.text())
            return keys
        else :
            print("OK")

    def addlist(self):
        print(self.keywords)
        for i in range(len(self.keywords)) :
            item = QtWidgets.QListWidgetItem(self.keywords[i])
            self.listView.addItem(item)
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(812, 589)
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
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.dateEdit = QtWidgets.QDateEdit(self.tab)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 0, 0, 1, 1)
        self.dateEdit_2 = QtWidgets.QDateEdit(self.tab)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.gridLayout.addWidget(self.dateEdit_2, 0, 2, 1, 1)

        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 3, 1, 1, 5)
        self.tableView.setModel(self.model) #show table in pyqt5

        self.label2 = QtWidgets.QLabel(self.tab)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setObjectName("label2")
        self.gridLayout.addWidget(self.label2, 2, 0, 1, 1)

        self.PushButton_2 = QtWidgets.QPushButton(self.tab)
        self.PushButton_2.setObjectName("PushButton_2")
        self.PushButton_2.clicked.connect(self.showDefaultFile)

        self.gridLayout.addWidget(self.PushButton_2, 2, 5, 1, 1)
        self.PushButton1 = QtWidgets.QPushButton(self.tab)
        self.PushButton1.setObjectName("PushButton1")
        self.gridLayout.addWidget(self.PushButton1, 2, 4, 1, 1)
        

        #เป็นวิธีการใส่พารามิเตอร์ลงไปในฟังก์ชั่นที่ต้องการเชื่อมกับปุ่ม
        #คือเวลาเชื่อมกับปุ่มมันใส่พารามิเตอร์ลงไปแบบ self.PushButton1.clicked.connect(self.showSecondFile("WebScrapingData24.csv")) 
        #ถ้าใส่แบบนั้นมันจะบัค เลยต้องใช้ functools มาช่วย
        btm1 = functools.partial(self.button1)   
        self.PushButton1.clicked.connect(btm1)

        self.listView = QtWidgets.QListWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setMidLineWidth(0)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 3, 0, 1, 1)
        self.addlist()
        
        self.SearchBox1 = QtWidgets.QLineEdit(self.tab)
        self.SearchBox1.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchBox1.sizePolicy().hasHeightForWidth())
        self.SearchBox1.setSizePolicy(sizePolicy)
        self.SearchBox1.setObjectName("SearchBox1")
        self.gridLayout.addWidget(self.SearchBox1, 2, 1, 1, 3)
        test = self.SearchBox1.text() 
        checkNew1 = functools.partial(self.checkInput,test)
        self.PushButton1.clicked.connect(checkNew1)

        self.label1 = QtWidgets.QLabel(self.tab)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setObjectName("label1")
        self.gridLayout.addWidget(self.label1, 1, 0, 1, 6)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.textEdit = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit.setGeometry(QtCore.QRect(140, 100, 391, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.tab_2)
        self.pushButton.setGeometry(QtCore.QRect(550, 100, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(660, 100, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(40, 110, 71, 16))
        self.label.setObjectName("label")

        self.listView_2 = QtWidgets.QListWidget(self.tab_2)
        self.listView_2.setGeometry(QtCore.QRect(20, 140, 151, 331))
        self.listView_2.setObjectName("listView_2")
        #วน add keywords ท้ังหมดเข้าไปในตารางของ GUI
        for i in range(len(self.keywords)) :
            item = QtWidgets.QListWidgetItem(self.keywords[i])
            self.listView_2.addItem(item)

        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(290, 60, 151, 20))
        self.label_2.setObjectName("label_2")
        self.dateEdit_3 = QtWidgets.QDateEdit(self.tab_2)
        self.dateEdit_3.setGeometry(QtCore.QRect(40, 10, 110, 22))
        self.dateEdit_3.setObjectName("dateEdit_3")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(160, 10, 16, 21))
        self.label_4.setObjectName("label_4")
        self.dateEdit_4 = QtWidgets.QDateEdit(self.tab_2)
        self.dateEdit_4.setGeometry(QtCore.QRect(180, 10, 110, 22))
        self.dateEdit_4.setObjectName("dateEdit_4")
        self.dateSet() #เรียกใช้ฟังก์ชั่นที่ตัดเวลาออก และคืนค่าวันที่ออกมา หากมีการเปลี่ยนแปลงวันที่ผ่านตัว GUI
        self.listWidget = QtWidgets.QListWidget(self.tab_2)
        self.listWidget.setGeometry(QtCore.QRect(20, 160, 151, 331))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setObjectName("listWidget")
        self.tabWidget.addTab(self.tab_2, "")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label1.setText(_translate("MainWindow", "Twitter keyword"))
        self.label2.setText(_translate("MainWindow", "Keyword"))
        self.PushButton1.setText(_translate("MainWindow", "Search"))
        self.PushButton_2.setText(_translate("MainWindow", "Default"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.pushButton.setText(_translate("MainWindow", "Search"))
        self.pushButton_2.setText(_translate("MainWindow", "Refresh"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "Web scraping"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.dateEdit.setDisplayFormat(_translate("MainWindow", "yyyy/M/d")) #format ของวันที่ที่แสดง
        self.dateEdit_2.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))
        self.dateEdit_3.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))
        self.dateEdit_4.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))


if __name__ == "__main__":
    dm = DataManager.DataManager()
    tw = twitter_scrap.Twitter_Scrap()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
