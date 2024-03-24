import requests
import json

apiKey = 'qWGdR3whkDhGy9dmO2AtwahlROfWH0ip'
endpoint = 'https://dataservice.accuweather.com/locations/v1/'
offline = True  # True - offline, False - online
def weatherLocations(location: str)  -> [str]:

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

#print(weatherLocations('Jaworzno'))
