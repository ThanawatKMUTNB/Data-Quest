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
    s = s.prettify()
    # print(s)
    try:
        file.writelines(s)
    except :
        pass
    file.close()
    
def writeJson(dictForWrite):
    #Over write
    with open(ex.getPath(),"w") as f:
        json.dump(dictForWrite,f)
    f.close()
    
def readJson():
    with open(ex.getPath(),encoding = "utf-8") as f:
        data = json.load(f)
    # print(data)
    f.close()
    # data = json.dumps(data, indent=4)
    return data


def updateDataWithClass(Link):
    subpatt = {str(Link) : ""}    
    try:
        subsoup = ex.makeSoup(Link)
        if subsoup != None :
            content = subsoup.find('div')
            classN = 1
            if content != None:
                classList = content.find_all('div',class_=True)
                # classList = content.find_all('div',id=True)
                print(str(classN) + " Class",len(classList))
                classN += 1
                n = 0
                subpatt[str(Link)] = {}
                for k in classList:
                    # tag = [t.name for t in k if t.name != None]
                    # print(tag,k['class'])
                    
                    if k.text != "" and len(k.text.strip()) != 0:
                        
                        # paragraph = k.text.strip()
                        
                        # paragraph = str(paragraph)
                        # paragraph = str(paragraph.strip()).replace("\n",' ')
                        
                        dictKey = [str(n+1)] + k['class']
                        dictKey = " ".join(dictKey)

                        subpatt[str(Link)].update({str(dictKey) : 'paragraph'})
                        n +=1
                return subpatt
            
    except print("********* Error   *********** ",Link):
        pass

def updateData(Link):
    subpatt = []  
    # print("Error----------------",type(Link),Link)  
    try:
        print(Link)
        subsoup = ex.makeSoup(Link)
        if subsoup != None :
            content = subsoup.find('div')
            if content != None:
                classList = content.find_all('div',class_=True)
                for k in classList:
                    # tag = [t.name for t in k if t.name != None]
                    # print(tag,k['class'])
                    if k.text != "" and len(k.text.strip()) != 0:
                        paragraph = k.text.strip()
                        paragraph = str(paragraph)
                        paragraph = str(paragraph.strip()).replace("\n",' ')
                        subpatt.append(paragraph)
                return list(set(subpatt))
    except :
        pass
        
            
def updateSubLink(patt,Link):
    i = Link
    soup = ex.makeSoup(i)
    ex.setMainDomain(i)

    ex.setSubLink(soup)
    subLink = ex.getSubLink()

    allLink = subLink 
    # for j in subLink:
    #     try:
    #         print("\nMain Domain : ",ex.getMainDomain())
    #         print("SubLink : ",j)
    #         ssoup = ex.makeSoup(j)
    #         ex.setSubLink(ssoup)
    #         subSubLink = ex.getSubLink()
    #         allLink += subSubLink
    #         allLink = list(set(allLink))
    #         print(len(allLink))
    #         # print(str(countN)+" "+str(len(allLink))+" subSubLink : ",j)
    #         # subpatt = { i : "ss" for i in subSubLink }
    #         # subpatt = updateData(j)
    #         # patt[str(i)].update(subpatt)
    #     except :
    #         pass
    subpatt = { ssl : updateData(ssl) for ssl in sorted(allLink[:5])}
    patt[str(i)].update(subpatt)
    return patt        

def updateDict(dictWithDate):
    for i in ex.web:
        patt = {
                #MainLink
                str(i) : 
                    #SubLink
                    {}
                }
        ex.setCurLink(i)
        patt = updateSubLink(patt,i)
        dictWithDate[str(ex.getTodayDate())].update(patt)
        writeJson(dictWithDate)
        # dictWithDate[dateKey][str(i)]["Sub 1"] = "LLL"
    return dictWithDate

def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value)
        else:
            yield (key, value)
            
ex = web.webScraping()
dm = data.DataManager()
link = "https://www.animenewsnetwork.com/"
# ex.setMainDomain(link)
# s = ex.makeSoup(link)

# path = dm.getPath('','try.csv')
# df = dm.readCsvToDf(path)

# print(df.head)
# print(type(df['Data'][0]))
# dataL = dm.strOfListToList(df['Data'][0])


# print(len(df))
# print(df.columns)

# searchDf = dm.search(df,['Anime',"Manga"])
# dm.writeCsvByDf("100searchTable.csv",searchDf)

# dm.convertToSearch(['Revisiting', 'G', 'no', 'Reconguista,', 'And', 'Looking', 'Back', 'On', "'Happy", "Tomino'", '', '', '', 'Nov', '26,', '22:00'])
# sl = ex.setSubLink(s)
# print(len(sl))

# for i in ex.web:
#     # i = ex.web[7]
#     ex.currentLink = i
#     soup = ex.makeSoup(i)
#     ex.setSubLink(soup)
#     sub = ex.getAllSubLink()
#     ref = ex.getAllRefLink()
#     print(len(sub),len(ref))
#     # print(i)
#     # print(dm.canFetch(i))

ex.startScraping()

#try