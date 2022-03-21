from ast import Try
from datetime import date
from email import header
from turtle import ht
from typing import Pattern
from bs4 import BeautifulSoup
import requests
import csv
from IPython.display import HTML
from soupsieve import escape
import re
import pandas as pd
class webScraping():
    def __init__(self):
        self.web = ["https://www.animenewsnetwork.com/","https://www.cbr.com/category/anime-news/",
                    "https://myanimelist.net/anime.php#","https://otakumode.com/news/anime",
                    "https://news.dexclub.com/","https://my-best.in.th/49872",
                    "https://www.anime-japan.jp/2021/en/news/","https://the-japan-news.com/news/manga&anime/",
                    "https://anime-news.tokyo/","https://manga.tokyo/news/",
                    "https://www.bbc.com/news/topics/c1715pzrj24t/anime","https://www.independent.co.uk/topic/anime",
                    "https://soranews24.com/tag/anime/","https://anitrendz.net/news/",
                    "https://thebestjapan.com/the-best-of-japan/anime-fans/","https://wiki.anime-os.com/chart/all-2020/",
                    "https://kwaamsuk.net/10-anime-netflix/","https://www.online-station.net/anime/326294/",
                    "https://th.kokorojapanstore.com/blogs/blogs/35-best-anime-of-all-time-new-and-old-in-2021",
                    "https://www.metalbridges.com/cool-anime-songs/"
                    ]    
        self.soupList = []
        self.dfdict = {"Page Title": [] ,"Page Date":[],"Page Data":[],"Page Image":[],"Page Link":[]}
        self.df = pd.DataFrame.from_dict(self.dfdict)
    
    
    def getData(self,soup):
        # divSoup = soup.find_all('div')
        textData = [""]
        for i in soup:
            if type(i) != None:
                textData =  textData + re.split("\s", i.text.strip())
        textData = [i for i in textData if i != ""]
        textData = [str(i) for i in textData]
        textData = " ".join(textData)
        return textData
        # print(len(divSoup),type(divSoup))
        
    def setTodayData(self):
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        for i in self.web:
            soup = self.makeSoup(i)
            if soup != None:
                print("\n\n",i)
                self.dfdict["Page Title"] = self.getTitle(soup)
                self.dfdict["Page Date"] = d1
                self.dfdict["Page Data"] = self.getData(soup)
                self.dfdict["Page Image"] = "photo"
                self.dfdict["Page Link"] = str(i)
                # print(self.dfdict)
                self.df = self.df.append(self.dfdict, ignore_index = True)
            else:
                print("\n\n---------None Soup -----------",i)
    def getTitle(self,soup):
        title = []
        # for t in self.soupList:
        if soup != None:
            for i in soup.find_all('title'):            
                title.append(i.text.strip())
                return i.text.strip()
    
    def makeSoup(self,link):
        # for link in self.web:
        req = requests.get(link)
        if req.status_code == 200:
            # print("in")
            req.encoding = "utf-8"
            soup = BeautifulSoup(req.text,"html.parser")
            self.soupList.append(soup)
            return soup
        # print(self.soupList)
        # else: return None
        
    def creatDataframe(self):
        self.setTodayData()
        self.writeCSV()
        
    def writeCSV(self):
        file = open("WebScrapingData.csv", encoding="utf8")
        try:
            numline = len(file.readlines())
        except print(file.readlines()):
            pass
        # print(numline)
        if numline != 0:
            # print("Read not 0")
            oldDf = pd.read_csv('WebScrapingData.csv',index_col=0)
            # print(oldDf)
            self.df = pd.concat([oldDf,self.df], ignore_index=True)
            # print(self.df.columns.to_list())
            self.df = self.df.drop_duplicates(subset=self.df.columns.to_list())
            # print("\n",self.df)
            self.df.to_csv('WebScrapingData.csv')
        if numline == 0:
            # print("Write 0 ")
            # print(self.df.columns.to_list())
            # print(self.df)
            self.df.to_csv('WebScrapingData.csv')
        file.close()
        
    def writeText(data):
        file = open("MyFile.txt","w")
        # data = []
        file.writelines(data)
        file.close()
    # def writeCSV(df):
    #     https://www.animenewsnetwork.com/
    def scrapingDiv():
        want = soup.find_all('div')
        print(len(want))
        # want = list(want)
        # print(str(want[0])[:500])
        data = []
        today = date.today()

        # dd/mm/YY
        d1 = today.strftime("%d/%m/%Y")
        print(d1)
        n=0
        for i in want:
            # print("\n\n")
            # print(len(list(i.find_all('a'))))
            # print(list(i.find_all('a')))
            if len(list(i.find_all('a'))) != 0:
                k = i.find_all('a')
                for j in k:
                    x = re.split('href="',str(j))
                    x=x[-1]
                    x = re.split('">',x)
                    x=x[0]
                    data.append("\n\n"+x)
        # writeText(data)
        print(len(data))
            # n+=1
            # if n == 2:
            #     break
        # print(want.find('a'))
        # aWant = want.find_all('a')
        # print("\n",len(aWant))
        # print(aWant)
        # for i in aWant:
            # i = str(i)
        # print("\n",aWant[:10]['href'])
            # x = re.search("href=$",str(i))
            # print(x)
        # print(aWant.find_all('href'))
        
    def scrapingTable():
        data = []
        table = soup.find("table", attrs={ "class" : "top-ranking-table" })
        # table_body = table.find('tbody')
        # print(table)

        rows = table.find_all('tr')
        for row in rows:
            # print("\n\n",row)
            # print("\n\n",row.find_all('img'))
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            img = row.find_all('img')
            # print(cols)
            if len(img) == 0:
                cols.append("Image")
            if len(img) > 0:
                src = img[0]["data-src"]
                imghtml = f'<img src ="{src}"/>'
                # print(type(HTML(imghtml)))
                cols.append(src)
                # cols[-1] = HTML(cols[-1])
                # print("\n\n",img[0]["data-src"])
            data.append([ele for ele in cols if ele]) # Get rid of empty values
            
        # print(data)
        # print(type(data[-1]))

        with open('animeRankTable.csv', 'w') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerows(data)
        f.close()

    def search(self,word):
        file = open("WebScrapingData.csv", encoding="utf8")
        # print(type(file))
        if len(file.readlines()) != 0:
            # print("Read not 0")
            print("Search : ",word)
            oldDf = pd.read_csv('WebScrapingData.csv',index_col=0)
            searchDict = {"Word Count": [] ,"Page Title": [] ,"Page Date":[],"Page Link":[]}
            searchDf = pd.DataFrame.from_dict(searchDict)
            for i in range(len(oldDf)):
                text = oldDf.iloc[i]["Page Data"]
                wordCount = text.count(word.lower())+text.count(word.upper())
                searchDf = searchDf.append({"Word Count": wordCount ,"Page Title": oldDf.iloc[i]["Page Data"] 
                                            ,"Page Date":oldDf.iloc[i]["Page Date"],"Page Link":oldDf.iloc[i]["Page Link"]}
                                           ,ignore_index=True)
            sorted_df = searchDf.sort_values(by=['Word Count'], ascending=False)
            print(sorted_df)
            
        file.close()

ex = webScraping()
# ex.creatDataframe()
ex.search("anime")