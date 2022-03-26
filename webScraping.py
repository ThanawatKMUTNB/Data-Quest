from datetime import date
import os
from textwrap import wrap
from turtle import ht
from bs4 import BeautifulSoup
import requests
from soupsieve import escape
import re
import pandas as pd
from urllib.parse import urlparse
import json

# from testCookie import write, writeJson
class webScraping():
    def __init__(self):
        self.web = ["https://www.animenewsnetwork.com/","https://www.cbr.com/category/anime-news/",
                    "https://myanimelist.net/","https://otakumode.com/news/anime",
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
        
        # self.web = ["https://www.animenewsnetwork.com/","https://www.cbr.com/",
        #             "https://myanimelist.net/","https://otakumode.com/"
        #             ]
        
        # self.web = ["https://www.animenewsnetwork.com/"]    
        self.SaveFileName = 'WebScrapingData24.csv'
        self.soupList = []
        self.dfdict = {"Page Title": [] ,"Page Date":[],"Page Data":[],"Page Image":[],"Page Link":[]}
        self.df = pd.DataFrame.from_dict(self.dfdict)
        self.MainDomain = ""
        self.currentLink = ""
        self.subLink = []

    def setCurLink(self,Link):
        self.currentLink = Link
    
    def getCurLink(self):
        return self.currentLink
        
    def getPath(self):
        path = "WebData"
        # path = "C:\\Users\\tongu\\Desktop\\Web-Scraping\\WebScraping\\Web-Scraping\\WebData"
        fileJsonName = "_WebJsonData.json"
        path = os.path.join(path,(str(self.getTodayDate())+fileJsonName))
        print(path)
        return path
    
    def setMainDomain(self,link):
        domain = urlparse(link).netloc
        self.MainDomain = "https://" + str(domain)
        # print(domain)
    
    def getMainDomain(self):
        return self.MainDomain
    
    def getStatus(self,link):
        req = requests.get(link)
        if req.status_code == 200:
            return True
        else:
            return False
        
    # def setSubLink(self,soup):
    #     href = [self.currentLink]
    #     # print(type(soup))   
    #     for link in soup.find_all('a', href=True):
    #         if urlparse(link['href']).netloc == self.MainDomain:
    #             href.append(link['href'])
    #         if urlparse(link['href']).netloc == "":
    #             # if self.getStatus(self.MainDomain + link['href']):
    #             href.append(self.MainDomain + link['href'])
    #     # print("Href Type : ",type(href[0]))
    #     self.subLink = list(set(href))
        
    # def getSubLink(self):
    #     # print(self.subLink)
    #     return sorted(self.subLink)
    
    def getLang(self,soup):
        for link in soup.find_all('html', lang=True):
            # print(link['lang'])
            return link['lang']
        return "Don't Set"
    
    # def getData(self,soup):
    #     # divSoup = soup.find_all('div')
    #     textData = [""]
    #     for i in soup:
    #         if type(i) != None:
    #             textData =  textData + re.split("\s", i.text.strip())
    #     textData = [i for i in textData if i != ""]
    #     textData = [str(i) for i in textData]
    #     textData = " ".join(textData)
    #     return textData
    #     # print(len(divSoup),type(divSoup))
    
    def getTodayDate(self):
        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        return d1
    
    # def setTodayData(self):
    #     for i in self.web:
    #         soup = self.makeSoup(i)
    #         if soup != None:
    #             print("\n\n",i)
    #             self.dfdict["Page Title"] = self.getTitle(soup)
    #             self.dfdict["Page Date"] = self.getTodayDate()
    #             self.dfdict["Page Data"] = self.getData(soup)
    #             self.dfdict["Page Image"] = "photo"
    #             self.dfdict["Page Link"] = str(i)
    #             # print(self.dfdict)
    #             self.df = self.df.append(self.dfdict, ignore_index = True)
    #         else:
    #             print("\n\n---------None Soup -----------",i)
    
    # def getTitle(self,soup):
    #     # for t in self.soupList:
    #     if soup != None:
    #         for i in soup.find_all('title'):            
    #             return i.text.strip()
    #     else:
    #         return "None Title"
    
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
        
    # def creatDataframe(self):
    #     self.setTodayData()
    #     self.writeCSV()
        
    # def writeCSV(self):
    #     file = open(self.SaveFileName, encoding="utf8")
    #     try:
    #         numline = len(file.readlines())
    #     except print(file.readlines()):
    #         pass
    #     # print(numline)
    #     if numline != 0:
    #         # print("Read not 0")
    #         oldDf = pd.read_csv(self.SaveFileName,index_col=0)
    #         # print(oldDf)
    #         self.df = pd.concat([oldDf,self.df], ignore_index=True)
    #         # print(self.df.columns.to_list())
    #         self.df = self.df.drop_duplicates(subset=self.df.columns.to_list())
    #         # print("\n",self.df)
    #         self.df.to_csv(self.SaveFileName)
    #     if numline == 0:
    #         # print("Write 0 ")
    #         # print(self.df.columns.to_list())
    #         # print(self.df)
    #         self.df.to_csv(self.SaveFileName)
    #     file.close()

    def search(self,word):
        file = open(self.SaveFileName, encoding="utf8")
        # print(type(file))
        if len(file.readlines()) != 0:
            # print("Read not 0")
            print("Search : ",word)
            oldDf = pd.read_csv(self.SaveFileName,index_col=0)
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
    
    def getDomain(self,link):
        domain = urlparse(link).netloc
        return str(domain)
        
    def getFullLink(self,href):
        if urlparse(href).netloc == self.MainDomain:
            return str(href)
        elif urlparse(href).netloc == "":
            # if self.getStatus(self.MainDomain + link['href']):
            return self.MainDomain + str(href)
        else:
            return ""
    
    def getSubLink(self,Alink):
        FullLink = {}
        for ListAlink in Alink:
            FullLink[self.getFullLink(ListAlink['href'])] = ""
        return FullLink
            # dictForJson.update({FullLink:""})
            # print(ListAlink['href'])
            
    def getDataBySoup(self,link):
        dictForJson = {link : []}
        soup = self.makeSoup(link)
        self.MainDomain = self.getDomain(link)
        content = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6",'p'])
        print(len(content))
        n = 1
        for tag in content:
            # tag = 
            # print("\n"+tag.name+ ' ' + tag.text.strip())
            wrapTag = tag.previous_element.previous_element
            # print(wrapTag.text.strip())
            # print(wrapTag)
            if tag.name == "p":
                print("\n"+tag.name+ ' ' + tag.text.strip())
                # print("---",wrapTag.text.strip())
                Alink = tag.find_all('a', href = True)
                if Alink != []:
                    subLink = self.getSubLink(Alink)
                    dictForJson.update(subLink)
                # dictForJson[link] += [str(n)+' ' + tag.text.strip()]
                n+=1
            else: #"h1", "h2", "h3", "h4", "h5", "h6"
                Alink = tag.find_all('a', href = True)
                if Alink != []:
                    subLink = self.getSubLink(Alink)
                    dictForJson.update(subLink)
                dictForJson[link] += [[tag.name+ ' ' + tag.text.strip(),wrapTag.text.strip().replace(tag.text.strip(),"").replace("\n"," ")]]
        
        return dictForJson
    
    def writeJson(self,dictForWrite):
            #Over write
        with open(self.getPath(),"w") as f:
            json.dump(dictForWrite,f)
        f.close()
        
    def readJson(self):
        with open(self.getPath(),encoding = "utf-8") as f:
            data = json.load(f)
        # print(data)
        f.close()
        # data = json.dumps(data, indent=4)
        return data
    
    def startScraping(self):
        dictForJson = {}
        dictForJson[self.getTodayDate()] = {}
        for link in self.web[:2]:
            # soup = ex.makeSoup(link)
            dictForJson[self.getTodayDate()].update({link : self.getDataBySoup(link)})
        print(json.dumps(dictForJson, indent=4, sort_keys=True))
        self.writeJson(dictForJson)
        # print(dictForJson)
ex = webScraping()
# link = 'https://www.animenewsnetwork.com/news/2022-03-22/crunchyroll-announces-release-schedule-for-spring-2022-anime-season/.183884'
ex.startScraping()
    
# ex.creatDataframe()
# ex.search("anime")