from ast import keyword
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
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
#class SearchKeyTweet() :
#class SearchLinkWeb() :

    

    #def getDate(self) :
        #Ui_MainWindow().__init__()
        
        


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
        self.data = pd.read_csv("tweet_data_1932022.csv", encoding='utf8',index_col=False)
        self.model = TableModel(self.data)
        self.table.setModel(self.model)
        self.table = QtWidgets.QTableView()
        #self.maxDate()
        #self.setDate()
        self.keywords = ['bl anime','anime comedy','anime romance','ต่างโลก','anime','animation','shounen','pixar',
        'harem','fantasy anime','sport anime','from manga','disney animation','animation studio',
        'shounen ai','shoujo','อนิเมะ','2d animation','อนิเมะแนะนำ','japan animation']
        
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

    '''def setDate(self) :
        self.data['Time'] = pd.to_datetime(self.data['Time']).dt.date
        self.data['Time'] = pd.to_datetime(self.data['Time']).dt.strftime('%d/%m/%Y')

    def maxDate(self) :
        self.setDate()
        print(self.data['Time'].min(), self.data['Time'].max())

    def rangeDate(self) :
        self.d = QDate(self.data['Time'].min())'''
        

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
        self.label1.setGeometry(QtCore.QRect(309, 20, 91, 20))
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
        checkNew = functools.partial(self.checkInput,self.SearchBox1.text())
        
        self.PushButton1.clicked.connect(checkNew)

        self.PushButton_2 = QtWidgets.QPushButton(self.tab)
        self.PushButton_2.setGeometry(QtCore.QRect(625, 70, 93, 28))
        self.PushButton_2.setObjectName("PushButton_2")

        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setGeometry(QtCore.QRect(40, 130, 711, 331))
        self.tableView.setObjectName("tableView")

        #self.setDate()
        self.tableView.setModel(self.model) #show table in pyqt5

        self.dateEdit = QtWidgets.QDateEdit(self.tab)
        self.dateEdit.setGeometry(QtCore.QRect(40, 10, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        #self.dateEdit.setDate(self.d)

        self.dateEdit_2 = QtWidgets.QDateEdit(self.tab)
        self.dateEdit_2.setGeometry(QtCore.QRect(180, 10, 110, 22))
        self.dateEdit_2.setObjectName("dateEdit_2")
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
        self.listView = QtWidgets.QListView(self.tab_2)
        self.listView.setGeometry(QtCore.QRect(40, 130, 681, 361))
        self.listView.setObjectName("listView")
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
        #self.tableV.horizontalHeader().sectionClicked.connect(self.on_header_doubleClicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label1.setText(_translate("MainWindow", "Twitter keyword"))
        self.label2.setText(_translate("MainWindow", "Keyword"))
        self.PushButton1.setText(_translate("MainWindow", "Search"))
        self.PushButton_2.setText(_translate("MainWindow", "Refresh"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "Web scraping"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))

    #def clickMethod(self):

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
