---
title: 'NLP-2:图搜索算法和梯度下降'
date: 2019-10-31 10:52:41
categories:
- nlp-自然语言处理
tags:
- nlp-自然语言处理

---

[toc]

# NLP-2:图搜索算法和梯度下降

## 图搜索算法：

- [深度优先搜索(dfs)和广度优先搜索(bfs,也叫层次搜索)]( https://blog.csdn.net/xyqqwer/article/details/81255634 )原理这篇博文很不错，可以快速入门

### 我不会讲理论，直接从项目开始理解吧

- 资源

  ```python
  coordination_source = """
  {name:'兰州', geoCoord:[103.73, 36.03]},
  {name:'嘉峪关', geoCoord:[98.17, 39.47]},
  {name:'西宁', geoCoord:[101.74, 36.56]},
  {name:'成都', geoCoord:[104.06, 30.67]},
  {name:'石家庄', geoCoord:[114.48, 38.03]},
  {name:'拉萨', geoCoord:[102.73, 25.04]},
  {name:'贵阳', geoCoord:[106.71, 26.57]},
  {name:'武汉', geoCoord:[114.31, 30.52]},
  {name:'郑州', geoCoord:[113.65, 34.76]},
  {name:'济南', geoCoord:[117, 36.65]},
  {name:'南京', geoCoord:[118.78, 32.04]},
  {name:'合肥', geoCoord:[117.27, 31.86]},
  {name:'杭州', geoCoord:[120.19, 30.26]},
  {name:'南昌', geoCoord:[115.89, 28.68]},
  {name:'福州', geoCoord:[119.3, 26.08]},
  {name:'广州', geoCoord:[113.23, 23.16]},
  {name:'长沙', geoCoord:[113, 28.21]},
  //{name:'海口', geoCoord:[110.35, 20.02]},
  {name:'沈阳', geoCoord:[123.38, 41.8]},
  {name:'长春', geoCoord:[125.35, 43.88]},
  {name:'哈尔滨', geoCoord:[126.63, 45.75]},
  {name:'太原', geoCoord:[112.53, 37.87]},
  {name:'西安', geoCoord:[108.95, 34.27]},
  //{name:'台湾', geoCoord:[121.30, 25.03]},
  {name:'北京', geoCoord:[116.46, 39.92]},
  {name:'上海', geoCoord:[121.48, 31.22]},
  {name:'重庆', geoCoord:[106.54, 29.59]},
  {name:'天津', geoCoord:[117.2, 39.13]},
  {name:'呼和浩特', geoCoord:[111.65, 40.82]},
  {name:'南宁', geoCoord:[108.33, 22.84]},
  //{name:'西藏', geoCoord:[91.11, 29.97]},
  {name:'银川', geoCoord:[106.27, 38.47]},
  {name:'乌鲁木齐', geoCoord:[87.68, 43.77]},
  {name:'香港', geoCoord:[114.17, 22.28]},
  {name:'澳门', geoCoord:[113.54, 22.19]}
  """
  ```

- 我们要把这个文件中的城市和地址区分开来,可以先看一看正则表达式，用法可以百度，我这里只是讲使用**因为我写这个示例的时候使用的jupyter所以我的导包对下面的都有用，以后就不再导包了**

  ```python
  import re
  #导入包
  l =  "color and colour"
  pattern = re.compile("colou?r")
  pattern.findall(l)
  输出:
      ['color', 'colour']
  
  ```

- 在上述基础上我们写出函数并运行

  ```python
  def get_city_info(city_coordination):
      city_location = {}
      for line in city_coordination.split("\n"):
              if line.startswith("//"):continue
              if line.strip()=="": continue
              # find city
              city = re.findall("name:'(\w+)'",line)[0]#分离出城市
              x_y = re.findall("Coord:\[(\d+.\d+),\s(\d+.\d+)\]",line)[0]#分离出经纬度
              print(x_y)
              x_y = tuple(map(float,x_y))
              city_location[city] = x_y;
      return city_location
  city_info = get_city_info(coordination_source)
  输出：
  {'兰州': (103.73, 36.03),
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
  ```

- 工具类：测量两个城市之间的距离

  ```python
  import math
  
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
  #写一个判断两个城市的距离
  def get_city_distance(city1,city2):
      return geo_distance(city_info[city1],city_info[city2]);
  get_city_distance("杭州","上海")
  输出
  153.5185697155768
  
  ```

- 将城市图画出来

  ```python
  import networkx as nx
  import matplotlib.pyplot as plt
  #导入字体库，并设置
  plt.rcParams['font.sans-serif'] = ['SimHei']
  plt.rcParams['axes.unicode_minus'] = False
  city_graph = nx.Graph()
  
  city_graph.add_nodes_from(list(city_info.keys()))
  nx.draw(city_graph,city_info,with_labels=True,node_size=10)
  ```

  运行结果

 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191031124254186.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjQ3OTE1NQ==,size_16,color_FFFFFF,t_70)

- 构建后继节点连接图，这里我们定义一个规则，距离在700以内的是可以相互连接的

  ```python
  threshold = 700 #define the threshold
  from collections import defaultdict
  def build_connection(city_info):
      cities_connection = defaultdict(list)
      cities = list(city_info.keys())
      for c1 in cities:
          for c2 in cities:
              if c1==c2:continue
              if get_city_distance(c1,c2) < threshold:#判断距离，如果距离小于700那么就是连接的，可以添加到后继节点网络
                  cities_connection[c1].append(c2)
      return cities_connection
  cities_connection = build_connection(city_info)
  结果：
  defaultdict(list,
              {'兰州': ['嘉峪关', '西宁', '成都', '拉萨', '贵阳', '西安', '重庆', '南宁', '银川'],
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
                '香港']})
  ```

- 将这个图谱画出来：

  ```python
  print(type(cities_connection))
  cities_connection_graph = nx.Graph(cities_connection)
  print(cities_connection_graph)
  nx.draw(cities_connection_graph,city_info,with_labels=True,node_size=10)
  ```

  ![\[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-suDgg478-1572496918946)(C:\Users\admin\Desktop\201911301112.png)\]](https://img-blog.csdnimg.cn/201910311243214.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjQ3OTE1NQ==,size_16,color_FFFFFF,t_70)

- 第一个bfs算法，寻找最短路径，这里的最短路径是上面的后继节点哈，不是距离

  ```python
  def bfs(graph,start,destination):
      pathes = [[start]]
      visited = set()
      while pathes:
          path = pathes.pop(0)
          froniter = path[-1]
          if froniter in visited:continue
          successors = graph[froniter]
          for city in successors:
              if city in path: continue #check up
              new_path = path + [city]
              print(new_path)
              pathes.append(new_path)
              if city == destination:
                  return new_path
          visited.add(froniter)#存储访问过的节点
  测试：
  bfs(cities_connection,"上海","香港")
  ['上海', '济南']
  ['上海', '南京']
  ['上海', '合肥']
  ['上海', '杭州']
  ['上海', '南昌']
  ['上海', '福州']
  ['上海', '沈阳']
  ['上海', '天津']
  ['上海', '济南', '石家庄']
  ['上海', '济南', '武汉']
  ['上海', '济南', '郑州']
  ['上海', '济南', '南京']
  ['上海', '济南', '合肥']
  ['上海', '济南', '杭州']
  ['上海', '济南', '南昌']
  ['上海', '济南', '福州']
  ['上海', '济南', '长沙']
  ['上海', '济南', '太原']
  ['上海', '济南', '北京']
  ['上海', '济南', '天津']
  ['上海', '济南', '呼和浩特']
  ['上海', '南京', '石家庄']
  ['上海', '南京', '武汉']
  ['上海', '南京', '郑州']
  ['上海', '南京', '济南']
  ['上海', '南京', '合肥']
  ['上海', '南京', '杭州']
  ['上海', '南京', '南昌']
  ['上海', '南京', '福州']
  ['上海', '南京', '长沙']
  ['上海', '南京', '北京']
  ['上海', '南京', '天津']
  ['上海', '合肥', '石家庄']
  ['上海', '合肥', '武汉']
  ['上海', '合肥', '郑州']
  ['上海', '合肥', '济南']
  ['上海', '合肥', '南京']
  ['上海', '合肥', '杭州']
  ['上海', '合肥', '南昌']
  ['上海', '合肥', '福州']
  ['上海', '合肥', '广州']
  ['上海', '合肥', '长沙']
  ['上海', '合肥', '太原']
  ['上海', '合肥', '北京']
  ['上海', '合肥', '天津']
  ['上海', '合肥', '香港']
  ['上海', '合肥', '香港']
  ```

- dfs:最快速的寻找一条路径，但是和距离没有关系，只是图的搜素最快而已

  ```python
  def dfs(graph,start,destination):
      pathes = [[start]]
      visited = set()
      while pathes:
          path = pathes.pop(0)
          froniter = path[-1]
          if froniter in visited:continue
          successors = graph[froniter]
          for city in successors:
              if city in path: continue #check up
              new_path = path + [city]
              #print(path)
              pathes = [new_path]+pathes
              #print(pathes) Keep adding small paths in, and the longer the path is in front
              if city == destination:
                  print(pathes)
                  return new_path
          visited.add(froniter)#保存访问过的节点
   dfs(cities_connection,"拉萨","北京")
  输出:
      ['拉萨', '银川', '南宁', '澳门', '香港', '长沙', '北京']
  ```

- 第二个bfs这里是距离最短的，里面嵌套了一个排序，同时把visited给取消了

  ```python
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
  
              pathes = search_strategy(pathes)
              # visit add
              if pathes and pathes[0][-1] == destination:# 这条路径经过重排序之后是最短的，
                  print(pathes)
                  print("--------------------------------------")
                  return pathes[0]
              #这里不能使用visited因为假设g在这条路径最后，但是这条路径不一定是最短的，并且这样会导致g被压入visited，从而永远也找不到目标
  def sort_by_distance(pathes):
      def get_distance_of_path(path):
          distance = 0
          for i,_ in enumerate(path[:-1]):
              distance += get_city_distance(path[i],path[i+1])
          return distance
      return sorted(pathes,key=get_distance_of_path)
  bfs_2(cities_connection,"北京","上海",search_strategy=sort_by_distance)
  ['北京', '天津', '上海']
  ```

## 梯度下降算法(线行回归)

- 目标函数:$$ y = k*rm + b$$

- 定义损失函数：

  $$ \frac{\partial{loss}}{\partial{k}} = -\frac{2}{n}\sum(y_i - \hat{y_i})x_i$$

  $$ \frac{\partial{loss}}{\partial{b}} = -\frac{2}{n}\sum(y_i - \hat{y_i})$$

- 定义损失函数计算：

  ```python
  # define loss function 
  def loss(y,y_hat):
      return sum((y_i - y_hat_i)**2 for y_i, y_hat_i in zip(list(y),list(y_hat)))/len(list(y))
  ```

- 定义梯度

  ```python
  # define partial derivative 
  def partial_derivative_k(x, y, y_hat):
      n = len(y)
      gradient = 0
      for x_i, y_i, y_hat_i in zip(list(x),list(y),list(y_hat)):
          gradient += (y_i-y_hat_i) * x_i
      return -2/n * gradient
  
  def partial_derivative_b(y, y_hat):
      n = len(y)
      gradient = 0
      for y_i, y_hat_i in zip(list(y),list(y_hat)):
          gradient += (y_i-y_hat_i)
      return -2 / n * gradient
  ```

- 这里的代码完全是按照上面数学公式来写的

- 总的使用函数，工具函数

  ```python
  #initialized parameters
  
  k = random.random() * 200 - 100  # -100 100
  b = random.random() * 200 - 100  # -100 100
  
  learning_rate = 1e-3
  
  iteration_num = 200 
  losses = []
  for i in range(iteration_num):
      
      price_use_current_parameters = [price(r, k, b) for r in X_rm]  # \hat{y}
      
      current_loss = loss(y, price_use_current_parameters)
      losses.append(current_loss)
      print("Iteration {}, the loss is {}, parameters k is {} and b is {}".format(i,current_loss,k,b))
      
      k_gradient = partial_derivative_k(X_rm, y, price_use_current_parameters)
      b_gradient = partial_derivative_b(y, price_use_current_parameters)
      
      k = k + (-1 * k_gradient) * learning_rate
      b = b + (-1 * b_gradient) * learning_rate
  best_k = k
  best_b = b
  ```

- 画出损失函数图像

  ```python
  plt.plot(list(range(iteration_num)),losses)
  ```

  ![\[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-GIqcBb3j-1572496918949)(C:\Users\admin\Desktop\201910311128.png)\]](https://img-blog.csdnimg.cn/20191031124342652.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjQ3OTE1NQ==,size_16,color_FFFFFF,t_70)

- 将拟合图像画出来

  ```python
  #define target function
  def price(rm, k, b):
      return k * rm + b
  price_use_best_parameters = [price(r, best_k, best_b) for r in X_rm]
  
  plt.scatter(X_rm,y)
  plt.scatter(X_rm,price_use_current_parameters)
  ```

   ![\[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-ZnBga8mH-1572496918950)(C:\Users\admin\Desktop\201910311130.png)\]](https://img-blog.csdnimg.cn/20191031124354674.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjQ3OTE1NQ==,size_16,color_FFFFFF,t_70)