"""Flask application"""
from flask import Flask, abort, render_template, request
import sqlite3
from datetime import date, timedelta
import location

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main_homepage() -> str:
    """Loads main landing page"""
    return render_template('main.html')


@app.route('/map', methods=['GET'])
def get_map() -> list:
    """Returns map centered at specified location"""
    beaches = {"Long Beach": [46.3523, -124.0543],
               "Twin Harbors": [46.8545, -124.1085],
               "Copalis Beach": [47.1126, -124.1738],
               "Mocrocks Beach": [47.2390, -124.2176],
               "Kalaloch": [47.6057, -124.3710]}

    # Gets date from front end in format "yyyy-mm-dd"
    entry = request.args.get('date')

    # Checks if date is within one week of today
    today = date.today()
    search = date(int(entry[0:4]), int(entry[5:7]), int(entry[8:]))

    if today <= search < today + timedelta(days=7):
        # In future, pull available locations from razor clam website based on the date
        locations_rough = ["Long Beach", "Twin Harbors"]
        locations = []

        for place in locations_rough:
            active_location = location.Location(place, beaches[place][0], beaches[place][1])
            active_location.get_tides(entry)
            locations.append(active_location.__dict__)

        print(locations)
        return locations
    else:
        return []


@app.errorhandler(404)
def page_not_found(error) -> tuple:
    """Handles errors"""
    return "The page cannot be found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
