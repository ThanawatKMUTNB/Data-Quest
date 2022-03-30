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

    def showDialog(self,keys):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure?")
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        #msgBox.buttonClicked.connect(msgButtonClick)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes: #If press yes
            self.keywords.append(keys)
            print(self.keywords)
            return self.keywords
        #if returnValue == QMessageBox.No: #If press no

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


    '''def getDate1(self,getDate) :
        #self.getDataDate1 = self.dateEdit.date().toPyDate()
        self.getDataDate1 = getDate
        print(self.getDataDate1)
        return self.getDataDate1 
    def getDate2(self,getDate) :
        #self.getDataDate1 = self.dateEdit.date().toPyDate()
        self.getDataDate2 = getDate
        print(self.getDataDate2)
        return self.getDataDate2 '''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 20, 791, 551))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label1 = QtWidgets.QLabel(self.tab)
        self.label1.setGeometry(QtCore.QRect(290, 40, 151, 20))
        self.label1.setObjectName("label1")
        self.SearchBox1 = QtWidgets.QLineEdit(self.tab)
        self.SearchBox1.setGeometry(QtCore.QRect(145, 70, 351, 31))
        self.SearchBox1.setObjectName("SearchBox1")
        #self.SearchBox1.QInputDialog.getText(self.checkInput)
        
        self.label2 = QtWidgets.QLabel(self.tab)
        self.label2.setGeometry(QtCore.QRect(45, 80, 81, 20))
        self.label2.setObjectName("label2")
        self.PushButton1 = QtWidgets.QPushButton(self.tab)
        self.PushButton1.setGeometry(QtCore.QRect(515, 70, 93, 28))
        self.PushButton1.setObjectName("PushButton1")           #search button in tweet
        #print(self.checkInput(self.SearchBox1.text()))
        

        #เป็นวิธีการใส่พารามิเตอร์ลงไปในฟังก์ชั่นที่ต้องการเชื่อมกับปุ่ม
        #คือเวลาเชื่อมกับปุ่มมันใส่พารามิเตอร์ลงไปแบบ self.PushButton1.clicked.connect(self.showSecondFile("WebScrapingData24.csv")) 
        #ถ้าใส่แบบนั้นมันจะบัค เลยต้องใช้ functools มาช่วย
        btm1 = functools.partial(self.button1)   
        self.PushButton1.clicked.connect(btm1)

        #checkNew1 = functools.partial(self.checkInput,self.SearchBox1.text())   
        #self.PushButton1.clicked.connect(self.PushButton1.clicked.connect(checkNew1)

        self.PushButton_2 = QtWidgets.QPushButton(self.tab)
        self.PushButton_2.setGeometry(QtCore.QRect(625, 70, 93, 28))
        self.PushButton_2.setObjectName("PushButton_2")
        self.PushButton_2.clicked.connect(self.showDefaultFile)

        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setGeometry(QtCore.QRect(190, 140, 561, 331))
        self.tableView.setObjectName("tableView")
        self.tableView.setModel(self.model) #show table in pyqt5

        self.listView = QtWidgets.QListWidget(self.tab)
        self.listView.setGeometry(QtCore.QRect(20, 140, 151, 331))
        self.listView.setObjectName("listView")
        self.addlist()
        
        self.dateEdit = QtWidgets.QDateEdit(self.tab)
        self.dateEdit.setGeometry(QtCore.QRect(40, 10, 110, 22))
        self.dateEdit.setObjectName("dateEdit")

         #เรียกใช้ฟังก์ชั่นที่ตัดเวลาออก และคืนค่าวันที่ออกมา หากมีการเปลี่ยนแปลงวันที่ผ่านตัว GUI
        self.dateEdit_2 = QtWidgets.QDateEdit(self.tab)
        self.dateEdit_2.setGeometry(QtCore.QRect(180, 10, 110, 22))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.dateSet()

        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(160, 10, 16, 21))
        self.label_3.setObjectName("label_3")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.textEdit = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit.setGeometry(QtCore.QRect(150, 70, 341, 31))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.tab_2)
        self.pushButton.setGeometry(QtCore.QRect(520, 70, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(630, 70, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(50, 80, 101, 16))
        self.label.setObjectName("label")

        self.tableView2 = QtWidgets.QTableView(self.tab_2)
        self.tableView2.setGeometry(QtCore.QRect(40, 130, 681, 361))
        self.tableView2.setObjectName("tableView2")

        #self.tableView2.setModel(self.model2)

        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(300, 20, 151, 20))
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
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
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
        self.dateEdit.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))
        self.dateEdit_2.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))
        self.dateEdit_3.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))
        self.dateEdit_4.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))

    #def clickMethod(self):

if __name__ == "__main__":
    dm = DataManager.DataManager()
    tw = twitter_scrap.Twitter_Scrap()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    win = windo.scrapingManager()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
