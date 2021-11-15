# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:01:22 2021

@author: user
"""

import os
import numpy as np
from openpyxl import load_workbook

#########################################

station_path = '/media/ubuntu/My Passport/NCDR/ncdr_rain_predict/data/station_data'


special_station_input_id = ['C0V250','C0R140']


#########################################


print("[INFO] loading special station")


tmp_special_stations = []
data_special_stations = []

for year in os.listdir(station_path):
    #print(file)
    year_dir = station_path + "/" + year
    for month in os.listdir(year_dir):
        month_dir = year_dir + "/" + month
        for date in os.listdir(month_dir):
            date_dir = month_dir + "/" + date
            for date_file in os.listdir(date_dir):
                if not date_file.endswith(".txt"):
                    #break
                    continue
                time = int(date_file[-6:-4])
                if time >11:
                    continue
                file_name = date_file
                date_txt = date_dir + "/" + date_file
                #print(date_txt)
                f = open(date_txt)
                
                stations = []
                lons = []
                lats = []
                elevs = []
                temps = []
                huminitys = []
                wind_directions = []
                
                for line in f.readlines():
                    line = line.replace("-", " -")
                    parsing = line.split()
                    if parsing[0] not in special_station_input_id:
                        continue
                    else:
                        # parsing append list
                        stations.append(parsing[0])
                        lons.append(float("{:.2f}".format(float(parsing[1]))))
                        lats.append(float("{:.2f}".format(float(parsing[2]))))
                        #elevs.append(float("{:.4f}".format(float(parsing[3]))))
                        elevs.append(float(parsing[3]))
                
                        temps.append(float(parsing[5]))
                
                        huminitys.append((float(parsing[6])))
                        wind_directions.append((float(parsing[7])))
                        
                for num in range(len(stations)):
                    tmp_special_stations.append([huminitys[0],temps[0],wind_directions[0]])
                data_special_stations.append(tmp_special_stations)
                tmp_special_stations = []
data_special_stations = np.array(data_special_stations)
data_special_stations = np.reshape(data_special_stations,(-1,station_time,len(special_station_input_id)*3))
print("number of videos: ", data_special_stations.shape)