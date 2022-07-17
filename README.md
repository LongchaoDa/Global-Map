
# GlobalMap
GlobalMap by DataShader, to support customized layer to demonstrate different datasets.
=======

## Visualization Demons(zoom in/out)
##### Demo1: weeplace dataset for checkin data (global) 
US part(the image size is limited, so cut into pieces for demonstrating)
![image.png](http://tva1.sinaimg.cn/large/0081frzVly1h49wto7t0hj30ge085ah3.jpg)  
the blow one is or EU:

EU part:
![image.png](http://tva1.sinaimg.cn/large/0081frzVly1h49ww2t5rvj30h40augth.jpg)  
  
China part(the checkin data is spare, which is reasonable because the data is collected from Facebook company)
![image.png](http://tva1.sinaimg.cn/large/0081frzVly1h49wzg5u7dj30h40b3jxn.jpg)  


#### Demo2: New York Taxi trajs and example from datashader
1. Taxi dats in an overall way of terrain
![image.png](http://tva1.sinaimg.cn/large/0081frzVly1h49x876d3uj30qg0nee81.jpg)
2. change the base layer into the openStreetMap to demonstrate the data:
![image.png](http://tva1.sinaimg.cn/large/0081frzVly1h49x94d96wj30pa0mlhdt.jpg)
3. zoom in to see the details match of each streets with data of taxis
 the overlap image is below:
 ![image.png](http://tva1.sinaimg.cn/large/0081frzVly1h49xag1oacj310q0p6npe.jpg)
 to see the comparison, we see the local pure street map of same location:
 ![image.png](http://tva1.sinaimg.cn/large/0081frzVly1h49xd8k07pj310q0p6e81.jpg)
we could clearly observe that the loaction of majority dorpoff places mainly exist in the New York Penn Station
which makes sense.
#### Demo3: The location data in Chicago to separate the communities
1. The comparison of OSM and plotted community cut edges(a series of points)
![image.png](http://tva1.sinaimg.cn/large/0081frzVly1h49xjyoldmj30p60f319y.jpg)
2. A detailed version of split communities
![image.png](http://tva1.sinaimg.cn/large/0081frzVly1h49xkzm3w5j30ug0kpkjl.jpg)

By this, we can clearly observe the separated communities and its boundaries, helpful to study the 
community problems in a relative direct way.

#### An overview of the layers
![image.png](http://tva1.sinaimg.cn/large/0081frzVly1h49x28xzktj31hc0qi4qp.jpg)

## How to build the visualization

```bash
conda env create -f environment.yml
```

The preprocess the _xxx.csv_ file to remove unneeded columns, and to convert the lat/long fields to metres using webm().

```bash
python preprocess.py
```

Generate the tiles as follows:

```bash
python generate_tiles.py
```

Then run a webserver to serve them:

```
python -m http.server 8008
```

And open http://localhost:8008/