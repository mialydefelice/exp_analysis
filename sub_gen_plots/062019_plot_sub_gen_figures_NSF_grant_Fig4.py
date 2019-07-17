import pandas as pd
import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'sub_gen_plots', 'functions'))
import functions.plot_sub_gen_figures_functions as sub_gen_func
import functions.general_functions as gen_func

#---- GATHER ALL PATH DATA ----#
'''
data_directory: base path where genes.tsv and the count data is stored
counts_subfolder: subfolder where the count data is stored within the data directory
genes_subfolder: subfolder where the gene datea is stored within the data directory
output_path: base folder we want to store the plots (additional subfolders will be added later)
'''
data_directory = '/Users/mialydefelice/Dropbox/Mialy/Modeling/TranscriptionUnitStructure/2019/WCM_FlatFiles'
counts_subfolder = 'SubgenerationalPlotData'
genes_subfolder = 'reconstruction'
genes_filename = 'genes.tsv'
subgen_data_filename = 'SubGenData.tsv'

output_path_base = '/Users/mialydefelice/Dropbox/papers/NSF_Grant_2019/Figures/Figure4'

#---- GENES TO PLOT / COLORS TO PLOT ----#
#Note will not currently work with synonyms
operon_genes = [['lacZ', 'lacY', 'lacA'], ['cadA', 'cadB']]
operon_names = ['lac_operon', 'cad_operon']
#colors = ['#077de8', '#c82606', '#dcbe23'] # RNA color, Protein color (Blue, red, yellow)
colors = ['#00b8de', '#cd288e', '#dcbe23']
plot_type = ['RNA_2', 'Protein_2']

#---- CREATE ALL PATHS / MAKE OUTPUT DIRECTORY ----#

subgen_data_path = os.path.join(data_directory, counts_subfolder, subgen_data_filename)
genes_model_path = os.path.join(data_directory, genes_subfolder, genes_filename)
full_output_path = os.path.join(output_path_base, 'sub_gen_plots', gen_func.get_todays_date())

gen_func.make_output_directory(full_output_path)

#---- LOAD DATA ----#
genesWC = pd.read_csv(genes_model_path, sep='\t', index_col=False)
sub_gen_data = pd.read_csv(subgen_data_path, sep = '\t', index_col = False)

#--- MAKE FIGURES ----#
'''
ids_locs = []
for operon in operon_genes:
	ids_locs.append(sub_gen_func.gather_protein_rna_ids_locs(operon, genesWC, sub_gen_data))
'''
#import ipdb; ipdb.set_trace()

count = 0
for operon in operon_genes:
	ids_loc = sub_gen_func.gather_protein_rna_ids_locs(operon, genesWC, sub_gen_data)
	for i in range(0, len(ids_loc)-1):
		#import ipdb; ipdb.set_trace()
		sub_gen_func.plot_operon(sub_gen_data, ids_loc[i], 
			colors, full_output_path, plot_type [i], operon_names[count])
	count += 1

#

# --- MAKE SUBFIGURES ---#
'''
sub_gen_func.subplot_counts(sub_gen_data, ids_locs, genes_to_pull, colors, full_output_path)
'''