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
from os.path import dirname, realpath, join
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidget, QTableWidgetItem,QMessageBox
import numpy as np
from datetime import datetime
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import functools
import importWin as windo 
#class SearchKeyTweet() :
#class SearchLinkWeb() :

    

    #def getDate(self) :
        #Ui_MainWindow().__init__()
        
        

'''class ImportWindow(QtWidgets.QMainWindow):
    scriptDir = dirname(realpath(__file__))
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.path = ""
        self.df = ""
        self.textLabel = str
        

    def openWindow(self):
        self.window = QtWidgets.QMainWindow() 
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def showQues(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure to select this file?")
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        #msgBox.buttonClicked.connect(msgButtonClick)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes: #If press yes
            self.hide()
            self.openWindow()
        if returnValue == QMessageBox.No:
            print("No")
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(385, 120)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(90, 60, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(win.OpenFile)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 60, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 55, 16))
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(90, 30, 191, 16))
        self.label2.setObjectName("label2")
        
        #checkNew = functools.partial(self.addPathList,self.path)
        #.label2.setText(self,self.addFile)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 20, 81, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.showQues)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 385, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi2(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi2(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Import file"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))
        self.pushButton_3.setText(_translate("MainWindow", "Confirm"))
        self.label.setText(_translate("MainWindow", "File name"))
        self.label2.setText(_translate("MainWindow", "None"))

    def Close(self):
        MainWindow.close()
'''
        
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
        self.df = pd.read_csv("tweet_data_2732022.csv", encoding='utf8',index_col=False) #win.readFile(win.path) save tweet file
        self.dt = pd.read_csv("WebScrapingData24.csv", encoding='utf8',index_col=False)
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
        self.keywords = ['bl anime','anime comedy','anime romance','ต่างโลก','anime','animation','shounen','pixar',
        'harem','fantasy anime','sport anime','from manga','disney animation','animation studio',
        'shounen ai','shoujo','อนิเมะ','2d animation','อนิเมะแนะนำ','japan animation']


    def showSecondFile(self) : #ถ้าเรียกฟังก์ชั่นนี้ จะแทนที่ตารางอันเก่าที่ใช้คำสั่งว่า self.tableView.setModel(self.model)
        self.model2 = TableModel(self.dt) # อยากได้ไฟล์ไหนไปใส่ในตาราง แทนที่ self.dt เลย
        self.table2 = QtWidgets.QTableView()
        self.table2.setModel(self.model2) #เอา df แปลงเป็นตารางเรียบร้อย
        self.tableView.setModel(self.model2) #เอาตารางไปโชว์เลย

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
                df = pd.read_csv(path, encoding='windows-1252')
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

    def setDate(self) :
        self.df['Time'] = pd.to_datetime(self.df['Time']).dt.date
        self.df['Time'] = pd.to_datetime(self.df['Time']).dt.strftime('%Y-%m-%d')
        #self.rangeDate()
        #self.minDate()
        #(type(self.d))
        #return self.data, self.d, self.f

    '''def maxDate(self) :
        self.earliest = (self.data['Time'].max()).toPyDate()
        return self.earliest
    def minDate(self) :
        self.lasted = (self.data['Time'].min()).toPyDate()
        return self.lasted
        #print(type(self.lasted))
    def rangeDate(self) :
        #self.maxDate()
        #self.minDate()
        start_date = self.earliest
        end_date = self.lasted
        mask = (self.data['Time'] > start_date) & (self.data['Time'] <= end_date)
        print(mask)

    def getDate1(self,getDate) :
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
        self.PushButton1.setObjectName("PushButton1") #search button in tweet
        #print(self.checkInput(self.SearchBox1.text()))
        checkNew1 = functools.partial(self.checkInput,self.SearchBox1.text())
        
        self.PushButton1.clicked.connect(checkNew1)

        self.PushButton_2 = QtWidgets.QPushButton(self.tab)
        self.PushButton_2.setGeometry(QtCore.QRect(625, 70, 93, 28))
        self.PushButton_2.setObjectName("PushButton_2")
        

        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setGeometry(QtCore.QRect(190, 140, 561, 331))
        self.tableView.setObjectName("tableView")

        self.setDate()
        self.tableView.setModel(self.model) #show table in pyqt5
        #############################
        #self.showSecondFile() 


        self.listView = QtWidgets.QListWidget(self.tab)
        self.listView.setGeometry(QtCore.QRect(20, 140, 151, 331))
        self.listView.setObjectName("listView")
        for i in range(len(self.keywords)) :
            item = QtWidgets.QListWidgetItem(self.keywords[i])
            self.listView.addItem(item)
        
        self.dateEdit = QtWidgets.QDateEdit(self.tab)
        self.dateEdit.setGeometry(QtCore.QRect(40, 10, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        #checkNew2 = functools.partial(self.getDate1,self.dateEdit.date().toPyDate())
        #print(self.dateEdit.date().toPyDate())
        #self.PushButton_2.clicked.connect(checkNew2)
        #self.dateEdit.setMinimumDate(QDate(1, 1, 1900))
        
        #self.dateEdit.dateTime(self.lasted , '%d %b %Y')
        #self.dateEdit.setDate(self.d)

        self.dateEdit_2 = QtWidgets.QDateEdit(self.tab)
        self.dateEdit_2.setGeometry(QtCore.QRect(180, 10, 110, 22))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        #checkNew3 = functools.partial(self.getDate2,self.dateEdit_2.date().toPyDate())
        #print(self.dateEdit.date().toPyDate())
        #self.PushButton_2.clicked.connect(checkNew3)


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
        #print(type(self.data))

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #print(self.getDataDate1)
        #return self.getDataDate1
        #self.tableV.horizontalHeader().sectionClicked.connect(self.on_header_doubleClicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label1.setText(_translate("MainWindow", "Twitter keyword"))
        self.label2.setText(_translate("MainWindow", "Keyword"))
        self.PushButton1.setText(_translate("MainWindow", "Search"))
        self.PushButton_2.setText(_translate("MainWindow", "Refresh"))
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
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    win = windo.scrapingManager()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
