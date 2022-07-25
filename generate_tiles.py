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
    CET_D11,\
    CET_D8, \
    kgy, \
    cwr, CET_L18, kr, bmw, CET_I1
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
cmap = CET_I1
zoom_min = 1
zoom_max = 5
# mode = 'point'
mode = 'polygon'


read_path = "./data/world_city4w/pure_worldcities.csv"
# out_path = 'tileDic/world_city4w'
out_path = 'tileDic/test'

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