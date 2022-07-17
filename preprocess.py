import json
import os
import numpy as np
import pandas as pd
from datashader.utils import lnglat_to_meters as webm
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

writein_file = "data/yunke/3.csv"
original_file = "data/yunke/3.geojson"


# os.makedirs(writein_file)
def process_csv_file(wri, ori):
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
            for lng, lat in zip(chunk['lng'], chunk['lat']):
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


'''
read csv_file
'''
# process_csv_file(writein_file, original_file)

'''
read geojson_file
'''
process_geojson_file(writein_file, original_file)
