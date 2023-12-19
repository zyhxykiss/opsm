import json
from Config.param_config import param


class BeaconPerson:
    def __init__(self, attributes: dict):
        self.id = attributes["id"]
        self.probability_map = self.reload_probability_map(attributes['probability_map'])  # 覆盖概率
        self.cover_map = self.reload_cover_map(attributes['probability_map'])
        self.charge = attributes['charge']  # 要价
        self.allocated = 0
        self.pi = 0  # 拍卖成功后得到的回报
        self.marginal_value = 0  # 边际价值
        self.marginal_density = 0  # 边际密度

    def reload_cover_map(self, probability_map):
        reload = []
        for line in probability_map:
            for elem in line:
                if elem == 0:
                    continue
                elif elem >= param['beacon_threshold']:
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

    def beacon_to_dict(self):
        return {
            "id": self.id,
            "charge": self.charge,
            "pi": self.pi,
            "marginal_value": self.marginal_value,
            "marginal_density": self.marginal_density
        }


def USER_format(person_file):
    with open(person_file, 'r') as file:
        ps = json.load(file)

    persons = {}
    for person in ps:
        persons[person["id"]] = BeaconPerson(attributes=person)
    return persons
