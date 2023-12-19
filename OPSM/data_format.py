import pandas as pd
from Config.param_config import param
from map.individual_probability_map import Person
import json
import numpy as np


class POI:
    def __init__(self, id: int, rm, vm):
        self.id = id
        self.rm = rm
        self.vm = vm

    def display(self):
        pass

    def to_dict(self):
        return {
            "id": self.id,
            "rm": self.rm,
            "vm": self.vm
        }


def task_data_format(task_map_file, value_map_file) -> dict:
    """
    将任务地图转化为POI类
    :param task_map_file:
    :param value_map_file:
    :return:
    """
    task_map = pd.read_csv(task_map_file)
    value_map = pd.read_csv(value_map_file)

    POIs = {}
    POI_id = 1

    for i in range(param["map_rows"]):
        for j in range(param['map_columns']):
            if task_map.iloc[i, j] != 0:
                POIs[POI_id] = POI(POI_id, task_map.iloc[i][j], value_map.iloc[i][j])
                POI_id += 1
    return POIs


def task_format_poi_change(task_map_file, value_map_file, select_map_file) -> dict:
    task_map = pd.read_csv(task_map_file)
    value_map = pd.read_csv(value_map_file)
    select_map = np.array(pd.read_csv(select_map_file)).tolist()

    POIs = {}
    poi_id = 1
    for i in range(param["map_rows"]):
        for j in range(param["map_columns"]):
            if select_map[i][j] == 1:
                POIs[poi_id] = POI(poi_id, task_map.iloc[i, j], value_map.iloc[i][j])
                poi_id += 1
    return POIs


def person_format(person_file) -> dict:
    """
    将人物信息从json文件中读取并转化为BasePerson类
    :param person_file:
    :return:
    """
    with open(person_file, 'r') as file:
        ps = json.load(file)

    persons = {}
    for person in ps:
        persons[person["id"]] = Person(attributes=person)
    return persons


def user_format_poi_change(user_file, select_map_file) -> dict:
    with open(user_file, 'r') as file:
        users = json.load(file)
    select_map = np.array(pd.read_csv(select_map_file)).tolist()

    USER = {}
    for user in users:
        USER[user["id"]] = Person(attributes=user, select_map=select_map)
    return USER


def display(POI: dict, USER: dict):
    print(f"There are {len(USER)} users and {len(POI)} POIs, and BUDGET is {param['budget']}")

    for user in USER.values():
        print(f"user {user.id} bid is {user.charge} and probability vector is {user.probability_map[0:5]}...")

    print()
    for poi in POI.values():
        print(f"POI {poi.id} need cover {poi.rm} times and generate a value (vm) up to {poi.vm}")
    print()

