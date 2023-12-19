from OptBEACON import beacon
from OptBEACON import data_format
from OPSM.data_format import POI, task_format_poi_change
from BEACON.data_format import BeaconPerson
from Config.param_config import param
from OptBEACON import beacon_fun
import storege

import multiprocessing as mp
import os
from datetime import datetime
from tqdm import tqdm

if __name__ == "__main__":
    budget = param["budget"]
    task_map_file = "document/task_map.csv"
    value_map_file = "document/value_map.csv"
    paths = ["document/InputData/POI_select_map_02/",
             "document/InputData/POI_select_map_03/",
             "document/InputData/POI_select_map_04/",
             "document/InputData/POI_select_map_05/"]
    user_file = 'document/probability/1000.json'
    POIs = {}
    USER = {}
    index = 2
    # for j in range(0, 1):
    with tqdm(total=len(paths) * 10, ncols=100) as bar:
        for path in paths:
            print(path.split("/")[-2])
            for select_file in os.listdir(path):
                POIs.clear()
                USER.clear()
                select_path = os.path.join(path, select_file)
                POIs = task_format_poi_change(task_map_file, value_map_file, select_path)
                USER = data_format.USER_format_select(user_file, select_path)

                # POIs = {1: POI(1, 1, 3), 2: POI(2, 2, 6)}
                # USER = {1: BeaconPerson(attributes={"id": 1, "charge": 3, "probability_map": [[0.3, 0.5]]}),
                #         2: BeaconPerson(attributes={"id": 2, "charge": 2, "probability_map": [[0.8, 0.5]]}),
                #         3: BeaconPerson(attributes={"id": 3, "charge": 3, "probability_map": [[0.6, 0.6]]})}

                print("---------------------------Allocation Stage------------------------------")
                winner = beacon.allocation_stage(USER, POIs, False)

                print("-----------------------------Payment Stage-------------------------------")
                pool = mp.Pool(processes=param["processes"])
                users_pi = [pool.apply_async(beacon.payment_stage, (USER, POIs, user, winner, False)) for user in
                            winner["winner"]]

                total_payment = 0
                i = 0
                for user in winner["winner"]:
                    user.pi = users_pi[i].get()
                    i += 1
                    total_payment += user.pi
                    print(f"user {user.id} bid is {user.charge} and payment is {user.pi}")

                print(f"BUDGET is {budget}, total payment is {total_payment}")

                total_value = 0
                for poi in POIs.values():
                    m_value = beacon_fun.Vm(winner, poi)
                    total_value += m_value
                    print(f"poi {poi.id} vm is {poi.vm} and real value is {m_value}")

                print(f"Total value of POIs is {total_value}")

                storege.storage_all(winner["winner"], POIs, f'document/beacon_result/POI_result/POI_CHANGE_0{index}/', len(POIs))
                bar.update(1)
            index += 1
    dt = datetime.now()
    print(dt.strftime("完成时间：%Y年%m月%d日 %H:%M:%S"))
