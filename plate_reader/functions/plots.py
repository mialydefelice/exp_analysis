import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

from functions.data_handling import convert_timestamp

def gather_data_to_plot(wells, df):
    """
    Given a well ID, plot the associated data, pull out treatments.
    Pull in dataframe of all the data.
    """
    data_to_plot = []
    error_to_plot = []
    legend = []
    for well in wells:
        data_to_plot.append(df.loc[well, '600_averaged'])
        error_to_plot.append(df.loc[well, '600_std'])
        legend.append(df.loc[well, 'cell'])
    return data_to_plot, error_to_plot, legend

def quick_plot_all_wells(df, fig_save_path, upper_bound):
    wavelengths_used = df.columns.values.tolist()
    for wavelength in wavelengths_used:
        fig, axs = plt.subplots(8, 12, sharex='col', sharey='row', figsize = (20, 10))
        sns.set_style('ticks')
        axs = axs.flatten()
        fig.subplots_adjust(hspace = .2, wspace=.2)
        x = convert_timestamp(list(df[wavelength].iloc[0]))
        for i in range(2, 98):
            y = list(df[wavelength].iloc[i])
            axs[i-2].plot(x, y, color = '#d55e00')
            axs[i-2].set_ylim(0, upper_bound)
    fig.savefig(os.path.join(fig_save_path, 'plot_all_wells_' + wavelength + '.pdf'), 
                    bbox_inches='tight')
    plt.show()
    return 

def make_individual_plots(time, conditions, condition_names, df_merged, fig_save_path, y_max, xbounds, fig_name_header):
    for j in range(len(conditions)):
        data_to_plot, error_to_plot, legendName = gather_data_to_plot(conditions[j][0], df_merged)
        f = plt.figure(figsize=(20,10))
        sns.set_style('ticks')
        plt.xlabel("Time (min)")
        plt.ylabel("OD_600")
        plt.title("UV")
        color_palette = ['#e69f00','#56b4e9', '#009e73', '#f0e442', '#d55e00', '#cc79a7']
        c = 0
        for data in data_to_plot:
            error = error_to_plot[c]
            plt.semilogy(time, data,  color_palette[c], linewidth = 4, alpha = .8, label = legendName[c])
            plt.fill_between(np.array(time), np.array(data)- np.array(error), 
                             np.array(data) + np.array(error), alpha=0.15, facecolor = color_palette[c])
            plt.ylim([0,y_max])
            plt.xlim(xbounds)
            c += 1
        plt.legend()
        sns.despine()
        f.savefig(os.path.join(fig_save_path, fig_name_header + condition_names[j] + '.pdf'), 
                        bbox_inches='tight')
        plt.show()
        plt.clf()
    return