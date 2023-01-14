"""
Author: Matt Cooper (https://github.com/mgcooper)
libhydro.py (c) 2022, Matt Cooper
Desc: library of hydrology related functions
Created:  2022-10-14T16:58:40.701Z
"""

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def hydrograph():

    """
    hydrograph plot
    this wasn't defined as a function, it was inline, so i put it here to adapt to func
    """
    fig = plt.figure(figsize=(20,5))
    ax  = fig.add_subplot(111)
    ax.set_xlabel('Time', fontsize = 24, fontweight = 'bold')
    ax.set_ylabel('Streamflow', fontsize = 24, fontweight = 'bold')
    ax.tick_params(axis = 'x', which = 'major', labelsize = 20, length = 6, width = 2)
    ax.tick_params(axis = 'y', which = 'major', labelsize = 20, length = 6, width = 2)
    ax.set_ylim([0, 80])
    sns.lineplot(t_list, q_obs, linestyle = 'solid', linewidth = 2.5, color = 'black', \
                marker = None, label = 'Observed') #Obs. discharge data
    sns.lineplot(t_list, q_mean, linestyle = 'dashed', linewidth = 2.5, color = 'rosybrown', \
                marker = None, label = 'mean ensemble') #Mean discharge data
    tick_spacing = 200
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.legend(loc = 'upper right')
    fig.tight_layout()
    plt.show()


def hydrographensemble( num_realz, t_list, y_ens, y_mean, y_lb, y_ub, y_obs, \
                str_x_label, str_y_label, fig_name, \
                legend_loc, plot_label_list, num_ticks, \
                line_width_ens, alpha_val, col_list):


    """
    hydrograph plot
    """
    legend_properties = {'weight':'bold'}
    fig               = plt.figure(figsize=(20,5))
    #
    #plt.rc('text', usetex = True)
    #plt.rcParams['font.family']     = ['sans-serif']
    #plt.rcParams['font.sans-serif'] = ['Lucida Grande']
    #plt.rc('legend', fontsize = 18)
    ax = fig.add_subplot(111)
    ax.set_xlabel(str_x_label, fontsize = 24, fontweight = 'bold')
    ax.set_ylabel(str_y_label, fontsize = 24, fontweight = 'bold')
    ax.tick_params(axis = 'x', which = 'major', labelsize = 20, length = 6, width = 2)
    ax.tick_params(axis = 'y', which = 'major', labelsize = 20, length = 6, width = 2)
    ax.set_ylim([0, 80])
    sns.lineplot(t_list, y_obs, linestyle = 'solid', linewidth = line_width_ens[0], color = col_list[0], \
                 marker = None, label = plot_label_list[0]) #Obs. discharge data
    sns.lineplot(t_list, y_mean, linestyle = 'dashed', linewidth = line_width_ens[1], color = col_list[1], \
                 marker = None, label = plot_label_list[1]) #Mean discharge data
    for i in range(0,num_realz):
        if i == 0:
            sns.lineplot(t_list, y_ens[:,i], linestyle = 'solid', \
                        linewidth = 0.1, color = col_list[2], \
                        marker = None, label = plot_label_list[2], \
                        alpha = alpha_val) #SWAT ensemble discharge FDC
        else:
            sns.lineplot(t_list, y_ens[:,i], linestyle = 'solid', \
                        linewidth = 0.1, color = col_list[2], \
                        marker = None, alpha = alpha_val) #SWAT ensemble discharge FDC
    tick_spacing = num_ticks
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.legend(loc = legend_loc)
    fig.tight_layout()
    fig.savefig(fig_name + '.pdf')
    fig.savefig(fig_name + '.png', dpi = 300) #Medium res-fig
    plt.close(fig)


def fdcplotensemble(x_list, y_ens, y_mean, y_obs, str_x_label, str_y_label, fig_name, \
                    legend_loc, plot_label_list, num_ticks, \
                    line_width_ens, alpha_val, col_list):

    #------------------------------------------;
    #  Obs data vs. mean ens data +/- 2 * std  ;
    #------------------------------------------;
    legend_properties = {'weight':'bold'}
    fig               = plt.figure()
    #
    #plt.rc('text', usetex = True)
    #plt.rcParams['font.family']     = ['sans-serif']
    #plt.rcParams['font.sans-serif'] = ['Lucida Grande']
    #plt.rc('legend', fontsize = 18)
    ax = fig.add_subplot(111)
    ax.set_xlabel(str_x_label, fontsize = 24, fontweight = 'bold')
    ax.set_ylabel(str_y_label, fontsize = 24, fontweight = 'bold')
    ax.tick_params(axis = 'x', which = 'major', labelsize = 12, length = 6, width = 2)
    ax.tick_params(axis = 'y', which = 'major', labelsize = 12, length = 6, width = 2)
    ax.set_xlim([0, 100])
    for i in range(0,num_realz):
        if i == 0:
            ax.plot(x_list, y_ens[:,i], linestyle = 'solid', \
                        linewidth = 0.5, color = col_list[2], \
                        marker = None, label = plot_label_list[2], \
                        alpha = alpha_val) #SWAT ensemble discharge FDC
        else:
            ax.plot(x_list, y_ens[:,i], linestyle = 'solid', \
                        linewidth = 0.5, color = col_list[2], \
                        marker = None, alpha = alpha_val) #SWAT ensemble discharge FDC
    ax.plot(x_list, y_obs, linestyle = 'solid', linewidth = line_width_ens[0], color = col_list[0], \
                 marker = None, label = plot_label_list[0]) #Obs. discharge FDC
    ax.plot(x_list, y_mean, linestyle = 'dashed', linewidth = line_width_ens[1], color = col_list[1], \
                 marker = None, label = plot_label_list[1]) #Mean discharge FDC
    ax.set_yscale('log')
    tick_spacing = num_ticks
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.legend(loc = legend_loc)
    fig.tight_layout()
    fig.savefig(fig_name + '.pdf')
    fig.savefig(fig_name + '.png', dpi = 300) #Medium res-fig
    plt.close(fig)

def fdcplot(x_list, y_mean, y_lb, y_ub, y_obs, \
            str_x_label, str_y_label, fig_name, \
            legend_loc, plot_label_list, num_ticks, \
            line_width_ens, alpha_val, col_list):

    """
    flow duration curve plot

    """
    legend_properties = {'weight':'bold'}
    fig = plt.figure()
    #
    #plt.rc('text', usetex = True)
    #plt.rcParams['font.family']     = ['sans-serif']
    #plt.rcParams['font.sans-serif'] = ['Lucida Grande']
    #plt.rc('legend', fontsize = 18)
    ax = fig.add_subplot(111)
    ax.set_xlabel(str_x_label, fontsize = 24, fontweight = 'bold')
    ax.set_ylabel(str_y_label, fontsize = 24, fontweight = 'bold')
    ax.tick_params(axis = 'x', which = 'major', labelsize = 12, length = 6, width = 2)
    ax.tick_params(axis = 'y', which = 'major', labelsize = 12, length = 6, width = 2)
    ax.set_xlim([0, 100])
    ax.plot(x_list, y_obs, linestyle = 'solid', linewidth = line_width_ens[0], color = col_list[0], \
                 marker = None, label = plot_label_list[0]) #Obs. discharge FDC
    ax.plot(x_list, y_mean, linestyle = 'dashed', linewidth = line_width_ens[1], color = col_list[1], \
                 marker = None, label = plot_label_list[1]) #Mean discharge FDC
    ax.fill_between(x_list, y_lb, y_ub, linestyle = 'solid', linewidth = 0.5, \
                    color = col_list[2], alpha = alpha_val) #Mean +/ 2*std or 95% CI
    ax.set_yscale('log')
    tick_spacing = num_ticks
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.legend(loc = legend_loc)
    fig.tight_layout()
    fig.savefig(fig_name + '.pdf')
    fig.savefig(fig_name + '.png', dpi = 300) #Medium res-fig
    plt.close(fig)


def plot_histplot(data_list, num_bins, label_name, \
				str_x_label, str_y_label, fig_name, loc_pos):

    #----------------------------------;
    #  Pre-processed data (histogram)  ;
    #----------------------------------;
    legend_properties = {'weight':'bold'}
    fig               = plt.figure()
    #
    #plt.rc('text', usetex = True)
    #plt.rcParams['font.family']     = ['sans-serif']
    #plt.rcParams['font.sans-serif'] = ['Lucida Grande']
    #plt.rc('legend', fontsize = 14)
    ax = fig.add_subplot(111)
    ax.set_xlabel(str_x_label, fontsize = 24, fontweight = 'bold')
    ax.set_ylabel(str_y_label, fontsize = 24, fontweight = 'bold')
    ax.tick_params(axis = 'both', which = 'major', labelsize = 20, length = 6, width = 2)
    ax.hist(data_list, bins = num_bins, label = label_name, \
    		edgecolor = 'k', alpha = 0.5, color = 'b', density = True)
    ax.legend(loc = loc_pos)
    fig.tight_layout()
    fig.savefig(fig_name + '.pdf')
    fig.savefig(fig_name + '.png')
    plt.close(fig)