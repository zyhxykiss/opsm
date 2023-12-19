import json
import pandas as pd
import numpy as np
from Config.param_config import param


class BeaconPerson:
    def __init__(self, attributes: dict, select_map=None, t=param["beacon_threshold"]):
        self.id = attributes["id"]
        if select_map is None:
            self.probability_map = self.reload_probability_map(attributes['probability_map'])  # 覆盖概率
        else:
            self.probability_map = self.reload_pro_as_select(attributes['probability_map'], select_map)
        self.cover_map = self.reload_cover_map(t)
        self.charge = attributes['charge']  # 要价
        self.allocated = 0
        self.pi = 0  # 拍卖成功后得到的回报
        self.marginal_value = 0  # 边际价值
        self.marginal_density = 0  # 边际密度

    def reload_cover_map(self, t):
        reload = []
        for elem in self.probability_map:
            if elem == 0:
                continue
            elif elem >= t:
                reload.append(1)
            else:
                reload.append(0)
        return reload

    def reload_probability_map(self, probability_map):
        reload = []
        for line in probability_map:
            for elem in line:
                if elem != 0:
                    reload.append(elem)
        return reload

    def reload_pro_as_select(self, probability_map: list, select_map: list):
        reload = []
        for i in range(param['map_rows']):
            for j in range(param['map_columns']):
                if select_map[i][j] == 1:
                    reload.append(probability_map[i][j])
        return reload


    def beacon_to_dict(self):
        return {
            "id": self.id,
            "charge": self.charge,
            "pi": self.pi,
            "marginal_value": self.marginal_value,
            "marginal_density": self.marginal_density
        }


def USER_format(person_file, t=param["beacon_threshold"]):
    with open(person_file, 'r') as file:
        ps = json.load(file)

    persons = {}
    for person in ps:
        persons[person["id"]] = BeaconPerson(attributes=person, t=t)
    return persons


def USER_format_select(user_file, select_file):
    with open(user_file, 'r') as file:
        users = json.load(file)

    select_map = np.array(pd.read_csv(select_file)).tolist()

    USER = {}
    for user in users:
        USER[user['id']] = BeaconPerson(attributes=user, select_map=select_map)
    return USER
