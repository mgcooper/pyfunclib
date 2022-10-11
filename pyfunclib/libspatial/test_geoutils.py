"""
Author: Matt Cooper (https://github.com/mgcooper)
test_geoutils.py (c) 2022, Matt Cooper
Desc: a script to test geoutils
Created:  2022-09-30T19:32:49.945Z
Modified:  2022-10-02T19:31:21.041Z
"""
import os
# from geoutils import os, gpd, convert_3D_2D
# import geoutils.convert_3D_2D
from .geoutils import convert_3D_2D

import pandas as pd
import geopandas as gp
from shapely.geometry import Point
from pyproj import Proj, transform
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(override=True)

# dotenv.dotenv_values(".env")
# print(os.environ.get('DATAPATH'))

datapath = os.getenv('DATAPATH')
fname = 'glims_polygons_fixed_geom_ease.shp'
fgeodf = datapath + fname
geodf = gp.read_file(fgeodf)
geodf.head()

geodf = convert_3D_2D(geodf)


# ----------------
# test pdrow2webmercator
from pyproj import Proj

inproj = Proj(init='epsg:4326')
outproj = Proj(init = 'epsg:3857')


# ----------------
# test rd2wgsgeojson
inproj = proj.Proj(init='epsg:28992')
outproj = proj.Proj(init='epsg:4326')


# ----------------
# test convertCoords
inproj = Proj(init='epsg:28992')
wgs84= Proj("+init=EPSG:4326") # LatLon with WGS84 datum used by GPS units and Google Earth

for i in test[['x_coord', 'y_coord']]:
    test.copy().loc[:,i] = test.loc[:,i].astype(str)


# create subset with latitude/ longitude (NaN values to be removed)
lon_lat = test.dropna(subset = ['x_coord', 'y_coord'])[['x_coord', 'y_coord']]
lon_lat = lon_lat.join(lon_lat.apply(convertCoords, axis=1))

# join back on original frame
test = pd.merge(test, lon_lat, left_index= True, right_index=True, how= 'left')





# --------------------------------------------------------------------------------
# test dict2gdf and df2gdf
# --------------------------------------------------------------------------------

# this also shows how to construct a dict and various ways to index dicts, dfs, and gdfs. https://gis.stackexchange.com/questions/345167/building-geodataframe-row-by-row

d = {'007': {'name': 'A', 'lat': 48.843664, 'lon': 2.302672, 'type': 'small' },
     '008': {'name': 'B', 'lat': 50.575813, 'lon': 7.258148, 'type': 'medium'},
     '010': {'name': 'C', 'lat': 47.058420, 'lon': 15.437464,'type': 'big'}}

# brute force it:
tmp_list = []
for item_key, item_value in d.items() :
    tmp_list.append({
      'geometry' : Point(item_value['lon'], item_value['lat']),
      'id': item_key,
      'name': item_value ['name'],
      'type': item_value ['type']
     })
gdf = gp.GeoDataFrame(tmp_list)

print(gdf.head())


## SOLUTION 1. Duration: ~2.3 ms, @gene's answer.
df = pd.DataFrame.from_dict(d, orient='index')
df["geometry"] = df.apply (lambda row: Point(row.lon,row.lat), axis=1)
gdf = gp.GeoDataFrame(df, geometry=df.geometry)
## 

## SOLUTION 2. Duration: ~2.5 ms
gdf = gp.GeoDataFrame()    
gdf["id"]   = [k for k in d.keys()]
gdf["name"] = [d[k]["name"] for k in d.keys()]
gdf["type"] = [d[k]["type"] for k in d.keys()]
gdf["geometry"]  = [Point(d[k]["lon"], d[k]["lat"]) for k in d.keys()]    
gdf.set_index('id', inplace=True)
##


## SOLUTION 3. Duration: ~9.5 ms
gdf = gp.GeoDataFrame(columns=["name", "type", "geometry"])
for k, v in d.items():
    gdf.loc[k] = (v["name"], v["type"], Point(v["lon"], v["lat"]))
##

print(gdf)
