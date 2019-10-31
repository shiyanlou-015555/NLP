---
title: NLP-lesson2作业
date: 2019-10-29 10:41:15
categories:
- nlp-自然语言处理
tags:
- nlp-自然语言处理
---

[toc]

# NLP-lesson2作业

## 理论部分

- **What conditions are required to make the BFS return the optimal solution**  (使用bfs返回最佳解决方案需要什么条件？)

  1. All costs between two nodes are positive or zero.
  2. Sort the list used to maintain the searching history in every iteration.

- **Is there a way to make DFS find the optimal solution ? (You may need to read some material about iterative DFS)**(有没有办法使DFS找到最佳解决方案？ （您可能需要阅读一些有关迭代DFS的材料)

  No,I don't think so ,DFS is used to find a solution fastly,it is mean a solution ,it is not necessarily the optimal solution

- **In what conditions BFS is a better choice than DFS and vice versa **(在什么情况下BFS比DFS更好，反之亦然)

  1. The branch factor is relatively small.
  2. The depth o the optimal solution is relatively shallow.

- **When can we use machine learning ?**(什么时候我们可以用机器学习)

  When we use data to learn a model that has good performance on unseen data. Machine learning can solve two types of questions--regression and classification.

- **What is the gradient of a function ?**(什么是函数梯度)

  The fastest decline in function

- **How can we find the maximum value of a function using the information of gradient ?**(我们如何使用信息找到函数最大值)

  reverse this function,find minimum value of the changed function,and then reverse it back.

## 实践1：寻找地铁路线

- 详细解释在旁边一个md文件内

  ```python
  import requests
  from bs4 import BeautifulSoup
  import json
  """
  目标：爬取中国大陆地铁线路信息
  要求：
  	①获取相关城市的地铁数量
  	②获取每个地铁站的名称
  	③写入文档
  
  """
  
  class Subway(object):
      def __init__(self):
          # 构造url
          self.url = "http://map.amap.com/subway/index.html?&1100"
          # 使用老版本请求头
          self.headers = {
              'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
          }
      # 获取数据
      def get_data(self):
          responses = requests.get(url=self.url, headers=self.headers)
          # 返回str字符串类型
          return responses.text
      # 解析每个城市地铁信息(地铁数量，站点)
      def parse_get_subway(self, ID, city, name):
          # 拼接地铁信息的url
          url = 'http://map.amap.com/service/subway?_1555502190153&srhdata=' + ID + '_drw_' + city + '.json'
          print(url)
          # 获取数据
          response = requests.get(url=url, headers=self.headers)
          # 传递一个参数接收返回的字符串类型
          html = response.text
          # 通过json.loads将json字符串类型转为python数据类型
          result = json.loads(html)
          # 循环遍历数据节点，所有地铁路线
          for node in result['l']:
              # "st"为地铁线的站点
              for start in node['st']:
  
                  # 判断是否含有地铁分线
                  # node:"l"里包含所有地铁路线  “la”为分线
                  if len(node['la']) > 0:
                      # "ln"为1号线，2号线。。。  “n”为地铁站站名
                      print(name, node['ln'] + '(' + node['la'] + ')', start['n'])
  
                      with open('subway.json', 'a+', encoding='utf8') as f:
  
                          f.write(name + ',' + node['ln'] + '(' + node['la'] + ')' + ',' + start['n'] + '\n')
  
                  else:
  
                      print(name, node['ln'], start['n'],start['sl'])
  
                      with open('subway.json', 'a+', encoding='utf8') as f:
  
                          f.write(node['ln'] + ',' + start['n'] + ',['+start['sl']+']\n')
      # 解析数据
      def parse_city_data(self, data):
          # 对数据进行编码
          data = data.encode('ISO-8859-1')
          data = data.decode('utf-8')
          soup = BeautifulSoup(data, 'lxml')
  
          # 获取城市信息
          res1 = soup.find_all(class_="city-list fl")[0].find_all('a')
          ID = res1[0]['id']
          city_name = res1[0]['cityname']
          name = res1[0].get_text()
          self.parse_get_subway(ID,city_name,name)
          #res2 = soup.find_all(class_="more-city-list")[0]
          # 遍历a标签
          # for temp in res1.find_all('a'):
          #     # 城市ID值
          #     ID = temp['id']
          #     # 城市拼音名
          #     city_name = temp['cityname']
          #     # 城市名
          #     name = temp.get_text()
          #     self.parse_get_subway(ID, city_name, name)
  
         # for temp in res2.find_all('a'):
         #      # 城市ID值
         #      ID = temp['id']
         #      # 城市拼音名
         #      city_name = temp['cityname']
         #      # 城市名
         #      name = temp.get_text()
         #      self.parse_get_subway(ID, city_name, name)
  
  
      def run(self):
          data =self.get_data()
          self.parse_city_data(data)
  
  
  if __name__ == '__main__':
      subway = Subway()
      subway.run()
  
  ```

## 实践部分2：bfs：最短距离

- 举例：奥体中心到天安门东

  ```python
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
  ```

## 实践3：寻找换乘最少的

- 例子：奥体中心到天安门东

  ```python
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
  #得到所有路径结果
  
  def bfs_3(graph,start,destination):
      """
  This bfs query can be understood as the shortest transfer query，得到节点最少的路径
      :param graph: the connection of diagram
      :param start: the starting point
      :param destination: the destination
      :return:
      """
      pathes = [[start]]
      result = []
      while len(result)<20:
          path = pathes.pop(0)
          froniter = path[-1]
          successors = graph[froniter]
          for city in successors:
              if city in path:continue# if city in the path means to check up
              new_path = path+[city]
              #print(new_path)
              pathes.append(new_path)# add new path but it is not the shortest distance but to the minimum node distance
              if city==destination:
                  print(new_path)
                  if new_path not in result:
                      result.append(new_path)
                  pathes.remove(new_path)
      return list(result)
  
  #print(bfs_3(stations_connection,"奥体中心","天安门东"))
  line_list = bfs_3(stations_connection,"奥体中心","天安门东")
  #print(line_list)
  #工具方法
  def get_keys(d, value):
      return [k for k,v in d.items() if v == value]
  #进行换线统计
  def line_static(line_name,line_list):
      """
      This code is for changing line statistics
      :param line_name:
      :param line_list:
      :return:
      """
      result = []
      set = {1,}
      new_pathes = []
      print(len(line_name))
      while len(result)<20:
          for line_list_line in line_list:
              for line_list_line_station in line_list_line:
                  for line_name_line in line_name.values():
                      # print(line_list_line.index(line_list_line_station)+1)
                      if line_list_line.index(line_list_line_station)+1 == len(line_list_line):
                          break
                      if line_list_line_station in line_name_line and line_list_line[line_list_line.index(line_list_line_station)+1] in line_name_line:#如果这个站和下个站是同一个线路那么就是对的了
                          # print(get_keys(line_name,line_name_line))
                          if str(get_keys(line_name,line_name_line)) not in set:
                              new_pathes.append(get_keys(line_name,line_name_line))
                              set.add(str(get_keys(line_name,line_name_line)))
                              break
              result.append(new_pathes)
              print(new_pathes)
              new_pathes = []
              set.clear()
      return result
  #print(line_static(lines_name,line_list))
  line_list_statistic = sorted(line_static(lines_name,line_list),key=lambda i:len(i))
  print(line_list_statistic[0])
  
  ```

## 实践4：比较两种选最好的

- 最近的：['奥体中心', '北土城', '安华桥', '安德里北街', '鼓楼大街', '什刹海', '南锣鼓巷', '东四', '灯市口', '东单', '王府井', '天安门东']
- 最少换乘的：['奥体中心', '北土城', '安华桥', '安德里北街', '鼓楼大街', '安定门', '雍和宫', '东直门', '东四十条', '朝阳门', '建国门', '东单', '王府井', '天安门东']
- 看个人喜好

