from bs4 import BeautifulSoup
import requests
import csv
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
    # print(row)
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty values
    
# print(data)

with open('animeRankTable.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(data)