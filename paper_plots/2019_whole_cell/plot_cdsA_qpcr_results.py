import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import numpy as np

data_file_name = '052919_070919_071219_results_collated.xlsx'
data_sheet_name = 'data_collated'


data_file_path = os.path.join(os.getcwd(), data_file_name)
data_df = pd.read_excel(data_file_path, 'data_collated')
wc_data_df = pd.read_excel(data_file_path, 'rna_seq')


#import pdb; pdb.set_trace()

#plt.plot(data_df['avg_counts'].values)

 
color_palette = sns.color_palette("husl", 4)

plt.figure(figsize=(5,10))
sns.set_style('white')
bar_plot = sns.barplot(x = data_df['name'], y = data_df['avg_count'], 
	data = data_df, palette = color_palette, yerr = data_df['std_count'])
plt.xlabel('')
plt.ylabel('Counts per 5ng Total RNA')
sns.despine()

for index, row in data_df.iterrows():
	bar_plot.text(x = row.name, y = row.avg_count, s = str(round(row.avg_count,2)), color='black', ha="center")

plt.tight_layout()
fig = bar_plot.get_figure()

fig.savefig('/Users/mialydefelice/Dropbox/Papers/WC_2018/Figures/cdsA_qPCR/qPCR_results.pdf', transparent = True)
#plt.show()
plt.close()


sns.set_style('white')
plt.figure(figsize=(5,10))
bar_plot = sns.barplot(x = wc_data_df['name'], y = wc_data_df['tpm'], 
	data = wc_data_df, palette = color_palette, yerr = wc_data_df['std_tpm'])
plt.xlabel('')
plt.ylabel('tpm')
sns.despine()

for index, row in wc_data_df.iterrows():
	bar_plot.text(x = row.name, y = row.tpm, s = str(row.tpm), color='black', ha="center")

plt.tight_layout()
fig = bar_plot.get_figure()
fig.savefig('/Users/mialydefelice/Dropbox/Papers/WC_2018/Figures/cdsA_qPCR/rna_seq_counts_comparison.pdf', transparent = True)
plt.show()
