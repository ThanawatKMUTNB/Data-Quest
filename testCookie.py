from cgitb import html
import re
from urllib.parse import urlparse
import webScraping as web
ex = web.webScraping()
s = ex.makeSoup("https://www.animenewsnetwork.com/")

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
# write()

# d = s.find('div',id="content").get_text()
d = re.split("\n", s.text.strip())
# d = re.split("\n",d)
d = [i for i in d if i != "" and i != '']
# wp(d)
# print(d)
ex.getMainDomain("https://www.animenewsnetwork.com/")
sl = ex.getSubLink(s)
print(sl)

# for link in s.find_all('html', lang=True):
#     print(link['lang'])

# wp(d)