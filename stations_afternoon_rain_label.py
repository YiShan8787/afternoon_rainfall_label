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


#special_station_input_id = ['C0R140']

#south
special_station_input_id = [
    
    '467410','467420','467780','CAN010','CAN020',
    'CAN030','CAN040','CAN050','CAN060','CAN070',
    'CAN080','CAN090','CAN100',
    
    'C0X100','C0X110','C0X310','CM0130','C0X060',
    'C0O860','C0X180','C0X160','C0O840','C0X290',
    'C0X210','C0X020','C0X240','C0X300','C0X200',
    'C0O930','C0X190','C0X150','C0O950','C0X140',
    'C0X080','C0X130','C0X050','C0O830','C0X260',
    'C0X270','C0X320','C0X280','C0X120','C0O900',
    'C0O970','C0O980','C0O910','C0X250','C0O810',
    'C0X220','C0O960','C0O990','C0X170','C0X230',
    
    '467440','467400','CAP010',
    'CAP020','CAP030','CAP040','CAP050','CAP060',
    
    'C0V700','C0V770','C0V730','C0V350','C0V450',
    'C0V680','C0V360','C0V800','C0V810','C0V620',
    'C0V370','C0V250','C0V820','C0V260','C0V150',
    'C0V660','C0V720','C0V530','C0V310','C0V630',
    'C0V790','CM0180','C0V710','C0V210','C0V610',
    'C0V640','C0V490','C0V490','C0V670','C0V750',
    'C0V690','C0V740','C0V500','C0V440','C0V760',
    'C0V400','C0V650',
    
    '467590','467790','CAQ010','CAQ020',
    
    'C0R170','C0R590','C0R100','C0R150','C0R500',
    'C0R650','C1R340','C0R340','C0R720','C0R750',
    'C0R790','C0R830','C0R420','C0R840','C0R590',
    'C0R540','C0R400','C0R670','C0R700','C0R380',
    'C0R660','C0R640','C0R430','CM0160','C0R530',
    'C0R480','C0R580','C0R350','C0R690','C0R360',
    'C0R620','C0R710','C0R730','C0R260','C0R440',
    'C1R440','C0R520','C0R600','C0R720','C0R470',
    'C0R550','C0R560','C0R510','C0R240','C0R190',
    'C0R220','C0R280','C0R370','C0R680','C0R760',
    'C0R780','C0R140','C0R130','C0R570','C0R160',
    'C1R320','C0R770','C0R740','C0R800','C0R810',
    'C0R820'
    ]


#########################################


print("[INFO] loading special station")


wb = Workbook()
sheet = wb.create_sheet("daily_afternoon_rainfall", 0)
count_true = 0
count_false = 0

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
            stations_list = []
            for date_file in os.listdir(date_dir):
                if not date_file.endswith(".txt"):
                    #break
                    continue
                time = int(date_file[-6:-4])
                is_morning = 0
                is_afternoon = 0
                is_night = 0
                #morning: 6~11
                if time <12 and time>5:
                    is_morning = 1
                #night: 18~23
                if time <24 and time >17:
                    is_night = 1
                # afternoon: 12~18
                if time <19 and time >11:
                    is_afternoon = 1
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
                                    if station not in stations_list:
                                        stations_list.append(station)
                                else:
                                    stations_morning_rain[station] += stations_morning_rain[station]
                            if is_afternoon:
                                if stations_afternoon_rain.get(station) == None:
                                    stations_afternoon_rain[station] = tmp_water
                                    if station not in stations_list:
                                        stations_list.append(station)
                                else:
                                    stations_afternoon_rain[station] += stations_afternoon_rain[station]
                            if is_night:
                                if stations_night_rain.get(station) == None:
                                    stations_night_rain[station] = tmp_water
                                    if station not in stations_list:
                                        stations_list.append(station)
                                else:
                                    stations_night_rain[station] += stations_night_rain[station]
                
            all_larger = 1
            
            for station_id in stations_list:
                
                if stations_afternoon_rain[station_id] < stations_morning_rain[station_id] + stations_night_rain[station_id]:
                    
                    all_larger = 0
                    break
            
            if all_larger:
                print("1")
                count_true+=1
                sheet.append([date,1])
            else:
                print("0")
                count_false+=1
                sheet.append([date,0])
                
wb.save(Result)
print(count_true)
print(count_false)