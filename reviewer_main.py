from Config.param_config import param
from Reviewer import reviewer, reviewer_fun
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
    path = "document/probability/"
    budget = param["budget"]
    task_map_file = "document/task_map.csv"
    value_map_file = "document/value_map.csv"
    POIs = {}
    USER = {}
    # for i in range(1):w
    with tqdm(total=len(os.listdir(path)), ncols=100) as bar:
        for user_file in os.listdir(path):
            POIs.clear()
            USER.clear()
            POIs = data_format.task_data_format(task_map_file, value_map_file)  # POI点，字典
            USER = data_format.person_format(os.path.join(path, user_file))  # 用户列表，字典

            # # 测试数据
            # POIs = {1: POI(1, 1, 3), 2: POI(2, 2, 6)}
            # USER = {1: Person(attributes={"id": 1, "charge": 3, "probability_map": [[0.3, 0.5]]}),
            #         2: Person(attributes={"id": 2, "charge": 2, "probability_map": [[0.8, 0.5]]}),
            #         3: Person(attributes={"id": 3, "charge": 3, "probability_map": [[0.6, 0.6]]})}

            print("---------------------------Allocation Stage------------------------------")
            winner = reviewer.allocation_stage(USER, POIs, False, seq=sequence)

            print("-----------------------------Payment Stage-------------------------------")
            pool = mp.Pool(processes=param["processes"])
            users_pi = [pool.apply_async(reviewer.payment_stage, (USER, POIs, user, winner, False, budget, sequence)) for user in winner["winner"]]

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
                m_value = reviewer_fun.Vm(winner, poi)
                total_value += m_value
                print(f"poi {poi.id} vm is {poi.vm} and real value is {m_value}")

            print(f"Total value of POIs is {total_value}")
            bar.update(1)
            storege.storage_all(winner["winner"], POIs, 'document/reviewer_result/USER_CHANGE/', int(user_file.split('.')[0]))