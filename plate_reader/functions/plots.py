import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
%matplotlib inline

from functions.data_handling import convert_timestamp

def quick_plot_all_wells(df, fig_save_path):
    wavelengths_used = df.columns.values.tolist()
    for wavelength in wavelengths_used:
        fig, axs = plt.subplots(8, 12, sharex='col', sharey='row', figsize = (20, 10))
        sns.set_style('ticks')
        axs = axs.flatten()
        fig.subplots_adjust(hspace = .2, wspace=.2)
        x = convert_timestamp(list(df[wavelength].iloc[0]))
        for i in range(2, 98):
            y = [float(j) for j in list(df[wavelength].iloc[i])]
            axs[i-2].plot(x, y, color = '#d55e00')
            axs[i-2].set_ylim(0, 0.6)
    fig.savefig(os.path.join(fig_save_path, 'plot_all_wells_' + wavelength + '.pdf'), 
                    bbox_inches='tight')
    plt.show()
    return 