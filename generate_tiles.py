import json
import os
import sys
import dask.dataframe as dd
import colorcet as cc
from colorcet import bmw, \
    kbc, \
    fire, \
    gray, \
    dimgray, \
    CET_D11, \
    CET_D8, \
    kgy, \
    cwr, CET_L18, kr, bmw, CET_I1, CET_CBTL3, CET_CBTL4, CET_CBL4, CET_L18

import dask
import pandas as pd
import datashader as ds
from datashader import transfer_functions as tf
from datashader.utils import lnglat_to_meters as webm
from datashader_fix.tiles import \
    render_tiles  # use version of render tiles with this fix: https://github.com/holoviz/datashader/pull/874
import datashader.transfer_functions as tf
import datashader as ds
import spatialpandas as sp
import geopandas

# The threads scheduler is more efficient than the multiprocessor one (which is the default for dask.bag)
# See https://docs.dask.org/en/latest/setup/single-machine.html
dask.config.set(scheduler='threads')

# cmap = cc.isolum

zoom_min = 1
zoom_max = 5
mode = 'point'
# mode = 'polygon'

# out_path = 'tileDic/world_city4w'

# --------------------------------------------------------------
# --------------------------------------------------------------
# color_list = ['#e1d656', '#e1dc77', '#e1dc82', '#f2f1b6']
# read_path = "./data/airport2017\details/pureair.csv"
# out_path = 'tileDic/detailports/pureair'

# color_list = ['#c20434','#ca0637','#dd0739', '#ea093a']
# read_path = "./data/airport2017\details/pureport.csv"
# out_path = 'tileDic/detailports/pureport'

# color_list = ['#00ffff']
# read_path = "./data/airport2017\details/purestation.csv"
# out_path = 'tileDic/detailports/purestation'

# color_list = ['#ffffff']
# read_path = "./data/airport2017\details/pureothers.csv"
# out_path = 'tileDic/detailports/pureothers'
# ------------------------------------------------------------------
# ------------------------------------------------------------------

'''
By Prof.ZhengGuanJie, Su ZiYang
'''
# color_list = ['#bebebe', '#c7c7c7', '#cfcfcf', '#d8d8d8', '#dedede', '#ebebeb', '#efefef', '#f4f4f4', '#f7f7f7',
#               '#f9f9f9', '#ffffff']
# read_path = "./data/ziyang/pure_ziyang_osm.csv"
# out_path = 'tileDic/ziyang/ziyang_osm'
# ------------------------------------------------------------------
# ------------------------------------------------------------------

# color_list = ['#2db9fc', '#2dd8fa', '#2de8fa', '#2df8fa', '#7ff8fa', '#8ff8fa', '#9ff8fa', '#aff8fa', '#bff8fa', '#cff8fa', '#eff8fa', '#fff8fa', '#fffffa']
# read_path = "./data/city8k/GHS_STAT_UCDB2015MT_GLOBE_R2019A/pure8k.csv"
# out_path = 'tileDic/city8k/pure8k'

# light blue color
# color_list = ['#a89e60', '#fcffe9']


# color_list = ['#2db9fc', '#2dd8fa', '#2de8fa', '#2df8fa', '#7ff8fa', '#8ff8fa', '#9ff8fa', '#aff8fa', '#bff8fa', '#cff8fa', '#eff8fa', '#fff8fa', '#fffffa']
# read_path = "./data/ziyang/pure_osm_node_counting.csv"
# out_path = 'tileDic/ziyang/newosm'


# global ports in the map
color_list = ['#cc3b2e', '#f10205', '#f9071e','#ff0018', '#ff0948', '#ff0a38', '#ff0b18', '#ff0d18', '#ffc1c5', '#ffcacb']
# color_list = ['#cc3b2e', '#cc372c', '#dc3b2f', '#dc3b2f', '#e83d31', '#ef3c32', '#f43c32', '#f93c32', '#fd3c32', '#fd594a', '#fd9a7c', '#fd8f8f', '#f10205']
read_path = "./data/globalport/pure_globalport.csv"
out_path = 'tileDic/globalport'

# read_path = "./data/coast/pure_coast1.csv"
# out_path = 'tileDic/population2'

# read_path = "./data/coast/pure_coast1.csv"
# out_path = 'tileDic/coast'

# read_path = "./data/fuel_station/pure_fuel_station.csv"
# out_path = 'tileDic/fuel_station'

# read_path="./data/taxi/pure_taxi.csv"
# out_path="tileDic/nyTaxiTile"

# read_path="./data/checkins/gowalla/pure_gowalla_spots_subset1.csv"
# out_path="tileDic/gowallacheckin1"

# read_path="./data/checkins/gowalla/pure_gowalla_spots_subset2.csv"
# out_path="tileDic/gowallacheckin2"

# read_path = "./data/checkins/weeplaces/pure_weeplace_checkins.csv"
# out_path="tileDic/weeplacecheckin"

# read_path = "./data/yunke/3.csv"
# out_path="tileDic/chicago"

cmap = color_list
# cmap = cc.kbc
df = pd.read_csv(read_path)

if mode == 'point':
    def get_extents(df, x, y):
        return df[x].min(), df[y].min(), df[x].max(), df[y].max()


    def load_data_func(x_range, y_range):
        return df.loc[df['x'].between(*x_range) & df['y'].between(*y_range)]


    def rasterize_func(df, x_range, y_range, height, width):

        cvs = ds.Canvas(x_range=x_range, y_range=y_range,
                        plot_height=height, plot_width=width)
        agg = cvs.points(df, 'x', 'y')
        return agg


    def shader_func(agg, span=None):
        img = tf.shade(agg, cmap=cmap)
        # img = tf.set_background(tf.shade(agg,  cmap=cmap), "black")
        return img


    def post_render_func(img, **kwargs):
        return img


    if __name__ == '__main__':
        # output_path = 'tileDic/nyTaxiTile'
        output_path = out_path
        if os.path.exists(output_path) == False:
            os.makedirs(output_path)
        full_extent_of_data = get_extents(df, 'x', 'y')
        print("full_extent_of_data:")
        print(full_extent_of_data)
        results = render_tiles(full_extent_of_data,
                               range(zoom_min, zoom_max),
                               load_data_func=load_data_func,
                               rasterize_func=rasterize_func,
                               shader_func=shader_func,
                               post_render_func=post_render_func,
                               output_path=output_path)

elif mode == 'polygon':

    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    # world = world.to_crs(epsg=4087)  # simple cylindrical projection
    world = world.to_crs(epsg=4087)  # simple cylindrical projection
    world['boundary'] = world.geometry.boundary
    world['centroid'] = world.geometry.centroid
    df_world = sp.GeoDataFrame(world)
    full_extent_data = (-9901010.655423956, 4973554.289976041, -9676931.310942153, 5261862.382069691)


    def get_extents(df, x, y):
        return df[x].min(), df[y].min(), df[x].max(), df[y].max()


    def load_data_func(x_range, y_range):
        return df.loc[df['x'].between(*x_range) & df['y'].between(*y_range)]


    def rasterize_func(df, x_range, y_range, height, width):
        cvs = ds.Canvas(plot_height=height, plot_width=width)
        # agg = cvs.polygons(df_world, geometry='geometry', agg=ds.mean('gdp_md_est'))
        agg = cvs.polygons(df_world, geometry='geometry', agg=ds.mean('pop_est'))
        return agg


    def shader_func(agg, span=None):
        # img = tf.shade(agg, cmap=cc.CET_L18)
        img = tf.shade(agg, cmap=cc.blues)
        return img


    def post_render_func(img, **kwargs):
        return img


    if __name__ == '__main__':
        # output_path = 'tileDic/nyTaxiTile'
        output_path = out_path

        if os.path.exists(output_path) == False:
            os.makedirs(output_path)
        full_extent_of_data = get_extents(df, 'x', 'y')
        results = render_tiles(full_extent_data,
                               range(zoom_min, zoom_max),
                               load_data_func=load_data_func,
                               rasterize_func=rasterize_func,
                               shader_func=shader_func,
                               post_render_func=post_render_func,
                               output_path=output_path)
    # python -m http.server 8008
