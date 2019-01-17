import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

def find_data_path(filename, base_file_dir):
    """
    If it is not already so, make sure the filename and the enclosing
    folder have the same name.
    i.e. /121118_UmuD_C_Growth/121118_UmuD_C_Growth.txt

    Assumes a base directory that is particular to how I store my experimental
    data. Will need to be changed for each person.

    Assumes dates are stored exactly as shown above.

    """
    year_folder = '20' + filename[4:6]
    file_folder = filename[0:filename.index('.')]
    experimental_folder_path = os.path.join(base_file_dir,
                                            year_folder, file_folder, filename)

    return experimental_folder_path, year_folder, file_folder

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
    data_all_wavelengths = []
    for i in range(0, len(data_bounds[0])):
        data_all_wavelengths.append(data[data_bounds[0][i]: data_bounds[1][i]])
    return data_all_wavelengths, wavelengths_used

def create_df_index(data_all_wavelengths):
    df_index = data_all_wavelengths[0][0][2:]
    df_index.insert(0, 'time')
    df_index.insert(1, 'temp')
    return df_index

def create_df_all_wavelengths(data_all_wavelengths, wavelenths_used):
    df_index = create_df_index(data_all_wavelengths)
    df = pd.DataFrame(index=df_index)
    for i in range(0, len(data_all_wavelengths)):
        transposed_list = list(zip(*data_all_wavelengths[i][1:]))
        df[wavelengths_used[i]] = transposed_list[0:]
    return df

def parse_data_file(filename):
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
    fig_save_path = os.path.join(base_file_path, main_output_folder_info[1], main_output_folder_info[2], 'analysis_figures')
    if not os.path.exists(fig_save_path):
        os.makedirs(fig_save_path)
    return fig_save_path