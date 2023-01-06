"""
Creates clamming_tides table with information on razor clams from
https://wdfw.wa.gov/fishing/shellfishing-regulations/razor-clams#current
"""

import re
import sqlite3
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

con = sqlite3.connect("clam.db")
cursor = con.cursor()

# Clears old table
res = cursor.execute("SELECT name FROM sqlite_master")
for table in res.fetchall():
    if table == ("clamming_tides",):
        cursor.execute("DROP TABLE clamming_tides")
        con.commit()

# Creates a table called clamming_tides: https://docs.python.org/3/library/sqlite3.html
cursor.execute("CREATE TABLE clamming_tides(day, time, height, location1, location2, location3)")

# Pull values from web: https://realpython.com/python-web-scraping-practical-introduction/
req = Request(
    url="https://wdfw.wa.gov/fishing/shellfishing-regulations/razor-clams#current",
    headers={'User-Agent': 'Mozilla/5.0'}
)

page = urlopen(req)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
dates = soup.find_all("div", class_="timeline-item-body")[0].find_all("ul")

if dates != []:
    dates = dates[0].find_all("li")

for day in dates:
    info = day.contents[0].split(',')
    date = info[0].replace('.', '')
    time = info[2].split(';')[0][1:].replace('.', '')
    height = info[2].split(';')[1][1:].replace(' feet', '')
    location1 = info[2].split(';')[2][1:]
    location2 = info[3][1:]
    location3 = info[4][1:]
    location3 = re.sub(' [(].*[)]', '', location3)

    data = [date, time, height, location1, location2, location3]
    print(data)
    cursor.execute(
        """INSERT INTO clamming_tides(day, time, height, location1, location2, location3) 
        VALUES (?, ?, ?, ?, ?, ?)""", data
    )
    con.commit()

con.close()
