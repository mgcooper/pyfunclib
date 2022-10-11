"""
Author: Matt Cooper (https://github.com/mgcooper)
libplot.py (c) 2022, Matt Cooper
Desc: plotting utilities
Created:  2022-10-01T02:03:52.579Z
"""

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms

#-------------------------------------------------------------------------------
#   scatter plot with one to one line
#-------------------------------------------------------------------------------
def scatter1to1(x,y,symcolor='blue',symcmap='none',makefig=True):

    if makefig is True:
        fig, ax = plt.subplots()
    elif len(plt.get_fignums()) == 0:
        # there is no open figure, make one
        fig, ax = plt.subplots()
    else:
        # get the current axis
        ax = plt.gca()

    # add the scatter plot and a one to one line
    if symcmap=='none':
        ax.scatter(x,y,c=symcolor)
    else:
        ax.scatter(x,y,cmap=symcmap)

    line = mlines.Line2D([0, 1], [0, 1], color='black')
    transform = ax.transAxes
    line.set_transform(transform)
    ax.add_line(line)
    plt.show()
    
    return fig,ax
