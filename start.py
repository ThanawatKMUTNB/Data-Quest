from turtle import ht
from bs4 import BeautifulSoup
import requests
import csv
from IPython.display import HTML
from soupsieve import escape
# print('kiki')

url = "https://myanimelist.net/topanime.php"
req = requests.get(url)

# print(req)

req.encoding = "utf-8"

soup = BeautifulSoup(req.text,"html.parser")

# print(soup.prettify())

# want = soup.find_all('a',limit = 3)

# want = soup.find('table')

# print(want)
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