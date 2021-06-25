import folium
import requests


check = requests.get('https://opendata.vancouver.ca/api/datasets/1.0/electric-vehicle-charging-stations/')
rows = check.json()['metas']['records_count']

r = requests.get(f'https://opendata.vancouver.ca/api/records/1.0/search/?dataset=electric-vehicle-charging-stations&q=&rows={rows}')

content = r.json()

charging_stations = {
    'addresses': [],
    'coordinates': []
}

for station in content['records']:
    charging_stations['operators'].append(station['fields']['lot_operator'])
    charging_stations['addresses'].append(station['fields']['address'])
    charging_stations['coordinates'].append(station['fields']['geom']['coordinates'])


map = folium.Map(
    zoom_start=11,
    location=[49.2827, -123.1207]
)


for i in range(len(charging_stations['addresses'])):
    longitude, latitude = charging_stations['coordinates'].pop(0)
    info = '<b>' + charging_stations['operators'].pop(0) + '</b>' 
    + '</br>' + charging_stations['addresses'].pop(0)
    folium.Marker(
        location=(latitude, longitude),
        popup=info,
        icon=folium.Icon(color='blue', icon="map-pin", prefix='fa')
    ).add_to(map)

map.save('index.html')

