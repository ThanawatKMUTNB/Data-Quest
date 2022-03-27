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
        self.SaveFileName = "_WebJsonData.json"
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
        fileJsonName = self.SaveFileName
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
    
    def getTitle(self,soup):
        # for t in self.soupList:
        if soup != None:
            for i in soup.find_all('title'):            
                return i.text.strip()
        else:
            return "None Title"
    
    def makeSoup(self,link):
        # for link in self.web:
        # print("makeSoup",link)
        try:
            req = requests.get(link)
            if req.status_code == 200:
                # print("in")
                req.encoding = "utf-8"
                soup = BeautifulSoup(req.text,"html.parser")
                self.soupList.append(soup)
                return soup
        except :
            print("makeSoup",link)
            print(req)
            pass
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
            return 'https://'+str(href)
        elif urlparse(href).netloc == "":
            # if self.getStatus(self.MainDomain + link['href']):
            return 'https://'+self.MainDomain + str(href)
        else:
            return ""
        
    def getDataList(self,soup):
        Data = []
        content = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6",'p'])
        # print(link,len(content))
        n=0
        for tag in content:
            wrapTag = tag.previous_element.previous_element
            if tag.name == "p":
                Data.append(["ParaGraph "+str(n) , tag.text.strip().replace("\n"," ")])
                n+=1
            else: #"h1", "h2", "h3", "h4", "h5", "h6"
                Data.append([tag.text.strip(),wrapTag.text.strip().replace(tag.text.strip(),"").replace("\n"," ")])
        return Data
        
    def getSubLink(self,tag):
        Alink = tag.find_all('a', href = True)
        wrapTag = tag.previous_element.previous_element
        dictForJson = {}
        for ListAlink in Alink:
            try:
                soup = self.makeSoup(self.getFullLink(ListAlink['href']))
                if self.getFullLink(ListAlink['href']) not in dictForJson.keys():
                    dictForJson.update({self.getFullLink(ListAlink['href']):{'Lang': self.getLang(soup),
                                                                        'Title' : self.getTitle(soup),
                                                                        'Ref' : 0,
                                                                        'Data' : self.getDataList(soup)
                                                                        }})
                else:
                    # print("Dub")
                    dictForJson[self.getFullLink(ListAlink['href'])]['Ref'] += 1
            except :
                pass
        return dictForJson
    
    def getDataByLink(self,link):
        soup = self.makeSoup(link)
        dictForJson = {}
        self.MainDomain = self.getDomain(link)
        content = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6",'p'])
        countN = len(content)
        for tag in content:
            print(countN," ",tag)
            countN -= 1
            if tag.name == "p":
                Alink = tag.find_all('a', href = True)
                if Alink != []:
                    subLink = self.getSubLink(tag)
                    
                    for ssl in list(subLink.keys()):
                        if ssl in list(dictForJson.keys()):
                            dictForJson[ssl]["Ref"] += 1
                            del subLink[ssl]
                    
                    dictForJson.update(subLink)
            else: #"h1", "h2", "h3", "h4", "h5", "h6"
                Alink = tag.find_all('a', href = True)
                if Alink != []:
                    subLink = self.getSubLink(tag)
                    for ssl in list(subLink.keys()):
                        if ssl in list(dictForJson.keys()):
                            dictForJson[ssl]["Ref"] += 1
                            del subLink[ssl]
                    dictForJson.update(subLink)
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
        
        countWeb = len(self.web)
        for link in self.web[:-1]:
            dictForJson = {}
            dictForJson[self.getTodayDate()] = {}
            self.SaveFileName = "_"+str(countWeb)+"_WebJsonData.json"
            countWeb -= 1
            soup = self.makeSoup(link)
            dictForJson[self.getTodayDate()].update({ link : {'Lang': self.getLang(soup),
                                                'Title' : self.getTitle(soup),
                                                'Data' : self.getDataList(soup)
                                                }
                                                })
            print("-----Main Link",link)
            # soup = ex.makeSoup(link)
            self.writeJson(dictForJson)
            dictForJson[self.getTodayDate()].update({link : self.getDataByLink(link)})
            self.writeJson(dictForJson)
            for ssl in list(dictForJson[self.getTodayDate()][link].keys())[1:]:
                self.writeJson(dictForJson)
                print("Current Size : ",len(dictForJson[self.getTodayDate()][link]))
                dictSsl = self.getDataByLink(ssl)
                for sslLink in list(dictSsl.keys()):
                    if sslLink in list(dictForJson[self.getTodayDate()][link].keys()):
                        dictForJson[self.getTodayDate()][link][sslLink]["Ref"] += 1
                        del dictSsl[sslLink]
                dictForJson[self.getTodayDate()][link].update(dictSsl)
        # print("Current Size : ",len(dictForJson[self.getTodayDate()][link]))
        # dictForJson[self.getTodayDate()].update({link : self.getDataByLink(ssl)})
        # print(json.dumps(self.getDataByLink(ssl), indent=4, sort_keys=True))
        # print(json.dumps(dictForJson, indent=4, sort_keys=True))
        self.writeJson(dictForJson)
        
ex = webScraping()
ex.startScraping()
# r = ex.readJson()
# print(r)
# ex.creatDataframe()
# ex.search("anime")