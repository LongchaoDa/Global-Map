import pandas as pd
import re
import csv
import sys
import numpy as np
from datashader.utils import lnglat_to_meters as webm

base_path = r"F:\PythonFiles\workspace\CityBrain\visualization\inaturalist-datashader-map\data\airport2017"
path = base_path + '/airport.csv'

df = pd.read_csv(path)
df.describe()

address = pd.read_csv(path, usecols=[12])  # 提取想要的数据列，0是列索引
df3 = np.unique(address)
print(df3)

address_pured = pd.read_csv(path, usecols=[6, 7, 12])
address_pured.head()

writein_airport = base_path + './details/pureair.csv'
writein_station = base_path + './details/purestation.csv'
writein_port = base_path + './details/pureport.csv'
writein_others = base_path + './details/pureothers.csv'
with open(writein_airport, "w") as ap, open(writein_station, "w") as sta, open(writein_port, "w") as pt, open(
        writein_others, "w") as oth:
    ap.write('x,y,type\n')
    sta.write('x,y,type\n')
    pt.write('x,y,type\n')
    oth.write('x,y,type\n')
    for i in range(len(address_pured)):
        txt = ''
        lng, lat = address_pured.iloc[i]['lng'], address_pured.iloc[i]['lat']
        temp = webm(lng, lat)
        input = temp[0], temp[1], address_pured.iloc[i]['Column13']
        if np.isfinite(temp[0]) and np.isfinite(temp[1]):
            txt += "%s,%s,%s\n" % input
        else:
            print(lng)
            print(lat)

        if address_pured.iloc[i]['Column13'] == 'airport':
            print(address_pured.iloc[i])
            ap.write(txt)
        elif address_pured.iloc[i]['Column13'] == 'port':
            pt.write(txt)
        elif address_pured.iloc[i]['Column13'] == 'station':
            sta.write(txt)
        else:
            oth.write(txt)

        print("finished")
