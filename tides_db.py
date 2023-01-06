"""
Creates tides table with information on tides from any razor clam beach
"""

import sqlite3
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import datetime


def create_table() -> None:
    """Clears original tide table and creates new empty one"""
    con = sqlite3.connect("clam.db")
    cursor = con.cursor()

    # Clears old table
    res = cursor.execute("SELECT name FROM sqlite_master")
    for table in res.fetchall():
        if table == ("tides",):
            cursor.execute("DROP TABLE tides")
            con.commit()

    # Creates new table called tides: https://docs.python.org/3/library/sqlite3.html
    cursor.execute("CREATE TABLE tides(location, day, time1, tide1, time2, tide2, time3, tide3, time4, tide4)")
    con.commit()
    con.close()


def get_tides(date: str, location: str) -> list:
    """Creates entry in tide table from web data"""
    beaches = {"Copalis Beach": "https://tides.willyweather.com/wa/grays-harbor-county/copalis-beach.html",
               "Mocrocks Beach": "https://tides.willyweather.com/wa/grays-harbor-county/moclips.html",
               "Kalaloch": "https://tides.willyweather.com/wa/jefferson-county/kalaloch.html",
               "Twin Harbors": "https://tides.willyweather.com/wa/grays-harbor-county/twin-harbors-beach.html",
               "Long Beach": "https://tides.willyweather.com/wa/pacific-county/long-beach.html"}

    con = sqlite3.connect("clam.db")
    cursor = con.cursor()

    # Pull values from web: https://realpython.com/python-web-scraping-practical-introduction/
    req = Request(
        url=beaches[location],
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    days = soup.find_all("li", class_="day")

    for day in days:
        # If the date is correct, adds tide information to table
        if day.time["datetime"] == date:
            times = day.find_all("h3")
            tides = day.find_all("span")
            entry = [location, date]

            for index in range(0, 4):
                if index < len(times):
                    in_time = datetime.strptime(times[index].contents[0], "%I:%M %p")
                    entry.append(datetime.strftime(in_time, "%H:%M"))
                    entry.append(tides[index].contents[0])
                else:
                    entry.append("N/A")
                    entry.append("N/A")

            cursor.execute(
                """INSERT INTO tides(location, day, time1, tide1, time2, tide2, time3, tide3, time4, tide4) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", entry
            )
            con.commit()
            break

    query = 'SELECT time1, tide1, time2, tide2, time3, tide3, time4, tide4 FROM tides WHERE location = "' + location + '"'
    output = cursor.execute(query).fetchall()[0]
    con.close()

    return output
