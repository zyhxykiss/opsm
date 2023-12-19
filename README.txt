1. 文件构成
在项目中包含一些文件夹，这些文件夹中包含了不同功能的python文件或者其它支持文件:
1). OPSM和OptOPSM中包含了OPSM相关的脚本；
2). BEACON和OptBEACON中包含了BEACON相关的脚本；
3). Stochastic中包含了随机方法相关的python脚本；
4). Reviewer文件夹中包含了使用线性价值函数的脚本；
5). map文件夹中包含了构建校园地图、任务地图和随机生成用户的脚本；
6). Config中包含了各个脚本中使用的参数配置；
7). document文件夹中包含了各种支持文件和实验结果，document中的CSV文件为数字化后的校园地图和任务地图。

2. 数据集说明
在本项目中，poi点从网格化后的云南大学地图中选取，云南大学网格化中代码在map/data_map_generation.py中实现，并且每间隔50米选取一个poi点，然后，在map/task_map_generation.py中生成了每个poi点的权重及其最大访问次数(rm)与价值(vm)，生成的结果以csv形式的文件保存在document文件中。
对于用户数据来源，我们首先使用问卷的方式获取了500余份数据，然后根据文件结果仿真生成虚拟用户，实现生成虚拟用户的文件为map/individual_probability_map.py，生成的文件位于document/probability中(我们提供了200个虚拟用户的demo)。


3. 运行文件
在项目文件夹中包含了一些以mian.py结尾的文件，这些文件用来实现在改变不同变量的情况下的各种算法：

1). Opsm算法：
改变用户数量：opsm_main.py
改变预算：opsm_main_budget.py
改变poi点的数量：opsm_main_poi.py

2). BEACON算法：
改变用户数量：beacon_main.py
改变预算：beacon_main_budget.py
改变poi点的数量：beacon_main_poi.py

3). 随机算法：
改变用户数量：stoch_main.py
改变预算：stoch_main_budget.py
改变poi点的数量：stoch_main_poi.py

4). 可信实验
赢者实验：believable_main.py
败者实验：believable_main_loser.py
