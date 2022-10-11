"""
Author: Matt Cooper (https://github.com/mgcooper)
geoutils.py (c) 2022, Matt Cooper
Desc: a set of python utilities to interact with geodatframes
Created:  2022-09-30T18:54:45.893Z
Modified:  2022-10-11T18:20:49.081Z
"""

import os
import numpy as np
import pandas as pd
import geopandas as gp
# from osgeo_utils import gdal_utils
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.validation import explain_validity
from shapely.validation import make_valid

#----------------------------------------------------------------------
#   make geometry valid
#----------------------------------------------------------------------
def gdfmakevalid(gdf):

    '''
    extract coordinate pairs from each feature in a gdf and concatenate them into one list, or list of lists. flatten it into one list if requested.
    Inputs
    '''

    # can use these to check first
    anyempty = gdf.geometry.is_empty.any()
    allvalid = gdf.geometry.is_valid.all()

    # # and to remove the invalid rows:
    # empty = gdf.geometry.is_empty
    # gdf = gdf[~empty]

    # but for now, just run it
    gdf.geometry = gdf.apply(lambda row: make_valid(row.geometry) if not row.geometry.is_valid else row.geometry, axis=1)

    return gdf

#------------------------------------------------------------------
#   points in dataframe polygon
#------------------------------------------------------------------

def gdfpointsinpoly(gdf,polygons,flatten=False):

    # this is not finished. the inpoly = gdf.points.within(poly) is correct for one poly as long as the points in gdf are GeoSeries, but i need the concatenation of inpoly into a list or similar, and might need methods to deal with the case where the points in gdf are not GeoSeries. there are two solutions here: https://python.tutorialink.com/when-do-i-need-to-use-a-geoseries-when-creating-a-geodataframe-and-when-is-a-list-enough/
    for ipoly,poly in polygons:
        inpoly = gdf.points.within(poly)
    
    # the pd approach i found online was clever b/c it first added the polygons to the df, then used the df method to find the points in the polys, then removed the polys.
    
    # first add the list of polygon coordinates 
    # df["polygon1"] = df.apply(lambda row: Polygon(polygon1_list).contains(Point(row["X"], row["Y"])), axis = 1)
    # df = df.drop(df[~df["polygon1"]].index)

    return inpoly



#------------------------------------------------------------
#   extract all lat,lon pairs from all geodataframe features
#------------------------------------------------------------
def gdfcoordinatelist(gdf,flatten=False):
    '''
    extract coordinate pairs from each feature in a gdf and concatenate them into one list, or list of lists. flatten it into one list if requested.
    Inputs
    '''
    coordlist = []
    for idx,feature in gdf.iterrows():
        
        if all(gdf.geom_type=='LineString'):
            coords = np.array(feature.geometry.coords)
        elif all(gdf.geom_type=='Point'):
            # not sure if this will work
            coords = np.array(feature.geometry.coords)
        elif all(gdf.geom_type=='Polygon'):
            coords = np.array(Polygon(feature['geometry']).exterior.coords)  
        
        coordlist.append(coords)

        # need a method to figure out if the feature needs to be converted to a polygon first:
        # coords = np.array(Polygon(feature['geometry']).exterior.coords)

    if flatten is True:
        coordlist = [coords for features in coordlist for coords in features]

    return coordlist


# this is apparently another way, from example for pandas df: (update: the og example is the Polygon one, I added the Point one but I think it needs to be flattened and there must be an easier way)
def geomcoordinatelist(geom):
    
    # if all(geom.geom_type=='LineString'):
        #coords = np.array(geom.geometry.coords)
    if all(geom.geom_type=='Point'):
        coords = [np.array(geom.x),np.array(geom.y)]
    elif all(geom.geom_type=='Polygon'):
        coords = list(geom.exterior.coords)
        # coordinates = df.geometry.apply(geomcoordinatelist)
        
    return (coords)

# then in the example it gets applied like this:
# coordinates = df.geometry.apply(geomcoordinatelist)
# so i added that to the def above commented out in case I want to have it accept the df, extract geom, and return the df


# and another way:
# [list(df.geometry.exterior[row_id].coords) for row_id in range(df.shape[0])]
# as above but for multipolygonz:
# [list(shp.geometry.exterior.iloc[row_id].coords) for row_id in range(shp.shape[0])]

#----------------------------------------------------------------------
#   delete shapefile
#----------------------------------------------------------------------

def rmshapefile(path_shp):
    """
    Deletes a shapefile and associated auxiliary files.

    Parameters
    ----------
    path_shp : str
        Path to the shapefile to delete.

    Returns
    -------
    None.
    
    Author: Jon Schwenk, jschwenk@lanl.gov
    """
    if os.path.isfile(path_shp) is True:
        remove_exts = ['.cpg', '.dbf', '.prj', '.shp', '.shx']
        remove_base = os.path.splitext(path_shp)[0]
        for re in remove_exts:
            if os.path.isfile(os.path.normpath(remove_base + re)) is True:
                os.remove(os.path.normpath(remove_base + re))

#-------------------------------------------------------------------
#   create a nan mask for a raster
#-------------------------------------------------------------------
def nanmask(filename, nanval=0):
    """ Returns a mask that is True for nan pixels, else False. 
    Author: Jon Schwenk, jschwenk@lanl.gov
    """
    
    I = gdal.Open(filename).ReadAsArray()
    Mask = np.zeros(I.shape, dtype=np.bool)
    Mask[I==nanval] = True
    
    return Mask
    
#-------------------------------------------------------------------
# convert MULTIPOLYGONZ 
#-------------------------------------------------------------------


# might rename flattenMultiPolygonZ
def convert_3D_2D(geodf):
    '''
    Takes a GeoSeries of 3D Multi/Polygons (has_z) and returns a list of 2D Multi/Polygons

    see: https://gist.github.com/rmania/8c88377a5c902dfbc134795a7af538d8

    Usage:
        geodf_2d = gpd.GeoDataFrame.from_file(shp_file) # plug_in your shapefile
        geodf_2d = convert_3D_2D(geodf_2d) # new geodf with 2D geometry series
        geodf_2d.to_file(path + shapefile.shp, driver = 'ESRI Shapefile') will sore a shapefile with 2D shape types
    '''
    new_geo = []
    for p in geodf.geometry:
        if p.has_z:
            if p.geom_type == 'Polygon':
                lines = [xy[:2] for xy in list(p.exterior.coords)]
                new_p = Polygon(lines)
                new_geo.append(new_p)
            elif p.geom_type == 'MultiPolygon':
                new_multi_p = []
                for ap in p:
                    lines = [xy[:2] for xy in list(ap.exterior.coords)]
                    new_p = Polygon(lines)
                    new_multi_p.append(new_p)
                new_geo.append(MultiPolygon(new_multi_p))
                
    geodf.geometry = new_geo
    return geodf


#-------------------------------------------------------------------------------
# create a gdf
#-------------------------------------------------------------------------------

def df2gdf(df):
    '''
    Takes a dataframe and returns a geodatafram

    see: https://gis.stackexchange.com/questions/345167/building-geodataframe-row-by-row

    Usage:
    '''
    df["geometry"] = df.apply (lambda row: Point(row.lon,row.lat), axis=1)
    gdf = gp.GeoDataFrame(df, geometry=df.geometry)

    # in one line:
    # gdf = gp.GeoDataFrame(df, geometry=df.apply(lambda row: Point(row.lon,row.lat), axis=1))
    return gdf


def dict2gdf(mydict):
    df = pd.DataFrame.from_dict(mydict,orient='index')
    df["geometry"] = df.apply (lambda row: Point(row.lon,row.lat), axis=1)
    gdf = gp.GeoDataFrame(df, geometry=df.geometry)
    return gdf

#-------------------------------------------------------------------------------
# add a new attribute to a gdf (?)
#-------------------------------------------------------------------------------
# links['hs_id'] = [[] for i in range(len(links))]


# for index, poi in test1.iterrows():
#     test1.loc[index, 'geometry'] = test1.loc[index, 'geometry'].translate(xoff=x[index], yoff=y[index])

#-------------------------------------------------------------------------------
# dataframe to geojson
#-------------------------------------------------------------------------------
# https://gist.github.com/rmania

from shapely.geometry import Polygon, mapping

def df_to_geojson(df, properties):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'MultiPolygon',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [mapping(row['geometry'])]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        
        geojson['features'].append(feature)
    return geojson




#-------------------------------------------------------------------------------
#   points in dataframe polygon
#-------------------------------------------------------------------------------

# started to make this then stopped. for gdf it can be as simple as:
# gdf.points.within(polygon)
# so I will use that instead

# # if we have a dataframe and a coordinate list and want to know
# df = pd.DataFrame([[0, 0, 0], [1, 2, 3], [2, 2, 2], [3, 2, 1] ], columns = list("XYZ"))
# #your polygon points
# polygon1_list = [(1, 1), (1, 3), (3, 3), (3, 1)]
# #adding a column that contains a boolean variable for each point
# df["polygon1"] = df.apply(lambda row: Polygon(polygon1_list).contains(Point(row["X"], row["Y"])), axis = 1)
# print(df)

# def dfpointsinpoly(df,flatten=False):

#     # first add the list of polygon coordinates 
#     df["polygon1"] = df.apply(lambda row: Polygon(polygon1_list).contains(Point(row["X"], row["Y"])), axis = 1)
#     df = df.drop(df[~df["polygon1"]].index)

    
