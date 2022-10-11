"""
Author: Matt Cooper (https://github.com/mgcooper)
Untitled-1 (c) 2022, Matt Cooper
Desc: description
Created:  2022-10-01T03:32:52.716Z
"""

#-------------------------------------------------------------------------------
# other methods to drop z

# commenters say the preferred method is shapely.ops b/c it works on any shape and returns the same shape.
# 
#  Example 1:
# import shapely.ops
# p = Point(2, 3) # no z
# pz = shapely.ops.transform(lambda x, y: (x, y, 2), p) # now pz is p with a z coordinate
# 
#  Example 2:
# l = shapely.geometry.LineString(([2, 3, 6], [4, 5, -1]))
# shapely.ops.transform(lambda x, y, z=None: (x, y), l).wkt  # 'LINESTRING (2 3, 4 5)'

# commenter also says this works:
# geom = shapely.wkb.load(shapely.wkb.dumps(geom,output_dimension=2))

# this is the same as above 
# import geopandas as gpd
# from shapely import wkb

# _drop_z = lambda geom: wkb.loads(wkb.dumps(geom, output_dimension=2))
# df.geometry = df.geometry.transform(_drop_z)

# commenter says this is better
from functools import singledispatch
from operator import itemgetter
from typing import TypeVar

from shapely.geometry import Polygon
from shapely.geometry.base import (BaseGeometry,
                                   BaseMultipartGeometry)

Geometry = TypeVar('Geometry', bound=BaseGeometry)


@singledispatch
def drop_z(geometry: Geometry) -> Geometry:
    """
    Removes Z-coordinate from a geometry object.
    Won't be necessary after it will be implemented in Shapely:
    https://github.com/Toblerity/Shapely/issues/709
    """
    if geometry.is_empty:
        return geometry
    geometry_type = type(geometry)
    xy_coordinates = map(itemgetter(0, 1), geometry.coords)
    return geometry_type(list(xy_coordinates))


@drop_z.register
def _(geometry: BaseMultipartGeometry):
    geometry_type = type(geometry)
    return geometry_type(list(map(drop_z, geometry.geoms)))


@drop_z.register
def _(geometry: Polygon):
    if geometry.is_empty:
        return geometry
    new_exterior = drop_z(geometry.exterior)
    new_interiors = list(map(drop_z, geometry.interiors))
    return Polygon(new_exterior, new_interiors)
