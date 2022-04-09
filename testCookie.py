from cgitb import html
from datetime import date, timedelta
from itertools import count
import json
import re
from urllib.parse import urlparse
import webScraping as web
import DataManager as data
from io import StringIO
import os
import ast
ex = web.webScraping()
dm = data.DataManager()
link = "https://www.animenewsnetwork.com/"
# path = "C:/Users/tongu/Desktop/Web SC 2/Web-Scraping/WebData"
# rawData = os.listdir(path)
ex.startScraping()

# # print(rawData[0].split("_"))

# for i in rawData:
#     today = i.split("_")[0]
    
#     newpath = os.path.join('web search',today) 
#     if not os.path.exists(newpath):
#         os.makedirs(newpath)
    
#     d = {}
#     for kw in ex.keyword:
#         dm.setDataForSearch(os.path.join(newpath,kw+".json"),d)
    
#     path = os.path.join("WebData",i)
#     dictForSearch = dm.readJson(path)
#     headDateName = list(dictForSearch.keys())[0]
    # print(headDateName)
    
    # for sublink in list(dictForSearch[headDateName].keys()):
    #     dataList = dictForSearch[headDateName][sublink]["Data"]
    #     for paragraph in dataList
    
    # dm.setDataForSearch(i.split("_")[0],d)

# print(dm.readCsvToDf("WebData\\"+rawData[0]))

# dm.startSearch(["02-04-2022","08-04-2022"],['Anime','Summer'])