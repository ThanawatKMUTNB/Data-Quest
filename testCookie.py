from cgitb import html
from datetime import date, timedelta
import json
import re
from urllib.parse import urlparse
import webScraping as web

def writePaintext():
    s = ex.makeSoup("https://www.animenewsnetwork.com/")
    # file = open("MyFileText.txt","w")
    file = open("MyFile.txt","w")
    titleT = s.find('title')
    file.writelines(titleT.text.strip()+"\n")

    # s = s.text.strip()
    # s = list(s)
    n = 1
    for i in s:
        try:
            t = str(n)+" "+str(i.text.strip())+"\n"
            file.writelines(t)
            n+=1
        except :
            pass
        
    file.close()

def write():
    s = ex.makeSoup("https://www.animenewsnetwork.com/")
    # file = open("MyFileText.txt","w")
    file = open("MyFile.txt","w")
    titleT = s.find('title')
    file.writelines(titleT.text.strip()+"\n")

    # s = s.text.strip()
    # s = list(s)
    s = s.prettify()
    # print(s)
    try:
        file.writelines(s)
    except :
        pass
        
    file.close()
    
def wp(source):
    print(source)
    print(type(source))
    
    file = open("MyFileCon.txt","w")
    # file.writelines(source)
    
    for i in source:
        # print(type(i))
        try:
            file.writelines(i)
        except print("ERROR"):
            file.writelines(source)
            pass
    file.close()

def writeJson(dictForWrite):
    #Over write
    with open("WebJsonData.json","w") as f:
        json.dump(dictForWrite,f)
    f.close()
    
def readJson():
    with open("WebJsonData.json") as f:
        data = json.load(f)
    # print(data)
    f.close()
    return data

def updateDict(dateKey,dictWithDate):
    for i in ex.web:
        soup = ex.makeSoup(i)
        ex.setMainDomain(i)
        # print("Main Domain : ",ex.getMainDomain())
        ex.setSubLink(soup)
        patt = {
                #MainLink
                str(i) : 
                    #SubLink
                    {}
                }
        for j in ex.subLink[:3]:
            subpatt = {str(j) : ""}
            patt[str(i)].update(subpatt)
        dictWithDate[dateKey].update(patt)
        # dictWithDate[dateKey][str(i)]["Sub 1"] = "LLL"
    return dictWithDate

ex = web.webScraping()
linkMain = "https://www.animenewsnetwork.com/"
s = ex.makeSoup(linkMain)

tm = timedelta(1)
yd = timedelta(-1)

# jsonDict = { str(date.today() + yd) : "4774",
#              str(date.today()) : "2",
#              str(date.today() + tm) : "3"}
jsonDict = {}
jsonDict[str(ex.getTodayDate())] = {}
print("\n\n ----------------- Start")
s = updateDict(str(ex.getTodayDate()),jsonDict)
# jsonDict = { str(ex.getTodayDate()) : 
#                     {
#                         #MainLink
#                         str(ex.getMainDomain(linkMain)) : 
#                             #SubLink
#                             {
#                                 "Sub 1" : "",
#                                 "Sub 2" : ""
#                                 },
#                         str(ex.getMainDomain(linkMain))+ " 2" : 
#                             #SubLink
#                             {
#                                 "Sub 1" : "",
#                                 "Sub 2" : ""
#                                 }
#                     } }

# writeJson(jsonDict)
# r = readJson()
print(s)
writeJson(s)