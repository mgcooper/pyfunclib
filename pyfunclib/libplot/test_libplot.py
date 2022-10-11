"""
Author: Matt Cooper (https://github.com/mgcooper)
test_libplot.py (c) 2022, Matt Cooper
Desc: test the libplot utilities
Created:  2022-10-02T18:41:46.863Z
"""

# none of this is implemented
# ----------------------------

# modify color of yticklabels for the current axes
[i.set_color("red") for i in plt.gca().get_yticklabels()]

# get all tweakable parameters of 'ytick' etc..
[(param, value) for param, value in plt.rcParams.items() if 'ytick' in param]

# get the yticklabel texts
[item.get_text() for item in axi.get_yticklabels()]

#change label display parameters like fontsize
[tick.label.set_fontsize(14) for tick in ax.yaxis.get_major_ticks()]

# change xticklabel colors
for ticklabel, tickcolor in zip(plt.gca().get_xticklabels(), my_colors):
    ticklabel.set_color(tickcolor)

# color bar yticklabels manipulation
cbar.ax.set_yticklabels(['{:.0f}'.format(x) for x in np.arange(cbar_min, cbar_max+cbar_step, cbar_step)], fontsize=16, weight='bold')

# For every axis, set the x and y major locator
for axi in ax.flat:
    axi.xaxis.set_major_locator(plt.MaxNLocator(3))
    axi.yaxis.set_major_locator(plt.MaxNLocator(3))
    
# get float of 2 decimals for the xticks
['{:,.2f}'.format(x) for x in xticks]