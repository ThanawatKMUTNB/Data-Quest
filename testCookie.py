from cgitb import html
from datetime import date, timedelta
import datetime
from itertools import count
import json
import re
from urllib.parse import urlparse
from datetime import date
from datetime import datetime
import pandas as pd
import webScraping as web
import DataManager as data
from io import StringIO
import os
import ast
from langdetect import detect
import scrapingGUI as scrap

# sc = scrap.Ui_MainWindow()
ex = web.webScraping()
dm = data.DataManager()

link = "https://www.animenewsnetwork.com/"
# path = "C:/Users/tongu/Desktop/Web SC 2/Web-Scraping/web search"
path = "C:/Users/tongu/Desktop/Web SC 2/Web-Scraping/WebData"
rawData = os.listdir(path)
today = ex.getTodayDate()
newpath = os.path.join('web search',today,"anime(1).csv")
              
dateList =  ['09-04-2022_10_WebJsonData.json', '09-04-2022_11_WebJsonData.json', 
              '09-04-2022_12_WebJsonData.json', '09-04-2022_13_WebJsonData.json',
              '09-04-2022_14_WebJsonData.json', '09-04-2022_15_WebJsonData.json', 
              '09-04-2022_16_WebJsonData.json', '09-04-2022_17_WebJsonData.json', 
              '09-04-2022_18_WebJsonData.json', '09-04-2022_19_WebJsonData.json', 
              '09-04-2022_1_WebJsonData.json', '09-04-2022_2_WebJsonData.json', 
              '09-04-2022_3_WebJsonData.json', '09-04-2022_4_WebJsonData.json', 
              '09-04-2022_5_WebJsonData.json', '09-04-2022_6_WebJsonData.json', 
              '09-04-2022_7_WebJsonData.json', '09-04-2022_8_WebJsonData.json', 
              '09-04-2022_9_WebJsonData.json'] 
            #   '09-04-2022_10_WebJsonData.json', '09-04-2022_11_WebJsonData.json', '09-04-2022_12_WebJsonData.json', '09-04-2022_13_WebJsonData.json', '09-04-2022_14_WebJsonData.json', '09-04-2022_15_WebJsonData.json', '09-04-2022_16_WebJsonData.json', '09-04-2022_17_WebJsonData.json', '09-04-2022_18_WebJsonData.json', '09-04-2022_19_WebJsonData.json', '09-04-2022_1_WebJsonData.json', '09-04-2022_2_WebJsonData.json', '09-04-2022_3_WebJsonData.json', '09-04-2022_4_WebJsonData.json', '09-04-2022_5_WebJsonData.json', '09-04-2022_6_WebJsonData.json', '09-04-2022_7_WebJsonData.json', '09-04-2022_8_WebJsonData.json', '09-04-2022_9_WebJsonData.json', '09-04-2022_10_WebJsonData.json', '09-04-2022_11_WebJsonData.json', '09-04-2022_12_WebJsonData.json', '09-04-2022_13_WebJsonData.json', '09-04-2022_14_WebJsonData.json', '09-04-2022_15_WebJsonData.json', '09-04-2022_16_WebJsonData.json', '09-04-2022_17_WebJsonData.json', '09-04-2022_18_WebJsonData.json', '09-04-2022_19_WebJsonData.json', '09-04-2022_1_WebJsonData.json', '09-04-2022_2_WebJsonData.json', '09-04-2022_3_WebJsonData.json', '09-04-2022_4_WebJsonData.json', '09-04-2022_5_WebJsonData.json', '09-04-2022_6_WebJsonData.json', '09-04-2022_7_WebJsonData.json', '09-04-2022_8_WebJsonData.json', '09-04-2022_9_WebJsonData.json', '09-04-2022_10_WebJsonData.json', '09-04-2022_11_WebJsonData.json', '09-04-2022_12_WebJsonData.json', '09-04-2022_13_WebJsonData.json', '09-04-2022_14_WebJsonData.json', '09-04-2022_15_WebJsonData.json', '09-04-2022_16_WebJsonData.json', '09-04-2022_17_WebJsonData.json', 
            # '09-04-2022_18_WebJsonData.json', '09-04-2022_19_WebJsonData.json', '09-04-2022_1_WebJsonData.json', '09-04-2022_2_WebJsonData.json', '09-04-2022_3_WebJsonData.json', '09-04-2022_4_WebJsonData.json', '09-04-2022_5_WebJsonData.json', '09-04-2022_6_WebJsonData.json', 
            # '09-04-2022_7_WebJsonData.json', '09-04-2022_8_WebJsonData.json', '09-04-2022_9_WebJsonData.json', '09-04-2022_10_WebJsonData.json', 
            # '09-04-2022_11_WebJsonData.json', '09-04-2022_12_WebJsonData.json', '09-04-2022_13_WebJsonData.json', '09-04-2022_14_WebJsonData.json', '09-04-2022_15_WebJsonData.json', '09-04-2022_16_WebJsonData.json', '09-04-2022_17_WebJsonData.json', '09-04-2022_18_WebJsonData.json', '09-04-2022_19_WebJsonData.json', '09-04-2022_1_WebJsonData.json', '09-04-2022_2_WebJsonData.json', '09-04-2022_3_WebJsonData.json', '09-04-2022_4_WebJsonData.json', '09-04-2022_5_WebJsonData.json', '09-04-2022_6_WebJsonData.json', '09-04-2022_7_WebJsonData.json', '09-04-2022_8_WebJsonData.json', '09-04-2022_9_WebJsonData.json', '10-04-2022_10_WebJsonData.json', '10-04-2022_11_WebJsonData.json', '10-04-2022_12_WebJsonData.json', '10-04-2022_13_WebJsonData.json', '10-04-2022_14_WebJsonData.json', '10-04-2022_15_WebJsonData.json', '10-04-2022_16_WebJsonData.json', '10-04-2022_17_WebJsonData.json', '10-04-2022_18_WebJsonData.json', '10-04-2022_19_WebJsonData.json', '10-04-2022_1_WebJsonData.json', '10-04-2022_2_WebJsonData.json', '10-04-2022_3_WebJsonData.json', '10-04-2022_4_WebJsonData.json', '10-04-2022_5_WebJsonData.json', '10-04-2022_6_WebJsonData.json', '10-04-2022_7_WebJsonData.json', '10-04-2022_8_WebJsonData.json', '10-04-2022_9_WebJsonData.json', '11-04-2022_10_WebJsonData.json', '11-04-2022_11_WebJsonData.json', '11-04-2022_12_WebJsonData.json', '11-04-2022_13_WebJsonData.json', '11-04-2022_14_WebJsonData.json', '11-04-2022_15_WebJsonData.json', '11-04-2022_16_WebJsonData.json', '11-04-2022_17_WebJsonData.json', '11-04-2022_18_WebJsonData.json', '11-04-2022_19_WebJsonData.json', '11-04-2022_1_WebJsonData.json', '11-04-2022_2_WebJsonData.json', '11-04-2022_3_WebJsonData.json', '11-04-2022_4_WebJsonData.json', '11-04-2022_5_WebJsonData.json', '11-04-2022_6_WebJsonData.json', '11-04-2022_7_WebJsonData.json', '11-04-2022_8_WebJsonData.json', '11-04-2022_9_WebJsonData.json', '12-04-2022_10_WebJsonData.json', '12-04-2022_11_WebJsonData.json', '12-04-2022_12_WebJsonData.json', '12-04-2022_13_WebJsonData.json', '12-04-2022_14_WebJsonData.json', '12-04-2022_15_WebJsonData.json', '12-04-2022_16_WebJsonData.json', '12-04-2022_17_WebJsonData.json', '12-04-2022_18_WebJsonData.json', '12-04-2022_19_WebJsonData.json', '12-04-2022_1_WebJsonData.json', '12-04-2022_2_WebJsonData.json', '12-04-2022_3_WebJsonData.json', '12-04-2022_4_WebJsonData.json', '12-04-2022_5_WebJsonData.json', '12-04-2022_6_WebJsonData.json', '12-04-2022_7_WebJsonData.json', '12-04-2022_8_WebJsonData.json', '12-04-2022_9_WebJsonData.json', '13-04-2022_10_WebJsonData.json', '13-04-2022_11_WebJsonData.json', '13-04-2022_12_WebJsonData.json', '13-04-2022_13_WebJsonData.json', '13-04-2022_14_WebJsonData.json', '13-04-2022_15_WebJsonData.json', '13-04-2022_16_WebJsonData.json', '13-04-2022_17_WebJsonData.json', '13-04-2022_18_WebJsonData.json', '13-04-2022_19_WebJsonData.json', '13-04-2022_1_WebJsonData.json', '13-04-2022_2_WebJsonData.json', '13-04-2022_3_WebJsonData.json', '13-04-2022_4_WebJsonData.json', '13-04-2022_5_WebJsonData.json', '13-04-2022_6_WebJsonData.json', '13-04-2022_7_WebJsonData.json', '13-04-2022_8_WebJsonData.json', '13-04-2022_9_WebJsonData.json', '14-04-2022_10_WebJsonData.json', '14-04-2022_11_WebJsonData.json', '14-04-2022_12_WebJsonData.json', '14-04-2022_13_WebJsonData.json', '14-04-2022_14_WebJsonData.json', '14-04-2022_15_WebJsonData.json', '14-04-2022_16_WebJsonData.json', '14-04-2022_17_WebJsonData.json', '14-04-2022_18_WebJsonData.json', '14-04-2022_19_WebJsonData.json', '14-04-2022_1_WebJsonData.json', '14-04-2022_2_WebJsonData.json', '14-04-2022_3_WebJsonData.json', '14-04-2022_4_WebJsonData.json', '14-04-2022_5_WebJsonData.json', '14-04-2022_6_WebJsonData.json', '14-04-2022_7_WebJsonData.json', '14-04-2022_8_WebJsonData.json', '14-04-2022_9_WebJsonData.json']

# now = datetime.now()
# starttime = now.strftime("%H:%M:%S")

ex.startScraping()

# for i in dateList:
#     dm.setDataByAllKeyword(i)
# now = datetime.now()
# Endtime = now.strftime("%H:%M:%S")
# print(starttime,Endtime)

# print(dm.startSearch(["16-04-2022","17-04-2022"],['anime','animation']))

#['kk'] [datetime.date(2022, 3, 17), datetime.date(2022, 4, 19)]