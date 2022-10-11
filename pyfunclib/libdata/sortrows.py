"""
Author: Matt Cooper (https://github.com/mgcooper)
sortrows.py (c) 2022, Matt Cooper
Desc: function to sort rows of a list
Created:  2022-10-04T01:49:26.033Z
"""
from numpy import array, flipud, argsort

def sortrows(data,column,direction='descend'):
    
    data = array(data).transpose()
    if direction == 'ascend':
        idx = argsort( data[:,column] )
    elif direction == 'descend':
        idx = flipud(argsort( data[:,column] ))
    
    data = data[idx,:]

    return data,idx