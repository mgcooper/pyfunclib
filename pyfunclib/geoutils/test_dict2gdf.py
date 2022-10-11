"""
Author: Matt Cooper (https://github.com/mgcooper)
test_dict2gdf.py (c) 2022, Matt Cooper
Desc: description
Created:  2022-10-02T17:33:24.256Z
"""

# 



d = {'007': {'name': 'A', 'lat': 48.843664, 'lon': 2.302672, 'type': 'small' },
     '008': {'name': 'B', 'lat': 50.575813, 'lon': 7.258148, 'type': 'medium'},
     '010': {'name': 'C', 'lat': 47.058420, 'lon': 15.437464,'type': 'big'}}

## IN THE ABOVE CASE. Duration: ~1 ms (milisecond)
tmp_list = []
for item_key, item_value in d.items() :
    tmp_list.append({
      'geometry' : Point(item_value['lon'], item_value['lat']),
      'id': item_key,
      'name': item_value ['name'],
      'type': item_value ['type']
     })
gdf = gpd.GeoDataFrame(tmp_list)
##


## SOLUTION 1. Duration: ~2.3 ms, @gene's answer.
df = pd.DataFrame.from_dict(d, orient='index')
df["geometry"] = df.apply (lambda row: Point(row.lon,row.lat), axis=1)
gdf = gpd.GeoDataFrame(df, geometry=df.geometry)
##


## SOLUTION 2. Duration: ~2.5 ms
gdf = gpd.GeoDataFrame()    
gdf["id"]   = [k for k in d.keys()]
gdf["name"] = [d[k]["name"] for k in d.keys()]
gdf["type"] = [d[k]["type"] for k in d.keys()]
gdf["geometry"]  = [Point(d[k]["lon"], d[k]["lat"]) for k in d.keys()]    
gdf.set_index('id', inplace=True)
##


## SOLUTION 3. Duration: ~9.5 ms
gdf = gpd.GeoDataFrame(columns=["name", "type", "geometry"])
for k, v in d.items():
    gdf.loc[k] = (v["name"], v["type"], Point(v["lon"], v["lat"]))
##

print(gdf)
