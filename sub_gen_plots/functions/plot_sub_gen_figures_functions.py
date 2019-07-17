import csv

import pandas as pd
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
#import pickle

def gather_protein_rna_ids(genes, gene_df):
	eco_cyc_ids= []
	monomer_ids = []
	rna_ids = []
	for gene in genes:
		eco_cyc_ids.append(gene_df.loc[(gene_df['symbol'] == gene), 'id'].tolist())
		monomer_ids.append(gene_df.loc[(gene_df['symbol'] == gene), 'monomerId'].tolist())
		rna_ids.append(gene_df.loc[(gene_df['symbol'] == gene), 'rnaId'].tolist())
	return rna_ids, monomer_ids

def gather_protein_rna_ids_locs(genes, gene_df, sub_gen_df):
	rna_ids, monomer_ids = gather_protein_rna_ids(genes, gene_df)
	monomer_id_locs = []
	rna_id_locs = []
	for monomer_id in monomer_ids:
		monomer_id_locs.append([col for col in sub_gen_df.columns if monomer_id[0] in col])
	for rna_id in rna_ids:
		rna_id_locs.append(rna_id[0] + '[c]')
	plot_types = ['RNA', 'protein'] #indicates the order the data is output.
	return rna_id_locs, monomer_id_locs, plot_types

def plot_counts(data, id_to_plot, gene_name, line_color, plot_type, output_path):
	'''
	data: dataframe containing sub-gen data
	id_to_plot: depending on if its an RNA or protiein, will be either the monomer id with location
		tag, or rna_id with the location tag.
	line_color: want to plot RNA and protein in differnet colors, specify that color here.
	plot_type: string stating if we are plotting a protein or rna, will end up in the plot name
	'''
	plt.figure(figsize=( 3, 2.4))
	#plt.axis('off')
	sns.set_style('ticks')
	for gen in np.unique(data['gen']):
		df_gen = data[data['gen']==gen]
		plt.plot(df_gen['time']/60, df_gen[id_to_plot], color = line_color, alpha = 0.8, linewidth = 1.5)
	custom_lines = [Line2D([0], [0], color = line_color, lw = 1.5)]
	sns.despine()
	plt.tight_layout()
	plt.savefig(os.path.join(output_path, gene_name + '_plot_' + plot_type + '.pdf'), transparent = True, bbox_inches='tight', pad_inches=0)
	return

def subplot_counts(data, ids_locs, gene_names, line_colors, output_path):
	fig, ax = plt.subplots(2, 5, figsize = (9.5, 3), sharex = True)
	pos_options = [0,1,2,3,4,0,1,2,3,4]
	y_ranges = [(0,1), (0,275)]
	#plt.figure(figsize=( 3, 2.4))
	#plt.axis('off')
	sns.set_style('ticks')
	j = 0
	for i in range(0, len(ids_locs)-1):
		count = 0
		for id_loc in ids_locs[i]:
			for gen in np.unique(data['gen']):
				df_gen = data[data['gen']==gen]
				col = pos_options[count]
				ax[j, col ].plot(df_gen['time']/60, df_gen[id_loc], color = line_colors[j], 
					alpha = 0.8, linewidth = 1.5)
			#custom_lines = [Line2D([0], [0], color = line_colors[j], lw = 1.5)]
			print(j, col)
			#
			if count == 4:
				j += 1
			count +=1
		
	sns.despine()
	plt.tight_layout()
	plt.savefig(os.path.join(output_path,'subplot_all_genes.pdf'), 
		transparent = True, bbox_inches='tight', pad_inches=0)
		
	return

def plot_operon(data, id_to_plot, line_color, output_path, plot_type, name):
	plt.figure(figsize=( 4, 2))
	sns.set_style('ticks')
	for gen in np.unique(data['gen']):
		df_gen = data[data['gen']==gen]
		for i in range(0,len(id_to_plot)):
			#import ipdb; ipdb.set_trace()
			plt.plot(df_gen['time']/60, df_gen[id_to_plot[i]], color = line_color[i], alpha = 0.8, linewidth = 3)
	#custom_lines = [Line2D([0], [0], color = line_color[i], lw = 1.5)]
	sns.despine()
	plt.tight_layout()
	plt.savefig(os.path.join(output_path, name + '_plot_' + plot_type + '.pdf'), transparent = True, bbox_inches='tight', pad_inches=0)
	return


