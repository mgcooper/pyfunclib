"""
Author: Matt Cooper (https://github.com/mgcooper)
datautils.py (c) 2023, Matt Cooper
Desc: a set of python utilities to interact with general data structures
Created:  2023-01-13T18:54:45.893Z
Modified:  2023-01-13T23:59:50.827Z
"""

import functools
import operator
import numpy as np
import pandas as pd
import geopandas as gpd
try:
    from itertools import izip_longest as zip_longest 
except ImportError:
    from itertools import zip_longest

#------------------------------------------------------------------------------
def sortrows(data,column,direction='descend'):

    """
    Author: Matt Cooper (https://github.com/mgcooper)
    sortrows.py (c) 2022, Matt Cooper
    Desc: function to sort rows of a list
    Created:  2022-10-04T01:49:26.033Z
    """
    # from numpy import array, flipud, argsort
    data = np.array(data).transpose()
    if direction == 'ascend':
        idx = np.argsort( data[:,column] )
    elif direction == 'descend':
        idx = np.flipud(np.argsort( data[:,column] ))
    data = data[idx,:]
    return data,idx

#------------------------------------------------------------------------------
def flattenlist(nestedlist):
    flatlist = []
    for eachlist in nestedlist:
        if type(eachlist) is list:
            flatlist.append(eachlist)
        else:
            flatlist.append([eachlist])
    return flatlist
    # might need to apply this:  functools.reduce(operator.iconcat, regular_list, []))

#------------------------------------------------------------------------------
def ismember(A, B):
    return [ np.sum(a == B) for a in A ]
# def ismember(A, B):
#   return [1 if (i == B) else 0 for i in A]

#------------------------------------------------------------------------------
def list2file(thelist,filename):
    with open(filename, 'w') as output:
        for eachrow in thelist:
            output.write(str(eachrow) + '\n')

#------------------------------------------------------------------------------
def padarray(arraylist,padval=np.nan):

    # might need the pd.Dataframe(list( ... )).values method on DataFrame cases
    if isinstance(arraylist, pd.DataFrame):
        return arraylist.fillna(padval).values
        # return pd.DataFrame(arraylist).values
    elif isinstance(arraylist, gpd.GeoDataFrame):
        return arraylist.fillna(padval).values
    elif isinstance(arraylist,pd.Series):
        return pd.DataFrame(list(arraylist.fillna(padval))).values
        # return pd.DataFrame(list(arraylist)).fillna(padval).values

    # this may be fastest
    return np.array(list(zip_longest(*arraylist, fillvalue=padval))).T

    # this is fast and understandable
    # cols=len(max(arraylist, key=len))
    # rows=len(arraylist)
    # paddedarray=np.empty((rows,cols, ))
    # paddedarray.fill(padval)
    # for idx in range(rows):
    #     paddedarray[idx,0:len(arraylist[idx])]=arraylist[idx]
    # return paddedarray

    # if we have a 2-d list this may work but it failed on my test:
    # from numpy import nan
    # maxlen = max(len(eachlist) for eachlist in arraylist)
    # for eachlist in arraylist:
    #     eachlist.extend([nan] * (maxlen - len(eachlist)))

    # other options:
    
    # this has fewest loops
    # lengths = np.array([len(eachlist) for eachlist in arraylist])
    # mask = lengths[:,None] > np.arange(lengths.max())
    # paddedarray = np.full(mask.shape,padval)
    # paddedarray[mask] = np.concatenate(arraylist)
    # return paddedarray

    # this converts to a df, same as pd.Series option
    # return pd.DataFrame(list(arraylist)).fillna(np.nan).values

    # this would require converting padval to np.pad options. 'empty'=nan, 'constant'=0, there are several others
    # maxlen = len(max(arraylist, key=len))
    # return np.array([np.pad(eachlist, (0, maxlen-len(eachlist)), 'empty') for eachlist in arraylist])

    # this is clearest imo
    # lengths = [len(eachlist) for eachlist in arraylist]
    # shape = (len(arraylist), max(lengths))
    # paddedarray = np.full(shape, padval)
    # for ilist, eachlist in enumerate(arraylist):
    #     paddedarray[ilist, :lengths[ilist]] = eachlist
    # return paddedarray

    # lengths can also be gotten this way:
    # lengths = [eachlength for eachlength in map(len, arraylist)]

    