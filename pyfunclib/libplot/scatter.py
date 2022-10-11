"""
Author: Matt Cooper (https://github.com/mgcooper)
scatter.py (c) 2022, Matt Cooper
Desc: scatter plot utilities
Created:  2022-10-01T02:03:52.579Z
"""

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms
import numpy as np
# from numpy import histogram2d, vstack, divide, sum, sqrt, multiply
from scipy.interpolate import interpn
from scipy import stats

#----------------------------------------------------------------
#   scatterplot with density colormapping
#----------------------------------------------------------------

# NOTE: should probably split into two functions, one that returns x,y,z as in the og func and put that in libdata, and the one that makes the plot

def scatterdensity( x , y, ax = None, sort = True, bins = 20, makefig=True, plotlinreg=False, **kwargs ):
    """
    Scatter plot colored by 2d histogram
    """
    data , x_e, y_e = np.histogram2d( x, y, bins = bins)
    z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([x,y]).T , method = "splinef2d", bounds_error = False )

    # Sort the points by density, so that the densest points are plotted last
    if sort :
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

    if makefig is True:
        fig, ax = plt.subplots(figsize=(8,8))
    elif len(plt.get_fignums()) == 0:
        # there is no open figure, make one
        fig, ax = plt.subplots()
    else:
        # get the current axis
        ax = plt.gca()

    # plot the data
    heatmap = ax.scatter(x, y, c=z, cmap=plt.cm.viridis)
    
    # add a linear regression line if requested
    if plotlinreg is True:

        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

        #Calculate errors
        MBE=np.divide(np.sum(y-x),len(x))
        RMSE=np.sqrt(np.divide(np.sum(np.multiply((y-x),(y-x))),len(x)))

        ax.plot(x, intercept + slope*x, 'k', label='$y$={:.2f}$x${:+.2f}; $r^2$={:.2f}\nRMSE={:.1f}; MBE={:.1f}\n$n$={:.0f}'.format(slope,intercept,(r_value*r_value), RMSE, MBE, x.shape[0]))

        # Add 1:1 line and make sure it is diagonal to plot
        x1 = mlines.Line2D([0, 1], [0, 1], color='red', linestyle='--',linewidth=2)
        transform = ax.transAxes
        x1.set_transform(transform)
        ax.add_line(x1)
        plt.colorbar(heatmap)

    ax.legend(fontsize=16)
    ax.axis('square')
    ax.tick_params(axis="both",labelsize=16)

    #Save figure
    plt.draw()

    # ax.set_xlabel("GEBA $K_{\downarrow,\mathrm{d}}$ (W m$^{-2}$) [Validation]", size=18)
    # ax.set_ylabel("MERRA-2 $K_{\downarrow,\mathrm{d}}$ (W m$^{-2}$) [Validation]", size=18)

    return [fig,ax,x,y,z]

# # this just returns the x,y,z data, see below for usage example
# def density_scatter( x , y, ax = None, sort = True, bins = 20, **kwargs )   :
#     """
#     Scatter plot colored by 2d histogram
#     """
#     data , x_e, y_e = histogram2d( x, y, bins = bins)
#     z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , vstack([x,y]).T , method = "splinef2d", bounds_error = False )

#     # Sort the points by density, so that the densest points are plotted last
#     if sort :
#         idx = z.argsort()
#         x, y, z = x[idx], y[idx], z[idx]

#     return [x,y,z]


# # this is how it was used. i took the main plotting steps and combined with the original function def above to make the active function def above that
# GEBA_obs=np.array(y_valid).flatten()
# MERRA_model=np.array(X_valid['MERRA']).flatten()
# slope, intercept, r_value, p_value, std_err = stats.linregress(GEBA_obs,MERRA_model)

# #Calculate errors
# MBE=np.divide(np.sum(MERRA_model-GEBA_obs),len(GEBA_obs))
# RMSE=np.sqrt(np.divide(np.sum(np.multiply((MERRA_model-GEBA_obs),(MERRA_model-GEBA_obs))),len(GEBA_obs)))

# #Plot figure
# fig = plt.figure(1)
# fig, ax = plt.subplots(figsize=(8,8))
# GEBA_obs, MERRA_model, z_MERRA = density_scatter(GEBA_obs, MERRA_model)
# heatmap = ax.scatter(GEBA_obs, MERRA_model, c=z_MERRA, cmap=plt.cm.viridis)
# ax.plot(GEBA_obs, intercept + slope*GEBA_obs, 'k', label='$y$={:.2f}$x${:+.2f}; $r^2$={:.2f}\nRMSE={:.1f}; MBE={:.1f}\n$n$={:.0f}'.format(slope,intercept,(r_value*r_value), RMSE, MBE, GEBA_obs.shape[0]))
# ax.legend(fontsize=16)
# ax.set_xlabel("GEBA $K_{\downarrow,\mathrm{d}}$ (W m$^{-2}$) [Validation]", size=18)
# ax.set_ylabel("MERRA-2 $K_{\downarrow,\mathrm{d}}$ (W m$^{-2}$) [Validation]", size=18)
# ax.axis('square')
# ax.tick_params(axis="both",labelsize=16)

# #Add 1:1 line and make sure it is diagonal to plot
# x1 = mlines.Line2D([0, 1], [0, 1], color='red', linestyle='--',linewidth=2)
# transform = ax.transAxes
# x1.set_transform(transform)
# ax.add_line(x1)
# plt.colorbar(heatmap)

# #Save figure
# plt.draw()    

#----------------------------------------------------------------
#   scatter plot with one to one line
#----------------------------------------------------------------
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