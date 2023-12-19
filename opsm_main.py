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
            winner = opsm.allocation_stage(USER, POIs, False, seq=sequence)

            print("-----------------------------Payment Stage-------------------------------")
            pool = mp.Pool(processes=param["processes"])
            users_pi = [pool.apply_async(opsm.payment_stage,
                                         (USER, POIs, user, winner, False, budget, sequence))
                        for user in winner["winner"]]

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
            bar.update(1)
            storege.storage_all(winner["winner"], POIs, 'document/opsm_result/USER_CHANGE/', int(user_file.split('.')[0]))


    # winner_num = 0
    # budget = param["budget"]
    #
    # winner = []  # 分配阶段的赢家, 元素为Person类型
    # users_primer = {}
    # winner_primer = []
    # total_value = 0
    # total_payment = 0
    #
    # print("---------------------------Display Data-----------------------------", end="\n")
    # data_format.display(POIs, USER)
    #
    # print("---------------------------Allocation Stage------------------------------", end="\n")
    # print(f"Round {winner_num + 1}")
    # max_user = opsm_fun.find_max_value_user(USER, winner, POIs)
    #
    # while max_user.charge <= opsm_fun.threshold(winner, max_user, POIs) and (max_user.id != 0):
    #     winner.append(max_user)
    #     max_user.allocated = 1
    #     winner_num += 1
    #     print(f"Round {winner_num + 1}")
    #     max_user = opsm_fun.find_max_value_user(USER, winner, POIs)
    #
    # print(f"winner list is {[user.id for user in winner]}")
    #
    # for user in winner:
    #     if user.id != 0:
    #         total_value += user.marginal_value
    #         print(f"user {user.id}  marginal_value is {user.marginal_value}, marginal_density "
    #               f"is {user.marginal_density}")
    # print(f"Total value of USERs is {total_value}")
    #
    # print("\n------------------------payment stage---------------------------")
    #
    # save_payment_stage = np.array(np.zeros(len(winner) * len(winner))).reshape(len(winner), len(winner))
    # i = 0
    #
    # for user in winner:
    #     print(f"\nCalculate user {user.id} payment")
    #     min = 0
    #     round = 1
    #     users_primer = copy.deepcopy(USER)
    #     users_primer.pop(user.id)
    #     for u in users_primer.values():  # 将user_primer中的所有用户置为未分配
    #         u.allocated = 0
    #     winner_primer.clear()
    #     print(f"Round {round}")
    #     max_user = opsm_fun.find_max_value_user(users_primer, winner_primer, POIs)  # 在user_primer中找到当前价值最大的用户
    #
    #     while (max_user.charge < opsm_fun.threshold(winner_primer, max_user, POIs)) and (max_user.id != 0):
    #         min = opsm_fun.min_pi(winner_primer, user, max_user, POIs)  # user为ui, max_user为uj, 即ij
    #         print(f"min p{user.id}({max_user.id}) is {min}")
    #         if user.pi < min:
    #             user.pi = min
    #
    #         save_payment_stage[i, round-1] = user.pi
    #
    #         round += 1
    #         print(f"Round {round}")
    #         winner_primer.append(max_user)
    #         max_user.allocated = 1
    #         max_user = opsm_fun.find_max_value_user(users_primer, winner_primer, POIs)
    #
    #     i += 1
    #
    #     # 如果是最后一个胜出用户，用其出价作为其关键价格，因为根据其前面的用户计算出来的
    #     # 支付可能会比其出价少。
    #
    #     if opsm_fun.is_last_winner(winner, user):
    #         if user.pi < user.charge:
    #             user.pi = user.charge
    #
    # print(f"payment list is:")
    #
    # winner_json = []
    # for user in winner:
    #     total_payment += user.pi
    #     print(f"user {user.id} bid is {user.charge} and payment is {user.pi}")
    #     winner_json.append(user.to_dict_base())
    #
    # print(f"BUDGET is {budget}, total payment is {total_payment}")
    #
    # total_value = 0
    # POIs_json = []
    # for poi in POIs.values():
    #     m_value = opsm_fun.Vm(winner, poi)
    #     total_value += m_value
    #     print(f"poi {poi.id} vm is {poi.vm} and real value is {m_value}")
    #     POIs_json.append(poi.to_dict())
    #
    # print(f"Total value of POIs is {total_value}")
    #
    # file_prefix = "budget_" + str(param["budget"]) + "+user_amount_" + str(param["sample_amount"])
    # folder = "document/result/"
    #
    # df_save_payment_stage = pd.DataFrame(np.around(save_payment_stage, 2), columns=[user.id for user in winner])
    # df_save_payment_stage.to_csv(folder+file_prefix+"payment_stage.csv", index=False)
    #
    # with open(folder+file_prefix+"_winner.json", "w") as file:
    #     json.dump(winner_json, file, cls=MyEncoder)
    #     file.close()
    #
    # with open(folder+file_prefix+"_POIs.json", "w") as file:
    #     json.dump(POIs_json, file, cls=MyEncoder)
    #     file.close()
