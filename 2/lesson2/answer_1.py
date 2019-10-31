import re
import math

def geo_distance(origin, destination):# 这个方法是通过经纬度得到两个站之间距离
    """
    Get distance by latitude and longitude
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
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
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

with open('subway.json',encoding='utf-8') as f:#这个是打开json进行数据读取
    l = f.readlines()
    print(l[0])

def get_station_info(station_lists:list):#这个是把每个站的站名称和经纬度组合
    """
    try to settle the list and Assembled into a dictionary
    station_name ： latitude and longitude
    :param station_lists:
    :return:
    """
    station_location = {}
    for line in station_lists:
        station = re.findall("\,(\w+)\,",line)[0]
        x_y = re.findall("\,\[(\d+.\d+),(\d+.\d+)\]",line)[0]
        # print(station)
        # print(x_y)
        x_y = tuple(map(float,x_y))
        # map(function, iterable, ...)
        # map() 会根据提供的函数对指定序列做映射。
        # 第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表
        station_location[station] = x_y
    return station_location
station_info = get_station_info(l)#把每个站和经纬度结合
#写一个判断两个城市的距离
def get_station_distance(station1,station2):
    return geo_distance(station_info[station1],station_info[station2])
#画图看看
import networkx as nx
import matplotlib.pyplot as plt
#导入字体库，并设置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
station_info.keys()
station_graph = nx.Graph()
station_graph.add_nodes_from(list(station_info.keys()))
nx.draw(station_graph,station_info,with_labels=True,node_size=10)
plt.show()#展示节点图
# 写connetion
from collections import defaultdict
def get_station_connect(station_lists:list):
    """
    This function is to build a communication diagram.
    事实上是为了搞清楚每条线路上面有多少个站：得到形式's1线': ['金安桥', '四道桥', '桥户营', '上岸', '栗园庄', '小园', '石厂']
    :param station_lists:
    :return:
    """
    lines_name = defaultdict(list)
    station_namelist = []
    # print(station_lists)
    for line in station_lists:
        # print(line)
        line_name = re.findall("(\w+)\,",line)[0]#切割线路
        station = re.findall("\,(\w+)\,",line)[0]#切割站点
        station_namelist.append(station)
        if station in lines_name.keys():
            lines_name[line_name].append(station)
        else:
            lines_name[line_name].append(station)
        # print(station)
        # print(station)
        # print(x_y)
        # x_y = tuple(map(float,x_y))
        # map(function, iterable, ...)
        # map() 会根据提供的函数对指定序列做映射。
        # 第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表
        # station_location[station] = x_y
    # return station_location
    # print(set(station_namelist))
    # print(lines_name.values())
    return lines_name,set(station_namelist)
#创建后继节点网络
def build_connection(lines_name,station_namelist):
    """
    try to build a communication diagram and node and successor of this node
    比如：'经海路': ['同济南路', '次渠南'], '朱辛庄': ['育知路', '巩华城', '生命科学园'],
    :param lines_name:
    :param station_namelist:
    :return:
    """
    station_connection = defaultdict(list)
    station = list(station_namelist)
    for c1 in station:
        for c2 in lines_name.values():
            if c1 in c2:#原理是因为我是在同一个线路里面顺序爬取的
                #如果这个站在这个线路里面那么它的前一个和后一个就是这个站的后继节点
                # print(c1)
                # print(c2)
                i = c2.index(c1)
                # print(i)
                if(i-1>0):
                    station_connection[c1].append(c2[i-1])
                if(i<len(c2)-1):
                    station_connection[c1].append(c2[i+1])
    # print(station_connection)
    return station_connection
lines_name,station_namelist = get_station_connect(l)#获得线路的值
# print(lines_name)
stations_connection = build_connection(lines_name,station_namelist)#构建后继节点
# print(type(stations_connection))
print(lines_name)
print(stations_connection)
stations_connection_graph = nx.Graph(stations_connection)
print(stations_connection_graph)
nx.draw(stations_connection_graph,station_info,with_labels=True)
# plt.show()
# bfs-2这个是为了找到距离最短的
def bfs_2(graph,start,destination,search_strategy):
    pathes = [[start]]
    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]
        successors = graph[froniter]
        for city in successors:
            if city in path: continue
            new_path = path+[city]
            pathes.append(new_path)
        #pathe
        pathes = search_strategy(pathes)# 进行排序
        # there is no doubt that we don't need the visit set ,if you want to know please open the test.py an see why I think so
        if pathes and pathes[0][-1] == destination:
            print(pathes)
            print("---------------------------------------")
            return pathes[0]
# sort_by_distance 设计是为了排序的
def sort_by_distance(pathes):
    def get_distance_of_path(path):
        distance = 0;
        for i,_ in enumerate(path[:-1]):
            distance += get_station_distance(path[i],path[i+1])
        return distance
    return sorted(pathes,key=get_distance_of_path)
print(bfs_2(stations_connection,"奥体中心","天安门东",sort_by_distance))