from Config.my_Enum import PointWeight as PW
import pandas as pd
import numpy as np
from Config.param_config import param
import random
import math
from individual_probability_map import normal_trunc


"""
    该点的访问次数 = 权重*随机值
    随机区间 = [1， 2], 正态分布
    :param data_map_file: 数字地图的存储路径
    :param point_weight_file: 权重的存储路径
    :param visit_upper_limit: 点允许的最大访问次数
    :return: task_map
    """


def task_map_maker(data_map_file: str, point_weight_file: str,
                   visit_upper_limit: int) -> np.array:
    data_map = pd.read_csv(data_map_file)
    point_weight = pd.read_csv(point_weight_file)

    columns = data_map.columns.tolist()
    indexs = data_map.index.tolist()

    task_map = np.array(np.zeros(param['map_rows']*param['map_columns']), dtype=int).\
        reshape(param['map_rows'], param['map_columns'])

    for i in range(len(indexs)):
        for j in range(len(columns)):
            task_map[i][j] = set_visit_time(point_weight.iloc[i, j])
    return task_map


def set_visit_time(point_weight: int) -> int:
    base_num = np.random.normal(param["task_map_random"]["col"], scale=param["task_map_random"]["col"])
    while (base_num < param["task_map_random"]["min"]) or (base_num > param["task_map_random"]["max"]):
        base_num = np.random.normal(param["task_map_random"]["col"], scale=param["task_map_random"]["col"])
    visit_time = int(np.around(base_num*point_weight, 1) * 10)
    return visit_time


def value_map_maker(task_map):
    value_map = np.array(np.zeros(param["map_rows"]*param["map_columns"])).\
        reshape(param["map_rows"], param["map_columns"])
    for i in range(param["map_rows"]):
        for j in range(param["map_columns"]):
            value_map[i][j] = np.around(task_map[i, j] * normal_trunc(1.5, 1, 1, 2), 2)
    return value_map


if __name__ == '__main__':
    data_map_file = '../document/data_map.csv'
    point_weight_file = '../document/weight_map.csv'

    task_map = task_map_maker(data_map_file, point_weight_file, param['visit_upper_limit'])
    columns = [f"X_{i}" for i in range(0, 41)]
    indexs = [f"Y_{i}" for i in range(0, 31)]

    df_task_map = pd.DataFrame(task_map, columns=columns, index=indexs)
    df_task_map.to_csv('../document/task_map.csv', index=False)

    value_map = value_map_maker(task_map)
    df_value_map = pd.DataFrame(value_map, columns=columns, index=indexs)
    df_value_map.to_csv('../document/value_map.csv', index=False)
