from ast import keyword
from xml.etree.ElementTree import tostring
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
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

class scrapingManager :
    def addPathList(self,path) :
        if len(path) != 0 :
            self.textLabel = self.path
            return self.textLabel
        else :
            self.textLabel = "None"
            return self.textLabel
    def OpenFile(self):
        #try:
        path = QFileDialog.getOpenFileName(None, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
        #QFileDialog.getSaveFileName(None, 'Dialog Title', home, file_filter)
        print(path)
        self.path = path
        self.readFile(path)
        return self.path

    def readFile(self,path):
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

    def addFile(self):
        self.label2.setText(self.path)

    