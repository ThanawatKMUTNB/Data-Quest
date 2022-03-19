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
        self.web = ["https://www.animenewsnetwork.com/","https://www.cbr.com/category/anime-news/"]    
        self.soupList = []
        self.dfdict = {"Page Title": [] ,"Page Date":[],"Page Data":[],"Page Image":[],"Page Link":[]}
        self.df = pd.DataFrame.from_dict(self.dfdict)
    
    def getData(self,soup):
        divSoup = soup.find_all('div')
        textData = ''
        for i in soup:
            textData =  textData + i.text.strip() + "\n"
        return textData
        # print(len(divSoup),type(divSoup))
        
    def setData(self):
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        for i in self.web:
            soup = self.makeSoup(i)
            self.dfdict["Page Title"] = self.getTitle(soup)
            self.dfdict["Page Date"] = d1
            self.dfdict["Page Data"] = self.getData(soup)
            self.dfdict["Page Image"] = "photo"
            self.dfdict["Page Link"] = str(i)
            # print(self.dfdict)
            self.df = self.df.append(self.dfdict, ignore_index = True)
            
    def getTitle(self,soup):
        title = []
        # for t in self.soupList:
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
        self.setData()
        self.writeCSV()
        
    def writeCSV(self):
        file = open("WebScrapingData.csv")
        numline = len(file.readlines())
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

    
# url = "https://myanimelist.net/topanime.php"
# req = requests.get(url)

# # print(req)
# if req.status_code == 200:
#     print("Successful")
#     req.encoding = "utf-8"
#     soup = BeautifulSoup(req.text,"html.parser")
#     # print(soup.prettify())
#     # scrapingDiv()

ex = webScraping()
ex.creatDataframe()