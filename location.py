import tides_db


class Location:
    name = ""
    latitude = 0
    longitude = 0
    date = ""
    tides = []
    times = []

    def __init__(self, name: str, latitude: float, longitude: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def get_tides(self, date: str):
        """Calls web scraper to populate tide information"""
        self.date = date
        tides_db.create_table()
        tides_rough = tides_db.get_tides(self.date, self.name)

        self.times = [tides_rough[0], tides_rough[2], tides_rough[4], tides_rough[6]]
        self.tides = [tides_rough[1], tides_rough[3], tides_rough[5], tides_rough[7]]
