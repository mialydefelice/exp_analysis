#import packages
import datetime
import itertools
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import csv
import seaborn as sns

from functions.data_handling import *
from functions.plots import *

'''
Note: Merging biological replicates will merge all associated technical replicates as well.
'''

base_file_path = '/Users/mialydefelice/Dropbox/Mialy/Experiments/TranscriptionUnitStructure'
additional_path_info = '2019'
file_name_base = '060419_S13_S21_growth'
merge_biological_replicates = True
merge_tech_replicates = True
wells_to_exclude = []

df_data, df_merged, time = parse_data_file(file_name_base, base_file_path, wells_to_exclude, 
                                          merge_biological_replicates, merge_tech_replicates)

fig_save_path = create_fig_save_folder(base_file_path, file_name_base)
csv_save_path = os.path.join(base_file_path, additional_path_info, file_name_base)
quick_plot_all_wells(df_data, fig_save_path, 0.6)
df_merged.to_csv(os.path.join(csv_save_path, 'df_merged.csv'))

BW25113 = [['C2']]
del_pabC = [['C3']]
del_pabC_no_kan = [['C4']]

conditions = [BW25113, del_pabC, del_pabC_no_kan]
condition_names = ['BW25113','del_pabC', 'del_pabC_no_kan']


make_individual_plots(time, conditions, condition_names, df_merged, fig_save_path, 1, [0, 1440], 'pabC_growth_Curve')

make_individual_plots_subplot(time, conditions, condition_names, df_merged, fig_save_path, 1, [0, 1440], 'pabC_growth_Curve_subplot')