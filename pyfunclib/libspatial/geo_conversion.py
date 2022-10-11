# ------------------------------------------------------------------------------
# geospatial conversions
# ------------------------------------------------------------------------------
import math
import json
import numpy as np
import pandas as pd
import pyproj as proj
from cartopy import crs
from pyproj import Proj, transform
from functools import partial
from shapely.ops import transform
from shapely.geometry import mapping, shape


# ------------------------------------------------------------------------------
def transform_coords(df):
    df = df.copy()
    lons = np.array(df['longitude'])
    lats = np.array(df['latitude'])
    coords = crs.GOOGLE_MERCATOR.transform_points(crs.PlateCarree(), lons, lats)
    df['longitude'] = coords[:, 0]
    df['latitude']  = coords[:, 1]
    return df


# ------------------------------------------------------------------------------
def pdrow2webmercator(inproj,outproj,row):
    """
    convert lon_lat epsg:4326 to WebMercator epsg:3857 on Pandas Series
    """
    return pd.Series(transform(inproj, outproj, row['longitude'], row['latitude']))

# ------------------------------------------------------------------------------
def latlon2webmercator(lat, lon):
    """
    convert lat lon epsg:4326 to WebMercator epsg:3857 on Pandas Series
    """
    # Check if coordinate out of range for Latitude/Longitude
    if (abs(lon) < 180) and (abs(lat) > 90):
        return
 
    # Check if coordinate out of range for Web Mercator
    # 20037508.3427892 is full extent of Web Mercator
    if (abs(lon) > 20037508.3427892) or (abs(lat) > 20037508.3427892):
        return
 
    semimajorAxis = 6378137.0  # WGS84 spheriod semimajor axis
 
    latitude = (1.5707963267948966 - (2.0 * math.atan(math.exp((-1.0 * lat) / semimajorAxis)))) * (180/math.pi)
    longitude = ((lon / semimajorAxis) * 57.295779513082323) - ((math.floor((((lon / semimajorAxis) * 57.295779513082323) + 180.0) / 360.0)) * 360.0)
 
    return [latitude,longitude]

# ------------------------------------------------------------------------------
def webmercator2latlon(lat, lon):
    """ 
    convert WebMercator epsg:3857 to lon_lat epsg:4326 mathematically per point
    """
    #Check if coordinate out of range for Latitude/Longitude 
    if (abs(lon) < 180) and (abs(lat) > 90):
        return
 
    # Check if coordinate out of range for Web Mercator
    # 20037508.3427892 is full extent of Web Mercator
    if (abs(lon) > 20037508.3427892) or (abs(lat) > 20037508.3427892):
        return
 
    semimajorAxis = 6378137.0  # WGS84 spheriod semimajor axis
    latitude = (1.5707963267948966 - (2.0 * math.atan(math.exp((-1.0 * lat) / semimajorAxis)))) * (180/math.pi)
    longitude = ((lon / semimajorAxis) * 57.295779513082323) - ((math.floor((((lon / semimajorAxis) * 57.295779513082323) + 180.0) / 360.0)) * 360.0)
 
    return [latitude,longitude]

# ------------------------------------------------------------------------------ 
def latlon2webmeters(lat,lon):
    """ 
    convert lon_lat epsg:4326 to WebMercator epsg:3857 mathematically per point
    """
    # Check if coordinate out of range for Latitude/Longitude
    if (abs(lon) > 180) and (abs(lat) > 90):
        return
 
    semimajorAxis = 6378137.0  # WGS84 spheriod semimajor axis
    east = lon * 0.017453292519943295
    north = lat * 0.017453292519943295
 
    northing = 3189068.5 * math.log((1.0 + math.sin(north)) / (1.0 - math.sin(north)))
    easting = semimajorAxis * east
 
    return [easting, northing]

# ------------------------------------------------------------------------------
def dflatlon2webmeters(df, lat_column, lon_column):
    """
    function 1 to convert to WebMercator format
    Convert longitude, latitude GPS coordinates into meters west and north of Greenwich (Web Mercator format). This makes it easier to overlay those with tiles from map providers.
    args:
        df: pandas Dataframe
        lon_name: dataframe column where the longitude coordinates are stored
        lat_name: dataframe column where the latitude coordinates are stored
    example:
        lonlat_to_meters(df, 'lon', 'lat')
    returns:
        df with converted coordinates
    """
    lat = df[lat_column]
    lon = df[lon_column]
    df.loc[:, ('x')] = df.loc[:, (lat_column)]
    df.loc[:, ('y')] = df.loc[:, (lon_column)]
    origin_shift = 2 * np.pi * 6378137 / 2.0
    mx = lon * origin_shift / 180.0
    my = np.log(np.tan((90 + lat) * np.pi / 360.0)) / (np.pi / 180.0)
    my = my * origin_shift / 180.0
    df.loc[:, 'x'] = mx
    df.loc[:, 'y'] = my
    
    return df

# below here was in the gist i think
# ------------------------------------------------------------------------------
def rd2wgsgeojson(inproj,outproj,geojson):
   # convert geojson from RD new to WSG84
   reprojection = partial(proj.transform,
                          # Source coordinate system
                          inproj,
                          # Destination coordinate system
                          outproj)
   g1 = shape(geojson)
   g2 = transform(reprojection, g1)  # apply projection
   geom = json.dumps(mapping(g2))

   return geom

# ------------------------------------------------------------------------------
# same but for a Pandas series. This needs to be a string without NaN values

def convertCoords(inproj,outproj,row):
    x2, y2 = transform(inproj,outproj, row['x_coord'], row['y_coord'])
    return pd.Series({'long':x2,'lat':y2})