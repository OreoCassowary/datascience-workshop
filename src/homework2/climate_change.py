# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 16:56:59 2017
"""

# climate change project

#files required:
    
# 1)data.csv => contains 
#    -station ID => Index[0]
#    -temperature => Index[3]

# 2)site_detail.csv => contains:
#    -station ID => Index[0]
#    -Latitude => Index[2]
#    -Longitude => Index[3]
#    -Country => Index[9]

# open both files, skip forward until header
# skip header

# read data.csv => dict {station ID: [temperature]}
# read site_detail =>dict {station ID: [lat, long, country]

# merge files {station ID, [temp, lat, long, country]


import csv
from pprint import pprint
from collections import Counter
from math import log, trunc
# station_ID_dict contains key=station_ID, value=[lat, lon, country]
station_ID_dict = dict()
debug = False

def make_station_ID_dict(infile='site_detail.csv'):
    '''
    read data from infile, create station_ID_dict {station_ID: [lat, lon, country]}
    infile = filename
    returns station_ID_dict
    '''
    station_ID_dict = dict()

    with open('site_detail.csv') as sitefile:
        site_detail_reader = csv.reader(sitefile, delimiter=';', quotechar='"')

        
        for row in site_detail_reader:

            if row[0][0] == '%':
                continue
            station_ID = int(row[0])
            latitude = float(row[2])
            longitude = float(row[3])
            country = row[8].rstrip()
            
            station_ID_dict[station_ID] = station_ID_dict.get(station_ID, [latitude, longitude, country])
        if debug:
            print(station_ID_dict)
        return station_ID_dict

def make_measurement_freq_file(station_ID_dict, outfile='station measurement frequency.csv', datafile='data.csv'):    
    """
    counts nr of measurements and temperature from infile and writes it in outfile
    input station_ID_dict, outfile, datafile
    returns dict {station_ID: {year: measurements}}
    """
    temp_measurements = dict()

    outfile = open('station measurement frequency.csv', "w", newline='')
         
    with open('data.csv') as datafile:
        data_reader = csv.reader(datafile, delimiter=';', quotechar='"')
        data_writer = csv.writer(outfile, delimiter=',', quotechar='"')  
        data_writer.writerow(['station_ID', 'num of measurements 1961-2000', 'lat', 'lon'])
    
        new_count = 0
        temp_counter = Counter()
        
        for row in data_reader:
            if row[0][0] == '%':
                continue   # skip header     
                
            station_ID = int(row[0])
            year = trunc(float(row[2]))
            temperature = float(row[3])
            if station_ID not in temp_measurements:
                temp_measurements[station_ID] = {year: []}
            elif year not in temp_measurements[station_ID]:
                temp_measurements[station_ID].update({year: []})
            # temp_measurements = {station_ID: {year: [temperature measurements]}}
            temp_measurements[station_ID][year].append(temperature)
            
            temp_counter[station_ID]  += 1 # maybe unecessary

#   # write station ID and number of measurements in csv file     
    
        for sid, l in station_ID_dict.items():
            count = log(1+temp_counter[sid])/log(480)*480
            data_writer.writerow([sid, count, station_ID_dict[sid][0],  station_ID_dict[sid][1] ])
        if debug:
            pprint(temp_measurements)

        
    outfile.close()

    if debug:
        print(f'unable to convert {new_count} items')
        
    return temp_measurements
        
def calc_avg(measurements_dict):
    """
    sum up temperature values per station per year and calculates temp average
    returns {station_ID: {year: average}}
    """
    temp_averages = dict()
    for station in measurements_dict.keys():
        
        for year in measurements_dict[station].keys():
            L = measurements_dict[station][year]
            if len(L) != 0:
                average = sum(L)/len(L)
            else:
                average = float('NaN')
            # temp_averages = {station_ID: {year: average}}
            if station not in temp_averages:
                temp_averages[station] = {year: None}
            elif year not in temp_averages[station]:
                temp_averages[station].update({year: None})
            temp_averages[station][year] = average
    if debug:
        pprint(temp_averages)
    return temp_averages
    
    
def write_station_year_avg_file(measurements_dict):
    """
    writes csv output file containing the yearly average temperature measurement / station
    return None
    """

    with open('station_year_avg.csv', "w", newline='') as f:
        data_writer = csv.writer(f, delimiter=',', quotechar='"')
        data_writer.writerow(['station_ID', 'year', 'average temperature'])

        for station_ID, _v in measurements_dict.items():
            for year, average in _v.items():
                data_writer.writerow([station_ID, year, average])


                



if __name__ == '__main__':
    station_ID_dict = make_station_ID_dict()
    temp_measurements = make_measurement_freq_file(station_ID_dict)
    temp_avg = calc_avg(temp_measurements)
    write_station_year_avg_file(temp_avg)
