# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:01:22 2021

@author: user
"""

import os
import numpy as np
from openpyxl import load_workbook

#########################################

station_path = '/media/ubuntu/My Passport/NCDR/Data/station_data'

Result = 'Result/daily_rain.xlxs'

min_rain = 0

thresh_hold = 50


special_station_input_id = ['C0V250','C0R140']


#########################################


print("[INFO] loading special station")


tmp_special_stations = []
data_special_stations = []

date_dic = {}

for year in os.listdir(station_path):
    #print(file)
    year_dir = station_path + "/" + year
    for month in os.listdir(year_dir):
        month_dir = year_dir + "/" + month
        for date in os.listdir(month_dir):
            date_dir = month_dir + "/" + date
            afternoon_rainfall = 0
            stations_daily_rain = {}
            for date_file in os.listdir(date_dir):
                if not date_file.endswith(".txt"):
                    #break
                    continue
                time = int(date_file[-6:-4])
                if time <11:
                    continue
                file_name = date_file
                date_txt = date_dir + "/" + date_file
                print(date_txt)
                f = open(date_txt)
                
                station = -1
                
                tmp_water = -1
                
                
                
                for line in f.readlines():
                    line = line.replace("-", " -")
                    parsing = line.split()
                    if parsing[0] not in special_station_input_id:
                        continue
                    else:
                        # parsing append list
                        station = parsing[0]
                        tmp_water= float(parsing[9])
                        if tmp_water<min_rain:
                            tmp_water = min_rain
                        
                        if station in special_station_input_id:
                            if stations_daily_rain.get(station) == None:
                                stations_daily_rain[station] = tmp_water
                            else:
                                stations_daily_rain[station] += stations_daily_rain[station]
                
            all_larger = 1
            
            for station_id in stations_daily_rain:
                if stations_daily_rain[station_id] < thresh_hold:
                    
                    all_larger = 0
                    break
            
            if all_larger:
                print("1")
            else:
                print("0")
                
                
