import requests
import matplotlib.pyplot as plt
from datetime import datetime
import json
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

apiKey = 'qWGdR3whkDhGy9dmO2AtwahlROfWH0ip'
endpoint = 'https://dataservice.accuweather.com/locations/v1/'
offline = True  # True - offline, False - online
def weatherLocations(location: str) -> [str]:

# Http request

    locations = []
    if offline:
        locations.append(['1', 'Jaworzno, miasto woj. śląskie, Polska'])
        locations.append(['2', 'Jaworzno, miasto woj. opolskie, Polska'])
        return locations
    else:
        url = endpoint + '/search?apikey=' + apiKey + '&q=' + location + '&language=pl-pl&details=false&offset=20'
        print(url)
        response = requests.get(url)
        json_data = json.loads(response.text)

    for location in json_data:
        locations.append([location['Key'], location['LocalizedName'] + ', ' + location['AdministrativeArea']['LocalizedType'] + ' ' + location['AdministrativeArea']['LocalizedName'] + ', ' + location['Country']['LocalizedName']])

    return locations

def get_hourly_weather(latitude, longitude):
    api_key = "qWGdR3whkDhGy9dmO2AtwahlROfWH0ip"
    url = f"https://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_key}&q={latitude},{longitude}"
    response = requests.get(url)
    location_data = response.json()
    location_key = location_data['Key']

    url_weather = f"https://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}?apikey={api_key}&metric=true"
    response_weather = requests.get(url_weather)
    weather_data = response_weather.json()
    print(weather_data)
    return weather_data


