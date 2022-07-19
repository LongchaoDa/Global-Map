import json
import os
import sys
import dask.dataframe as dd
import colorcet as cc
from colorcet import bmw, kbc, fire, gray, dimgray
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

cmap = gray
zoom_min = 1
zoom_max = 5
mode = 'point'
# mode = 'polygon'
# read_path="./data/taxi/pure_taxi.csv"
# read_path = "./data/checkins/weeplaces/pure_weeplace_checkins.csv"
read_path = "./data/airport2017/pure_airport.csv"
out_path = 'tileDic/airport2017'
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
        img = tf.shade(agg, cmap=cmap, how='log', span=span)
        return img


    def post_render_func(img, **kwargs):
        return img


    if __name__ == '__main__':
        # output_path = 'tileDic/nyTaxiTile'
        output_path = out_path
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
        agg = cvs.polygons(df_world, geometry='geometry', agg=ds.mean('gdp_md_est'))
        return agg


    def shader_func(agg, span=None):
        img = tf.shade(agg, cmap=cc.CET_L18)
        return img


    def post_render_func(img, **kwargs):
        return img


    if __name__ == '__main__':
        # output_path = 'tileDic/nyTaxiTile'
        output_path = out_path
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