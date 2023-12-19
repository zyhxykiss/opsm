from map.individual_probability_map import Person
from Config.param_config import param
import json
import datetime
import numpy as np


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


if __name__ == "__main__":
    data_map_file = "document/data_map.csv"
    samples = []
    pid = 1
    for _ in range(1, 11):
        for i in range(0, 200):
            sample = Person(pid, data_map_file)
            samples.append(sample.to_dict())
            pid += 1

        json_file_name = 'document/probability/' + str(_*200) + '.json'
        with open(json_file_name, "w") as file:
            json.dump(samples, file, cls=MyEncoder)
            file.close()
        print(f"完成了样本{_*200}批次的样本生成")
