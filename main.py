import pandas
import pandas as pd
import folium
import requests
import pprint
import csv

check = requests.get('https://opendata.vancouver.ca/api/datasets/1.0/electric-vehicle-charging-stations/')
rows = check.json()['metas']['records_count']

r = requests.get(f'https://opendata.vancouver.ca/api/records/1.0/search/?dataset=electric-vehicle-charging-stations&q=&rows={rows}')

content = r.json()
pprint.pprint(content)

charging_stations = {}

for station in content['records']:
    charging_stations[station['fields']['address']] = station['fields']['geom']['coordinates']


pprint.pprint(charging_stations)


map = folium.Map(
    zoom_start=11,
    location=[49.2827, -123.1207]
)


print(len(charging_stations))

for (sta, loc) in charging_stations.items():
    folium.Marker(
        location=(loc[1], loc[0]),
        popup=sta,
        icon=folium.Icon(color='blue', icon="map-pin", prefix='fa')
    ).add_to(map)

map.save('world_empty.html')

