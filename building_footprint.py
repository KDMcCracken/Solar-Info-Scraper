import json
import requests
import urllib
import configparser

from math import cos, asin, sqrt

config = configparser.ConfigParser()
config.read('config.ini')

def get_site_lat_lng(address):
    params = urllib.parse.urlencode({'address': address, 'key': config['KEYS']['MyKey']})
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?%s' % params)
    address_lat_lng = response.json()['results'][0]['geometry']['location']

    return address_lat_lng 


def distance(lat1, lng1, lat2, lng2):
    """
    Solution from https://stackoverflow.com/questions/41336756/find-the-closest-latitude-and-longitude
    """
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lng2 - lng1) * p)) / 2
    return 12742 * asin(sqrt(a))


def get_closest_building(buildings, address_lat_lng):
    """
    Find the closest building to the given address_lat_lng value.
    """
    closest_building = None
    min_distance = float('inf')

    for building in buildings:
        for coords in building['geometry']['coordinates'][0]:
            building_distance = distance(coords[1], coords[0], address_lat_lng['lat'], address_lat_lng['lng'])
            if building_distance < min_distance:
                closest_building = building
                min_distance = building_distance

    return closest_building


def get_url(building_info):
    coords = building_info['geometry']['coordinates'][0]
    urlBuilder = "https://www.calcmaps.com/map-area/?&points=%5B%5B"

    # Loop through each coordinate pair and append them to our URL
    for coordinates in coords:
        urlBuilder += str(coordinates[1]) + "%2C" + str(coordinates[0]) + "%5D%2C%5B"

    # Chop off some extra characters from the loop and replace with proper URL syntax
    urlBuilder = urlBuilder[:-6]
    urlBuilder += "%5D"

    return urlBuilder


def run(address, state):
    """
    Args:
        argv[1] - the data file containing building information for a state
        argv[2] - the address of the building we are profiling
    """
    buildings = None

    print('\nReading state file...')
    with open(state + ".geojson") as file:
        buildings = json.load(file)

    site_lat_lng = get_site_lat_lng(address)
    print('\nSite lat/lng = ', site_lat_lng)

    print('\nFinding closest building...')
    closest_building = get_closest_building(buildings['features'], site_lat_lng)
    print('\nClosest building coords = ', closest_building)

    return get_url(closest_building)
