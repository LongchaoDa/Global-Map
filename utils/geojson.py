class GeoJson():
    import json

    # 基本模板
    Base = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::3857"}},
        "features": [
        ]
    }


'''
如果生成的GEOJSON无法识别，请将"FeatureCollection"替换为"GeometryCollection"，"features"替换为"geometries"。
'''


# 定义参考系
def __init__(self, crs={}):
    if crs is not {}:
        self.Base.crs = crs


# 被打印的方法
def __str__(self):
    return self.json.dumps(self.Base)


# 被迭代的方法
def __iter__(self):
    return self.Base['features']


# 返回元素数量
def __len__(self):
    return len(self.Base["features"])


# 保存JSON文件
def save(self, filename: str):
    with open(filename, mode='w', encoding='utf-8') as f:
        self.json.dump(self.Base, ensure_ascii=False, fp=f)


# 读取JSON文件
def read(self, filename: str):
    with open(filename, mode='r', encoding='utf-8') as f:
        try:
            data = self.json.load(f)
            self.Base['features'] = data['features']
            if 'crs' in data:
                self.Base['crs'] = data['crs']
            return self.Base
        except:
            print('文件格式不正确，读取失败。')


# 添加要素，私有方法
def __add(self, type: str, coordinates: list, properties={}):
    Feature = {
        "type": "Feature",
        "properties": properties,
        "geometry": {
            "type": type,
            "coordinates": coordinates
        }
    }
    self.Base['features'].append(Feature)


# 添加点要素
def addPoint(self, coordinates: list, properties={}):
    if len(coordinates) == 2:
        self.__add('Point', coordinates, properties)


# 添加线要素
def addLineString(self, coordinates: list, properties={}):
    if len(coordinates) >= 2:
        self.__add('LineString', coordinates, properties)


# 添加面要素
def addPolygon(self, coordinates: list, properties={}):
    if len(coordinates) >= 3:
        self.__add('Polygon', coordinates, properties)


# 合并图层
def merge(self, another):
    try:
        for item in another:
            self.Base['features'].append(item)


    except:
        print('合并图层失败')


pass