import random
from Config.param_config import param
import pandas as pd
import numpy as np


def select_POI(POI_num: int, POI_file: str) -> np.array:
    POI_map = pd.read_csv(POI_file)
    select_map = np.array(np.zeros(param['map_rows'] * param['map_columns'])).\
        reshape(param['map_rows'], param['map_columns'])
    i = random.choice(range(0, param['map_rows']))
    j = random.choice(range(0, param['map_columns']))
    while POI_num > 0:
        if (select_map[i, j] == 0) and (POI_map.iloc[i, j] != 0):
            select_map[i, j] = 1
            POI_num -= 1
        i = random.choice(range(0, param['map_rows']))
        j = random.choice(range(0, param['map_columns']))
    return select_map


def storage(array: np.array):
    sdf = pd.DataFrame(array, columns=[f'X_{i}' for i in range(0, array.shape[1])])
    sdf.to_csv(f"../document/InputData/POI_select_map_05/select_map_{int(np.sum(np.sum(array)))}.csv", index=False)


if __name__ == "__main__":
    POI_file = '../document/task_map.csv'
    for poi_num in range(191, 642, 50):
        select_map = select_POI(poi_num, POI_file)
        print(f'{poi_num} select map generation complete')
        storage(select_map)
