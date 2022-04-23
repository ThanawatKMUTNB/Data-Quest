import calendar
from ast import keyword
import encodings
from msilib.schema import ListView
from tabnanny import check
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

import DataManager
import twitter_scrap
import webNewNew
from Tw_Thread import *
import scrapingGUI


class Ui_MainWindowSecond(object):
    def __init__(self):
        super().__init__()
        self.qDateBegin = str
        self.qDateEnd = str
        self.enterM = str

    def showTableWebNewTab(self) :
        print("\n\n")
        #print(len(self.dt.index),'rows')
        print(self.dateSinceReturnWeb(),self.dateUntilReturnWeb())
        '''if self.dateSinceReturnWeb()>self.dateUntilReturnWeb():
            self.showErrorDialog()
            return'''
        self.dt = DataManager.DataManager().getperiod(str(self.dateSinceReturnWeb()),str(self.dateUntilReturnWeb()))
        print(list(set(self.dt['Keyword'].tolist())))
        twitter_scrap.Twitter_Scrap().setdataframe(self.dt)
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
                '''if int(str(datetime.now().date()-self.dateUntilReturnWeb())[0]) > 7:
                    self.showErrorDialog2()
                    return'''
                if self.showDialogWebForNew() == 'Yes':      #search new 
                    self.keywords.extend(dhave)
                    self.dt = DataManager.DataManager().startSearch([self.dateSinceReturnWeb(),self.dateUntilReturnWeb()],[keyword])
                    DataManager.DataManager().concatfile(self.dt)
                    #print(list(set(dm.df['Keyword'].tolist())))
                    self.addlist()
                else:
                    self.dt = DataManager.DataManager().startSearch([self.dateSinceReturnWeb(),self.dateUntilReturnWeb()],[keyword])
                #dm.concatfile(self.dt)
            else:
                self.dt = DataManager.DataManager().startSearch([self.dateSinceReturnWeb(),self.dateUntilReturnWeb()],[keyword])
            #self.dateSet()    
            #tw.setdataframe(self.dt)
        #print(self.SearchBox_3.text())
        #(len(self.dt.index),twitter_scrap.Twitter_Scrap().keys)
        
        self.modelNew = scrapingGUI.TableModel(self.dt) 
        self.table2 = QtWidgets.QTableView()
        self.table2.setModel(self.modelNew)
        scrapingGUI.Ui_MainWindow().tableView_3.setModel(self.modelNew)

    def enterMassage(self) :
        enterM = self.textBrowser.text()
        DataManager.DataManager.startSearch([self.qDateBegin, self.qDateEnd],[enterM])
        
    def dateSet(self) :
        since = datetime.now().date()
        date = (datetime.strptime(str(since),'%Y-%m-%d'))
        self.dateEdit.setDate(date) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit.dateChanged.connect(self.dateSinceReturn) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

        until = datetime.now().date()
        date2 = (datetime.strptime(str(until),'%Y-%m-%d'))
        self.dateEdit_2.setDate(date2) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_2.dateChanged.connect(self.dateUntilReturn)

    def dateSinceReturn(self) :
        self.qDateBegin = self.dateEdit.date().toPyDate() #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getSince)
        return self.qDateBegin

    def dateUntilReturn(self) :
        self.qDateEnd = self.dateEdit_2.date().toPyDate() #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getUntil)
        return self.qDateEnd

    '''def printDateInfo(self, qDate):
        calendarDate = '{0}-{1}-{2}'.format(qDate.day(),qDate.month(),qDate.year())
        print(calendarDate)
        return self.qDate'''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(536, 177)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.textBrowser = QtWidgets.QLineEdit(self.centralwidget)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setAcceptDrops(True)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 1, 1, 4)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 1, 4, 1, 1)
        self.dateEdit_2 = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.gridLayout.addWidget(self.dateEdit_2, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 3, 1, 1)
        self.pushButton.clicked.connect(self.enterMassage) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 4, 1, 1)
        self.pushButton_2.clicked.connect(self.dateSinceReturn) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

        self.dateSet()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 536, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Keyword"))
        self.label.setText(_translate("MainWindow", "Choose date want to search"))
        self.label_2.setText(_translate("MainWindow", "to"))
        self.pushButton.setText(_translate("MainWindow", "OK"))
        self.pushButton_2.setText(_translate("MainWindow", "Cancel"))


