import multiprocessing as mp
import os
import json
from Config.param_config import param
from OptOPSM import opsm, opsm_fun
from OPSM import data_format
from Stochastic import stochastic as sth
import storege
from Believable import believable as be
from tqdm import tqdm


if __name__ == "__main__":
    with open("document/sequence/sequence.json", "r") as file:
        sequence = json.load(file)
        sequence = list(sequence['sequence'])
        file.close()
    budget = param["budget"]
    task_map_file = "document/task_map.csv"
    value_map_file = "document/value_map.csv"
    # path = "document/probability/"
    user_path = 'document/probability/1000.json'
    POIs = {}
    USER = {}
    observe_user = be.find_loser_user()
    ou_charges = [float(i) for i in range(6, 60, 2)]
    print(f"observe user is {observe_user.id}")

    with tqdm(total=len(ou_charges), ncols=100) as bar:
        for ou_charge in ou_charges:
            POIs.clear()
            USER.clear()
            POIs = data_format.task_data_format(task_map_file, value_map_file)  # POI点，字典
            USER = data_format.person_format(user_path)  # 用户列表，字典
            USER[observe_user.id].charge = ou_charge

            # # 测试数据
            # POIs = {1: POI(1, 1, 3), 2: POI(2, 2, 6)}
            # USER = {1: Person(attributes={"id": 1, "charge": 3, "probability_map": [[0.3, 0.5]]}),
            #         2: Person(attributes={"id": 2, "charge": 2, "probability_map": [[0.8, 0.5]]}),
            #         3: Person(attributes={"id": 3, "charge": 3, "probability_map": [[0.6, 0.6]]})}

            print("\n---------------------------Allocation Stage------------------------------")
            winner = opsm.allocation_stage(USER, POIs, False, seq=sequence)

            print("-----------------------------Payment Stage-------------------------------")
            pool = mp.Pool(processes=param["processes"])
            users_pi = [pool.apply_async(opsm.payment_stage, (USER, POIs, user, winner, False, budget, sequence)) for user in winner["winner"]]

            total_payment = 0

            i = 0
            for user in winner["winner"]:
                user.pi = users_pi[i].get()
                i += 1
                total_payment += user.pi
                print(f"user {user.id} bid is {user.charge} and payment is {user.pi}")

            print(f"BUDGET is {budget}, total payment is {total_payment}")
            #
            # total_value = 0
            # for poi in POIs.values():
            #     m_value = opsm_fun.Vm(winner, poi)
            #     total_value += m_value
            #     print(f"poi {poi.id} vm is {poi.vm} and real value is {m_value}")
            #
            # print(f"Total value of POIs is {total_value}")

            if USER[observe_user.id] not in winner['winner']:
                break
            else:
                print(f"Observe user location in winner list is {winner['winner'].index(USER[observe_user.id])}")

            storege.storage_all(winner['winner'], POIs, 'document/believable_result/loser/winner_POIs/', ou_charge)
            storege.storage_observe_user('document/believable_result/loser/observe_USER/', observe_user, ou_charge)
            bar.update(1)
