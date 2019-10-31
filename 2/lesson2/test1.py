import networkx as nx
import math
cities_connection = {'兰州': ['嘉峪关', '西宁', '成都', '拉萨', '贵阳', '西安', '重庆', '南宁', '银川'],
             '嘉峪关': ['兰州', '西宁', '成都', '拉萨'],
             '西宁': ['兰州', '嘉峪关', '成都', '拉萨', '贵阳', '重庆', '银川'],
             '成都': ['兰州', '嘉峪关', '西宁', '拉萨', '贵阳', '西安', '重庆', '南宁', '银川'],
             '石家庄': ['武汉',
              '郑州',
              '济南',
              '南京',
              '合肥',
              '南昌',
              '广州',
              '长沙',
              '太原',
              '西安',
              '北京',
              '天津',
              '呼和浩特'],
             '拉萨': ['兰州', '嘉峪关', '西宁', '成都', '贵阳', '重庆', '南宁', '银川'],
             '贵阳': ['兰州', '西宁', '成都', '拉萨', '西安', '重庆', '南宁', '银川'],
             '武汉': ['石家庄',
              '郑州',
              '济南',
              '南京',
              '合肥',
              '杭州',
              '南昌',
              '福州',
              '广州',
              '长沙',
              '太原',
              '西安',
              '北京',
              '天津',
              '呼和浩特',
              '香港',
              '澳门'],
             '郑州': ['石家庄',
              '武汉',
              '济南',
              '南京',
              '合肥',
              '南昌',
              '广州',
              '长沙',
              '太原',
              '西安',
              '北京',
              '天津',
              '呼和浩特',
              '香港',
              '澳门'],
             '济南': ['石家庄',
              '武汉',
              '郑州',
              '南京',
              '合肥',
              '杭州',
              '南昌',
              '福州',
              '长沙',
              '太原',
              '北京',
              '上海',
              '天津',
              '呼和浩特'],
             '南京': ['石家庄',
              '武汉',
              '郑州',
              '济南',
              '合肥',
              '杭州',
              '南昌',
              '福州',
              '长沙',
              '北京',
              '上海',
              '天津'],
             '合肥': ['石家庄',
              '武汉',
              '郑州',
              '济南',
              '南京',
              '杭州',
              '南昌',
              '福州',
              '广州',
              '长沙',
              '太原',
              '北京',
              '上海',
              '天津',
              '香港',
              '澳门'],
             '杭州': ['武汉', '济南', '南京', '合肥', '南昌', '福州', '北京', '上海', '天津'],
             '南昌': ['石家庄',
              '武汉',
              '郑州',
              '济南',
              '南京',
              '合肥',
              '杭州',
              '福州',
              '广州',
              '长沙',
              '太原',
              '北京',
              '上海',
              '天津',
              '香港',
              '澳门'],
             '福州': ['武汉',
              '济南',
              '南京',
              '合肥',
              '杭州',
              '南昌',
              '广州',
              '上海',
              '香港',
              '澳门'],
             '广州': ['石家庄',
              '武汉',
              '郑州',
              '合肥',
              '南昌',
              '福州',
              '长沙',
              '太原',
              '西安',
              '南宁',
              '香港',
              '澳门'],
             '长沙': ['石家庄',
              '武汉',
              '郑州',
              '济南',
              '南京',
              '合肥',
              '南昌',
              '广州',
              '太原',
              '西安',
              '北京',
              '天津',
              '呼和浩特',
              '南宁',
              '香港',
              '澳门'],
             '沈阳': ['长春', '哈尔滨', '上海'],
             '长春': ['沈阳', '哈尔滨'],
             '哈尔滨': ['沈阳', '长春'],
             '太原': ['石家庄',
              '武汉',
              '郑州',
              '济南',
              '合肥',
              '南昌',
              '广州',
              '长沙',
              '西安',
              '北京',
              '天津',
              '呼和浩特',
              '银川',
              '澳门'],
             '西安': ['兰州',
              '成都',
              '石家庄',
              '贵阳',
              '武汉',
              '郑州',
              '广州',
              '长沙',
              '太原',
              '重庆',
              '呼和浩特',
              '南宁',
              '银川'],
             '北京': ['石家庄',
              '武汉',
              '郑州',
              '济南',
              '南京',
              '合肥',
              '杭州',
              '南昌',
              '长沙',
              '太原',
              '天津',
              '呼和浩特'],
             '上海': ['济南', '南京', '合肥', '杭州', '南昌', '福州', '沈阳', '天津'],
             '重庆': ['兰州', '西宁', '成都', '拉萨', '贵阳', '西安', '呼和浩特', '南宁', '银川'],
             '天津': ['石家庄',
              '武汉',
              '郑州',
              '济南',
              '南京',
              '合肥',
              '杭州',
              '南昌',
              '长沙',
              '太原',
              '北京',
              '上海',
              '呼和浩特'],
             '呼和浩特': ['石家庄',
              '武汉',
              '郑州',
              '济南',
              '长沙',
              '太原',
              '西安',
              '北京',
              '重庆',
              '天津',
              '银川'],
             '南宁': ['兰州',
              '成都',
              '拉萨',
              '贵阳',
              '广州',
              '长沙',
              '西安',
              '重庆',
              '银川',
              '香港',
              '澳门'],
             '银川': ['兰州',
              '西宁',
              '成都',
              '拉萨',
              '贵阳',
              '太原',
              '西安',
              '重庆',
              '呼和浩特',
              '南宁'],
             '香港': ['武汉', '郑州', '合肥', '南昌', '福州', '广州', '长沙', '南宁', '澳门'],
             '澳门': ['武汉',
              '郑州',
              '合肥',
              '南昌',
              '福州',
              '广州',
              '长沙',
              '太原',
              '南宁',
              '香港']}

city_info = {'兰州': (103.73, 36.03),
 '嘉峪关': (98.17, 39.47),
 '西宁': (101.74, 36.56),
 '成都': (104.06, 30.67),
 '石家庄': (114.48, 38.03),
 '拉萨': (102.73, 25.04),
 '贵阳': (106.71, 26.57),
 '武汉': (114.31, 30.52),
 '郑州': (113.65, 34.76),
 '济南': (117.0, 36.65),
 '南京': (118.78, 32.04),
 '合肥': (117.27, 31.86),
 '杭州': (120.19, 30.26),
 '南昌': (115.89, 28.68),
 '福州': (119.3, 26.08),
 '广州': (113.23, 23.16),
 '长沙': (113.0, 28.21),
 '沈阳': (123.38, 41.8),
 '长春': (125.35, 43.88),
 '哈尔滨': (126.63, 45.75),
 '太原': (112.53, 37.87),
 '西安': (108.95, 34.27),
 '北京': (116.46, 39.92),
 '上海': (121.48, 31.22),
 '重庆': (106.54, 29.59),
 '天津': (117.2, 39.13),
 '呼和浩特': (111.65, 40.82),
 '南宁': (108.33, 22.84),
 '银川': (106.27, 38.47),
 '乌鲁木齐': (87.68, 43.77),
 '香港': (114.17, 22.28),
 '澳门': (113.54, 22.19)}
def bfs_2(graph, start, destination, search_strategy):
    pathes = [[start]]
    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]
        successors = graph[froniter]
        for city in successors:
            if city in path: continue
            new_path = path + [city]
            pathes.append(new_path)

        pathes = search_strategy(pathes)
        # visit add
        if pathes and pathes[0][-1] == destination:  # 这条路径经过重排序之后是最短的，
            print(pathes)
            print("--------------------------------------")
            return pathes[0]
# 地点距离
def geo_distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    # >>> origin = (48.1372, 11.5756)  # Munich
    # >>> destination = (52.5186, 13.4083)  # Berlin
    # >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d
#写一个判断两个城市的距离
def get_city_distance(city1,city2):
    return geo_distance(city_info[city1],city_info[city2]);
#对长度进行排序
def sort_by_distance(pathes):
    def get_distance_of_path(path):
        distance = 0
        for i,_ in enumerate(path[:-1]):
            distance += get_city_distance(path[i],path[i+1])
        return distance
    return sorted(pathes,key=get_distance_of_path)
bfs_2(cities_connection,"北京","上海",search_strategy=sort_by_distance)
#--------------------------------------------------------------------
'''
对上面的理解，假如目的地是G，假设第一次是AB AD AF AG
从前依次向后排序那么第一次BFS遍历的就是以AB为基础扩展,假设
AD AF AG ABG ABH
显然可以观察到，在这种情况下，是会出现AG越来越向前，最后通过比较最后一个是G而得到输出
'''


def bfs_3(graph, start, destination, search_strategy):
 # 这是个有问题的
    pathes = [[start]]
    visited = set()
    while pathes:
        #print(pathes[0])
        path = pathes.pop(0)
        froniter = path[-1]
        if '香港' in visited:
            pass
        if froniter in visited: continue
        successors = graph[froniter]
        for city in successors:
           if city in path: continue
           new_path = path + [city]
           pathes.append(new_path)

        pathes = search_strategy(pathes)
        print(pathes[0])
  # visit add
        if pathes and pathes[0][-1] == destination:  # 这条路径经过重排序之后是最短的，
   #                 print(pathes)
   #                 print("--------------------------------------")
            return pathes[0]
        visited.add(froniter)
bfs_3(cities_connection,"上海","香港",search_strategy=sort_by_distance)#寻找不到路径