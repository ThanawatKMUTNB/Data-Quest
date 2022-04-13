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
# path = "C:/Users/tongu/Desktop/Web SC 2/Web-Scraping/web search"
path = "C:/Users/tongu/Desktop/Web SC 2/Web-Scraping/WebData"
rawData = os.listdir(path)
today = ex.getTodayDate()
newpath = os.path.join('web search',today)

# dm.setDataByKeyword()

ex.startScraping()
# print(dm.readCsvToDf(os.path.join("web search","08-04-2022","animation.csv")))
# ud = ['o','k','l']
# dm.writeCsvByList(os.path.join("web search","08-04-2022","animation.csv"),ud)
# print(dm.readCsvToDf(os.path.join("web search","08-04-2022","animation.csv")))

# dm.startSearch(["02-04-2022","08-04-2022"],['Anime','Summer'])