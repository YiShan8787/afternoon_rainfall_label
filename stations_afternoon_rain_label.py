"""
Created on Mon Nov 15 16:01:22 2021

@author: user
"""

import os
import numpy as np
from openpyxl import load_workbook, Workbook

#########################################

station_path = '/media/ubuntu/My Passport/NCDR/Data/station_data'

Result = 'Result/afternoon_rain.xlsx'

min_rain = 0


special_station_input_id = ['C0R140']


#########################################


print("[INFO] loading special station")


wb = Workbook()
sheet = wb.create_sheet("daily_afternoon_rainfall", 0)

for year in os.listdir(station_path):
    #print(file)
    year_dir = station_path + "/" + year
    for month in os.listdir(year_dir):
        month_dir = year_dir + "/" + month
        for date in os.listdir(month_dir):
            date_dir = month_dir + "/" + date
            afternoon_rainfall = 0
            stations_morning_rain = {}
            stations_afternoon_rain = {}
            stations_night_rain = {}
            for date_file in os.listdir(date_dir):
                if not date_file.endswith(".txt"):
                    #break
                    continue
                time = int(date_file[-6:-4])
                is_morning = 0
                is_afternoon = 0
                is_night = 0
                if time <12 and time>5:
                    is_morning = 1
                if time <24 and time >17:
                    is_night = 1
                if time <19 and time >11:
                    is_afternoon
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
                            
                            if is_morning:
                                if stations_morning_rain.get(station) == None:
                                    stations_morning_rain[station] = tmp_water
                                else:
                                    stations_morning_rain[station] += stations_morning_rain[station]
                            if is_afternoon:
                                if stations_afternoon_rain.get(station) == None:
                                    stations_afternoon_rain[station] = tmp_water
                                else:
                                    stations_afternoon_rain[station] += stations_afternoon_rain[station]
                            if is_night:
                                if stations_night_rain.get(station) == None:
                                    stations_night_rain[station] = tmp_water
                                else:
                                    stations_night_rain[station] += stations_night_rain[station]
                
            all_larger = 1
            
            for station_id in special_station_input_id:
                print(stations_morning_rain[station_id])
                print(stations_afternoon_rain[station_id])
                print(stations_night_rain[station_id])
                if stations_afternoon_rain[station_id] < stations_morning_rain[station_id] + stations_night_rain[station_id]:
                    
                    all_larger = 0
                    break
            
            if all_larger:
                print("1")
                sheet.append([date,1])
            else:
                print("0")
                sheet.append([date,0])
                
wb.save(Result)