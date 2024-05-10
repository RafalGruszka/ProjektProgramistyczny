import requests
import matplotlib.pyplot as plt
from datetime import datetime
import json

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


def plot_hourly_weather(data):
    if data:
        hourly_temperatures = [hour['Temperature']['Value'] for hour in data]
        hours_list = [hour['DateTime'] for hour in data]
        hours_object = [datetime.fromisoformat(hour) for hour in hours_list]
        hours = [hour.strftime("%H:%M") for hour in hours_object]

        plt.plot(hours, hourly_temperatures, marker='o', linestyle='-')
        plt.xlabel('Time (Hour)')
        plt.ylabel('Temperature (°C)')
        plt.title('Hourly Temperature Forecast')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("No weather data available.")


def create_plot(latitude: str, longitude: str):
    weather_data = get_hourly_weather(latitude, longitude)
    plot_hourly_weather(weather_data)
