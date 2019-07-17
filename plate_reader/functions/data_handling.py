import datetime
import itertools
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import csv
import seaborn as sns

def find_data_path(filename_base, base_file_dir):
    """
    If it is not already so, make sure the filename and the enclosing
    folder have the same name.
    i.e. /121118_UmuD_C_Growth/121118_UmuD_C_Growth.txt

    Assumes a base directory that is particular to how I store my experimental
    data. Will need to be changed for each person.

    Assumes dates are stored exactly as shown above.

    """
    year_folder = '20' + filename_base[4:6]
    #file_folder = filename[0:filename.index('.')]
    experimental_folder_path = os.path.join(base_file_dir,
                                            year_folder, filename_base)
    path_excel = os.path.join(experimental_folder_path, filename_base + '.xlsx')
    path_data = os.path.join(experimental_folder_path, filename_base + '.txt')

    return path_data, path_excel, year_folder, filename_base

def import_data(path_to_data):
    """
    Read in data with csv reader.
    Reads it in as a list of lists.
    """
    with open(path_to_data, 'r', encoding = 'ISO-8859-1', newline = '') as f:
        reader = csv.reader(f, delimiter = '\t')
        next(reader)
        data_import = [r for r in reader]
    return data_import

def find_data_starts_breaks(data):
    """
    Data is burried between headers of variable length, and
    footers of variable length.

    However, the bounds for each set of plate reader data is
    marked by a List that starts with Time and is 98 positions
    long, and ends with an empty list. We will use this
    knowldege to find the start and stop positions for each
    dataset.

    data_starts, returns a list of variable length (depending
    on how many wavelengths were monitered) indicating where
    the data starts for each wavelength.

    data_breaks, returns a list of variable length indicating all
    the locations where there are empty lists.
    The empty lists will be used to find the place
    where the data for each wavelength ends.
    """
    count = 0
    data_starts = []
    data_breaks = []
    for line in data:
        if len(line) == 98 and line[0] == 'Time':
            data_starts.append(count)
        if len(line) == 0:
            data_breaks.append(count)
        count += 1
    return data_starts, data_breaks

def find_data_stops(data_starts, data_breaks):
    """
    Takes in all the data start sites, and all the potential
    places where the data would stop, and finds the next empty
    list after a data start site, to define that data's stop
    site.
    """
    data_stop = []
    for start in data_starts:
         for brea in data_breaks:
            if brea > start:
                data_stop.append(brea)
                break
    return data_stop

def find_data_bounds(data):
    """
    Returns a list of lists containing the places where the
    data starts and stops.
    As shown below.

    [[Start1, Start2, Start3], [Stop1, Stop2, Stop3]]
    """
    data_starts, data_breaks = find_data_starts_breaks(data)
    data_stops = find_data_stops(data_starts, data_breaks)
    return data_starts, data_stops

def extract_wavelength_from_multi(wave_string):
    """
    This function is called if multiple wavelengths were meausred
    in a single experiment.

    Returns string with the wavelength used.
    """
    wavelength = re.split(':', wave_string)[1]
    return wavelength

def extract_wavelength_from_single(wave_string):
    """
    This function is called to extract the wavelength used if
    only a single wavelength was measured in the experiment.

    Returns string with the wavelength used.
    """
    wavelength = re.split('\s', wave_string)[1]
    return wavelength

def find_wavelengths(data, data_starts):
    """
    Returns a list of the wavelength(s) measured in an experiment.
    Extraction depends on how many wavelengths were measured in
    and experiment, since the output from the plate reader will change.
    """
    wavelength_info = data[data_starts[0]][1]
    wavelengths_in_exp = []
    for start in data_starts:
        wavelength_info = data[start][1]
        if re.search(':', wavelength_info):
            wavelengths_in_exp.append(extract_wavelength_from_multi(wavelength_info))
        else:
            wavelengths_in_exp.append(extract_wavelength_from_single(wavelength_info))
    return wavelengths_in_exp

def get_list_of_data(data):
    """
    Returns a list of all the data, at this point everything is still exported as a string.
    """
    data_bounds = find_data_bounds(data)
    wavelengths_used = find_wavelengths(data, data_bounds[0])
    print(data_bounds)
    print(wavelengths_used)
    data_all_wavelengths = []
    for i in range(0, len(data_bounds[0])):
        data_all_wavelengths.append(data[data_bounds[0][i]: data_bounds[1][i]])
    return data_all_wavelengths, wavelengths_used

def create_df_index(data_all_wavelengths):
    df_index = data_all_wavelengths[0][0][2:]
    df_index.insert(0, 'time')
    df_index.insert(1, 'temp')
    return df_index

def create_df_all_wavelengths(data_all_wavelengths, wavelengths_used):
    df_index = create_df_index(data_all_wavelengths)
    df = pd.DataFrame(index=df_index)
    for i in range(0, len(data_all_wavelengths)):
        transposed_list = list(zip(*data_all_wavelengths[i][1:]))
        for j in range(2,len(transposed_list)):
            print(float(i))
            print(transposed_list[j])
            transposed_list[j] = [float(i) for i in transposed_list[j]]
        df[wavelengths_used[i]] = transposed_list[0:]
    return df

def to_min(s):
    hr, min, sec = [float(x) for x in s.split(':')]
    return hr*60 + min + sec/60

def convert_timestamp(ts):
    converted_time = []
    for stamp in ts:
        timeCalc = to_min(stamp)
        converted_time.append(timeCalc)
    return converted_time

def create_fig_save_folder(base_file_path, file_name):
    main_output_folder_info = find_data_path(file_name, base_file_path)
    fig_save_path = os.path.join(base_file_path, main_output_folder_info[2], main_output_folder_info[3], 'analysis_figures')
    if not os.path.exists(fig_save_path):
        os.makedirs(fig_save_path)
    return fig_save_path

def drop_excluded_wells(df, well_exclusion_list):
    df_dropped = df.drop(well_exclusion_list)
    return df_dropped

def get_condition_details(df):
    """
    This function will pull out all the conditions for how the 
    experiment was run
    """
    cond_details = []
    unique_values = df['cell'].unique()
    cond_details.append(list(filter(lambda v: v==v, unique_values)))
    return cond_details

def group_conditional_ids(df):
    all_conditions = get_condition_details(df)[0]
    cond_idx = []
    for condition in all_conditions:
        cond_df = df.loc[(df['cell'] == condition)]
        cond_idx.append(cond_df.index.tolist())
    col_names = get_non_cell_col_names(df)
    return cond_idx, all_conditions, col_names

def averageSingleCondition(single_group_data):
    """
    single_group_data should be a list of lists containing all data
    that belongs to a single treatment group.
    """
    averaged_data = [sum(e)/len(e) for e in zip(*single_group_data)] 
    return averaged_data

def stdSingleCondition(single_group_data):
    """
    single_group_data should be a list of lists containing all data
    that belongs to a single treatment group.
    """
    std_data = []
    for e in zip(*single_group_data):
        cntN = len(e)
        avgVal = float(sum(e))/cntN
        std_data.append((sum((i-avgVal)**2 for i in e)/(cntN-1))**0.5)
    return std_data
def get_non_cell_col_names(df):
    col_names = df.columns.values.tolist()
    col_names.remove('cell')
    return col_names

def create_merged_df(merged_list, column_names, well_ids, condition_names):
    df_merged_conditions = pd.DataFrame(merged_list).T
    df_merged_conditions.columns = column_names
    df_merged_conditions['well_id'] = well_ids
    df_merged_conditions['cell'] = condition_names
    df_merged_conditions.set_index('well_id', inplace = True)
    return df_merged_conditions    

def merge_replicates(df):
    condition_ids, condition_names, col_names = group_conditional_ids(df)
      
    all_data_to_merge = []
    first_well_id = []
    condition_name = []
    
    for col_name in col_names:
        condition_data_to_merge = []
        for condition_pair in condition_ids:
            data_for_pairs = []
            for well_id in condition_pair:
                data_for_pairs.append(df.loc[well_id, col_name])
            condition_data_to_merge.append(data_for_pairs)
            condition_name.append(df.loc[condition_pair[0], 'cell'])
            first_well_id.append(condition_pair[0])
        all_data_to_merge.append(condition_data_to_merge)
    df_merged = create_merged_df(all_data_to_merge, col_names, first_well_id, condition_name)
    return df_merged

def rework_df_bio_rep(df):
    df['cell'] = df['cell_type'] + '_' + df['stimulus_type'] + '_' + df['Media'].map(str)
    df.drop(['cell_type', 'cell_biol_replicate_num', 'stimulus_type', 'Media'], axis = 1, inplace=True)
    return df
    
def rework_df(df):
    df['cell'] = df['cell_type'] + '_' + df['cell_biol_replicate_num'] + '_' + df['stimulus_type'] + '_' + df['Media'].map(str)
    df.drop(['cell_type', 'cell_biol_replicate_num', 'stimulus_type', 'Media'], axis = 1, inplace=True)
    return df

def merge_conditions(df, merge_biological_replicates, merge_tech_replicates):
    '''
        Input data frame that already has dropped wells that we dont want to include
        and which already has well data associated.
    '''

    if merge_biological_replicates:
        df = rework_df_bio_rep(df)
        merged_df = merge_replicates(df)
    elif merge_tech_replicates:
        df = rework_df(df)
        merged_df = merge_replicates(df)
    else:
        df = rework_df(df)
        merged_df = df

    return merged_df

def average_merged_dataframe(df):
    column_names = get_non_cell_col_names(df)
    for col_name in column_names:
        if type(df[col_name][0][0]) == list:
            averaged_condition = []
            std_condition = []
            new_col_name_avg = col_name + '_averaged'
            new_col_name_std = col_name + '_std'
            for index, row in df.iterrows():
                averaged_condition.append(averageSingleCondition(row.loc[col_name]))
                std_condition.append(stdSingleCondition(row.loc[col_name]))
            df[new_col_name_avg] = averaged_condition
            df[new_col_name_std] = std_condition
    return df

def make_layout_df(filename_base, base_file_path, wells_to_exclude):
    plate_data_path = find_data_path(filename_base, base_file_path)[1]
    df = pd.read_excel(plate_data_path, sheetname='PlateLayout')
    df['well_id'] = df['row']+ df['col'].map(str)
    df.drop(['row', 'col'], axis = 1, inplace=True)
    df.cell_biol_replicate_num = df.cell_biol_replicate_num.fillna(0).astype(np.int64)
    df.cell_biol_replicate_num = df.cell_biol_replicate_num.astype(str)
    df.set_index('well_id', inplace=True)
    df_d = drop_excluded_wells(df, wells_to_exclude)
    return df_d

def make_merged_df(data_df, filename_base, base_filepath, wells_to_exclude, mer_bio_rep, mer_tec_rep):
    df_layout = make_layout_df(filename_base, base_filepath, wells_to_exclude)
    df_w_data = df_layout.join(data_df, how='outer')
    merged_df = merge_conditions(df_w_data, mer_bio_rep, mer_tec_rep)
    averaged_df = average_merged_dataframe(merged_df)
    return averaged_df

def get_time_axis(df, wavelength):
    time = convert_timestamp(list(df[wavelength].iloc[0]))
    return time

def parse_data_file(filename, base_file_path, wells_to_exclude,
                           merge_bio_rep, merge_tech_rep):
    """
    Should be able to take in a file directly output from the
    Huang lab plate reader, and parse the data and return
    files based on the number of channels read.

    Data is exported as a text file, with non ascci characters.
    """
    data_path = find_data_path(filename, base_file_path)
    imported_data = import_data(data_path[0])
    data_all_waves, waves_used = get_list_of_data(imported_data)
    df = create_df_all_wavelengths(data_all_waves, waves_used)
    time = get_time_axis(df, waves_used[0])
    df_merged = make_merged_df(df, filename, base_file_path, wells_to_exclude,
                           merge_bio_rep, merge_tech_rep)
    return df, df_merged, time