import json
import os
import numpy as np
import pandas as pd
from datashader.utils import lnglat_to_meters as webm
import re
import geopandas
import utils.geojson as geo
from shapely import geometry

# with open('data/inaturalist.csv', 'w') as f:
#     f.write('x,y\n')
#     for chunk in pd.read_csv("data/observations.csv", chunksize=10000):
#         txt = ''
#         for lng, lat in zip(chunk['decimalLongitude'], chunk['decimalLatitude']):
#             txt += "%s,%s\n" % webm(lng, lat)
#         f.write(txt)
# writein_file = "data/checkins/gowalla/pure_gowalla_spots_subset1.csv"
# original_file = "data/checkins/gowalla/gowalla_spots_subset1.csv"

# writein_file = "data/coast/pure_coast1.csv"
# original_file = "data/coast/coast1.csv"

# all types for airports
# ['balloonport', 'closed', 'heliport', 'large_airport', 'medium_airport', 'seaplane_base', 'small_airport']
# writein_file = "data/airport2017/details/new/newairport.csv"
# original_file = "data/airport2017/details/new/airports.csv"

writein_file = "data/globalport/pure_globalport.csv"
original_file = "data/globalport/globalports.geojson"


# writein_file = "data/city8k/GHS_STAT_UCDB2015MT_GLOBE_R2019A/pure8k.csv"
# original_file = "data/city8k/GHS_STAT_UCDB2015MT_GLOBE_R2019A/GHS_STAT_UCDB2015MT_GLOBE_R2019A_V1_2.csv"

def pre_process(wri, ori):
    with open(wri, 'w') as f:
        f.write('x,y\n')
        counter = 0
        for chunk in pd.read_csv(ori, chunksize=10000):
            counter += 1

            # chunksize(file chuncks, to process the files base on the smaller pieces)
            txt = ''
            # taxi:
            # for lng, lat in zip(chunk['dropoff_x'], chunk['dropoff_y']):

            # checkin:
            # for lng, lat in zip(chunk['lon'], chunk['lat']):

            for info, value in zip(chunk['the_geom_4326'], chunk['ann_dpf']):
                lng, lat = re.findall(r'[(](.*?)[)]', info)[0].split(" ")
                # print(lng+","+lat)
                lng = float(lng)
                lat = float(lat)
                temp = webm(lng, lat)
                if np.isfinite(temp[0]) and np.isfinite(temp[1]):
                    txt += "%s,%s\n" % temp
                else:
                    print(lng)
                    print(lat)
            print("-----finished" + str(counter) + "------")
            f.write(txt)


# os.makedirs(writein_file)
def process_csv_file(wri, ori):
    with open(wri, 'w', encoding='utf-8') as f:
        f.write('x,y\n')
        counter = 0
        for chunk in pd.read_csv(ori, chunksize=10000):
            counter += 1

            # chunksize(file chuncks, to process the files base on the smaller pieces)
            txt = ''
            # taxi:
            # for lng, lat in zip(chunk['dropoff_x'], chunk['dropoff_y']):

            # checkin:
            for lng, lat in zip(chunk['lon'], chunk['lat']):
                # for lng, lat in zip(chunk['Longitude'], chunk['Latitude']):
                temp = webm(lng, lat)
                if np.isfinite(temp[0]) and np.isfinite(temp[1]):
                    txt += "%s,%s\n" % temp
                else:
                    print(lng)
                    print(lat)
            print("-----finished" + str(counter) + "------")
            f.write(txt)


def process_geojson_file(wri, ori):
    with open(ori, mode='r', encoding='utf-8') as f:
        # try:
        data = json.load(f)
        features = data['features']  # 6584 [:]['geometry']['coordinates']
        print(data)
        length = len(features)
        global order_data
        for i in range(length):
            t = features[i]['geometry']['coordinates'][0][0]
            temp = np.array(t)
            # print(temp.shape)
            if i == 0:
                order_data = temp
            else:
                order_data = np.concatenate((order_data, temp), axis=0)
            # print(order_data.shape)
        # print(order_data.shape)
        # x: long, y: lat
        # print("--------------------------")
        with open(wri, 'w') as w:
            w.write('x,y\n')
            txt = ''
            counter = 0
            for lng, lat in order_data:
                counter += 1
                temp = webm(lng, lat)
                if np.isfinite(temp[0]) and np.isfinite(temp[1]):
                    txt += "%s,%s\n" % temp
                else:
                    print(lng)
                    print(lat)
            print("-----finished" + str(counter) + "------")
            w.write(txt)
            # except:
            #     print('文件格式不正确，读取失败。')

def process_geojson_file_for_port(wri, ori):
    with open(ori, mode='r', encoding='utf-8') as f:
        # try:
        data = json.load(f)
        features = data['features']  # 6584 [:]['geometry']['coordinates']
        print(data)
        length = len(features)
        global order_data
        counter = 0
        for i in range(length):
            t = features[i]['geometry']['coordinates']
            temp = np.array([t])
            print(temp)
            # print(temp.shape)
            if i == 0:
                order_data = temp
            else:
                order_data = np.concatenate((order_data, temp), axis=0)
            # print(order_data.shape)
            counter += 1
        print(order_data)
        print("total_num:"+str(counter))
        # x: long, y: lat
        # print("--------------------------")
        with open(wri, 'w') as w:
            w.write('x,y\n')
            txt = ''
            counter = 0
            for lng, lat in order_data:
                counter += 1
                temp = webm(lng, lat)
                if np.isfinite(temp[0]) and np.isfinite(temp[1]):
                    txt += "%s,%s\n" % temp
                else:
                    pass
                    # print(lng)
                    # print(lat)
            # print("-----finished" + str(counter) + "------")
            # w.write(txt)
            # except:
            #     print('文件格式不正确，读取失败。')


def ij_to_latlon(x, y):
    x = 90 - x * 0.02
    y = -180 + y * 0.02
    return x, y


def add_title(wri, ori):
    with open(wri, 'w', encoding='utf-8') as f, open(ori, 'r', encoding='utf-8') as f2:
        f.write('lat,lon,val\n')
        f.write(f2.read())


def process_ziyang_csv_file(wri, ori):
    with open(wri, 'w', encoding='utf-8') as f:
        f.write('x,y\n')
        counter = 0
        for chunk in pd.read_csv(ori, chunksize=10000):
            counter += 1

            # chunksize(file chuncks, to process the files base on the smaller pieces)
            txt = ''
            # taxi:
            # for lng, lat in zip(chunk['dropoff_x'], chunk['dropoff_y']):

            # checkin:
            for lat, lng in zip(chunk['lat'], chunk['lon']):
                la, ln = ij_to_latlon(lat, lng)
                # for lng, lat in zip(chunk['Longitude'], chunk['Latitude']):
                temp = webm(ln, la)
                if np.isfinite(temp[0]) and np.isfinite(temp[1]):
                    txt += "%s,%s\n" % temp
                else:
                    print(lng)
                    print(lat)
            print("-----finished" + str(counter) + "------")
            f.write(txt)


'''
read csv_file
'''
# process_csv_file(writein_file, original_file)

'''
read geojson_file
'''
process_geojson_file_for_port(writein_file, original_file)

'''
pre_process_coast:
'''

# add_title(writein_file, original_file)
# process_ziyang_csv_file(writein_file, original_file)
