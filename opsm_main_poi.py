from Config.param_config import param
from OptOPSM import opsm, opsm_fun
from OPSM import data_format
from map.individual_probability_map import Person
from OPSM.data_format import POI
import storege
import os
import multiprocessing as mp
from tqdm import tqdm
import json

if __name__ == "__main__":
    with open("document/sequence/sequence.json", "r") as file:
        sequence = json.load(file)
        sequence = list(sequence['sequence'])
        file.close()
    paths = ["document/InputData/POI_select_map_02/",
             "document/InputData/POI_select_map_03/",
             "document/InputData/POI_select_map_04/",
             "document/InputData/POI_select_map_05/"]
    budget = param["budget"]
    task_map_file = "document/task_map.csv"
    value_map_file = "document/value_map.csv"
    user_file = "document/probability/1000.json"
    POIs = {}
    USER = {}
    index = 2
    # for i in range(1):w
    with tqdm(total=len(paths) * 10, ncols=100) as bar:
        for path in paths:
            print(path.split("/")[-2])
            for select_file in os.listdir(path):
                POIs.clear()
                USER.clear()
                select_file_path = os.path.join(path, select_file)
                POIs = data_format.task_format_poi_change(task_map_file, value_map_file, select_file_path)  # POI点，字典
                print('user loading...')
                USER = data_format.user_format_poi_change(user_file, select_file_path)  # 用户列表，字典
                print('loading complete')

                # # 测试数据
                # POIs = {1: POI(1, 1, 3), 2: POI(2, 2, 6)}
                # USER = {1: Person(attributes={"id": 1, "charge": 3, "probability_map": [[0.3, 0.5]]}),
                #         2: Person(attributes={"id": 2, "charge": 2, "probability_map": [[0.8, 0.5]]}),
                #         3: Person(attributes={"id": 3, "charge": 3, "probability_map": [[0.6, 0.6]]})}

                print("---------------------------Allocation Stage------------------------------")
                winner = opsm.allocation_stage(USER, POIs, False, seq=sequence)

                print("-----------------------------Payment Stage-------------------------------")
                pool = mp.Pool(processes=param["processes"])
                users_pi = [pool.apply_async(opsm.payment_stage, (USER, POIs, user, winner, False, budget, sequence)) for user in
                            winner["winner"]]

                total_payment = 0
                print(f"payment list is:")

                i = 0
                for user in winner["winner"]:
                    user.pi = users_pi[i].get()
                    i += 1
                    total_payment += user.pi
                    print(f"user {user.id} bid is {user.charge} and payment is {user.pi}")

                print(f"BUDGET is {budget}, total payment is {total_payment}")

                total_value = 0
                for poi in POIs.values():
                    m_value = opsm_fun.Vm(winner, poi)
                    total_value += m_value
                    print(f"poi {poi.id} vm is {poi.vm} and real value is {m_value}")

                print(f"Total value of POIs is {total_value}")

                storege.storage_all(winner["winner"], POIs, f'document/opsm_result/POI_result/POI_CHANGE_0{index}/', len(POIs))
                bar.update(1)
            index += 1
