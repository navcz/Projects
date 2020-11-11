#!/usr/bin/python3
import pandas as pd
import time
import yaml
from pandas import ExcelWriter
from pandas import ExcelFile

key_status = 0

def edit_yaml(stat_key):
    with open(r'/home/naveen/Desktop/exp/Station-key/config.yaml') as file:
        d = yaml.full_load(file)
        print (d)


station_id_input = input("please enter the station number : ")
stationid = "WMQISXM1V1-" + station_id_input.zfill(5)
df = pd.read_excel('station_key.xlsx', sheet_name='Sheet1')

for i in df['Station ID']:
    if i == stationid:
        key_status = 1

if key_status == 0:
    print ("Key do not exist,Contact Smart Network")
    exit()

for i in df.index:
    #print ("Station ID {} = Station key {}".format(df['Station ID'][i],df['Primary String'][i]))
    if df['Station ID'][i] == stationid:
        print ("Station ID = ",df['Station ID'][i])
        print ("Key = ",df['Primary String'][i])
        key = df['Primary String'][i]

confirm = input("Apply Key [y/n] : ")

if confirm == 'y':
    print ("Enter")
    edit_yaml(key)
else:
    print ("Exit")
    exit()


