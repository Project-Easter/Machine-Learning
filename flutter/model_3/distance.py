"""
This module is used for calculating the latitude and longitude at a particular distance in which the the rows have to taken for recommending.
"""

import math

R = 6378.1 # Radius of the earth
bearings = [0,math.pi/2, math.pi, 1.5*math.pi] # Bearing is 90 degrees converted in radians

def get_coordinates(lat=None, lon=None, distance=None):
    """
    This function returns set of coordinates at the particular distances on angles 0, 90, 180 and 270 degrees.

    Parameters
    ----------
    lat, lon : coordinates of current location
    distance : required distance in km.

    Return
    ----------
    coordinates : list of the desired coordinates
    """
    lat = math.radians(lat)
    lon = math.radians(lon)

    coordinates = []
    for brng in bearings:
        new_lat = math.asin(math.sin(lat)*math.cos(distance/R) + math.cos(lat)*math.sin(distance/R)*math.cos(brng))

        new_lon = lon + math.atan2(math.sin(brng)*math.sin(distance/R)*math.cos(lat),math.cos(distance/R)-math.sin(lat)*math.sin(new_lat))

        new_lat = round(math.degrees(new_lat),6)
        new_lon = round(math.degrees(new_lon),6)
        
        coordinates.append((new_lat, new_lon))

    return coordinates

def get_limits(lat=None, lon=None, distance=None):
    """
    Parameters
    -----------
    lat, lon : coordinates of current location
    distance : desired distance 

    Return 
    -----------
    tuple of latitude and longitudes at the distance
    """
    c = get_coordinates(lat, lon, distance)
    return (c[2][0], c[0][0], c[1][1], c[3][1])

def fetch_query(lat=None, lon=None, distance=None):
    """
    This function returns a PostgreSQL query for finding records having coordinates in a given range

    Parameters
    ----------
    lat, lon : coordinates
    distance : desired distance 

    Return
    ----------
    query : SQL query with coordinates within which to search for
    """
    lims = get_limits(lat, lon, distance) # tuple of limit coordinates within which search will be done
    query = "SELECT * FROM \"Book\" WHERE (\"latitude\" BETWEEN "
    query = query + str(lims[0]) + " AND " + str(lims[1]) + ") AND (\"longitude\" BETWEEN " + str(lims[3]) + " AND " + str(lims[2]) + ");"

    return query
