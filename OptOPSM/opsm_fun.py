import numpy as np
from OPSM.data_format import POI
from map.individual_probability_map import Person
from Config.param_config import param
import json


def find_max_value_user(USER: dict, winner_dict: dict, POIs: dict, add_total_value=False, seq=None) -> Person:
    """
    找到当前边际价值最大的用户
    :param POIs:
    :param USER:
    :param winner_dict:
    :return:
    """
    winner = winner_dict["winner"]
    current_total_value = winner_dict["total_value"]
    max_val = -1
    id = 0
    for user in USER.values():
        if user.allocated == 0:
            val = Vi(user, winner_dict, POIs, seq)  # 求边缘概率
            density = val / user.charge
            if density > max_val:
                max_val = density
                id = user.id
    if id != 0:
        USER[id].marginal_value = max_val * USER[id].charge
        USER[id].marginal_density = max_val
        if add_total_value:
            winner_dict["total_value"] += max_val * USER[id].charge
        return USER[id]
    return Person()  # 返回空用户(id==0)


def threshold(winners_dict:dict, max_user: Person, POIs: dict, budget=param['budget'], seq=None) -> float:
    marginal_val = Vi(max_user, winners_dict, POIs, seq)  # 计算加入max_user后的边际价值
    val_add_max_user = val_add_i(winners_dict, max_user, POIs, seq)  # 计算加入max_user后的价值
    t = (budget / 2)*(marginal_val/val_add_max_user)
    return t


def bij(winner_primers: dict, useri: Person, userij: Person, POIs: dict, seq=None):
    """
    bij = ui在A`中的边际价值*ui的要价/ij在A`中的边际价值
    :param winner_primers: ui在A`中的边际价值
    :param useri: ui
    :param userij: ij
    :param POIs:
    :return:
    """
    marginal_useri = Vi(useri, winner_primers, POIs, seq)
    marginal_userij = Vi(userij, winner_primers, POIs, seq)
    bij = (marginal_useri * userij.charge) / marginal_userij
    return bij


def rhoij(winner_primers: dict, useri: Person, POIs: dict, budget=param['budget'], seq=None):
    """
    rhoij = (ui在A`中的边际价值/A`加上ui总价值) * (预算/2)
    :param budget:
    :param winner_primers: A`
    :param useri: ui
    :param POIs:
    :return:
    """
    marginal_useri = Vi(useri, winner_primers, POIs, seq)
    total_value_useri = val_add_i(winner_primers, useri, POIs, seq)
    return (marginal_useri * budget) / (total_value_useri * 2)


def min_pi(winner_primers, useri: Person, userij: Person, POIs: dict, budget=param['budget'], seq=None):
    var_bij = bij(winner_primers, useri, userij, POIs, seq)
    var_rhoij = rhoij(winner_primers, useri, POIs, budget, seq)
    print(f"b({useri.id},{userij.id}) is {var_bij}")
    print(f"rho({useri.id},{userij.id}) is {var_rhoij}")
    if var_bij <= var_rhoij:
        return var_bij
    return var_rhoij


def is_last_winner(winners, winner):
    if winner.id == winners[-1].id:
        return True
    return False


def Vm(winners: dict, poi):
    """
    计算在poi点上产生的总价值
    :param winners:
    :param poi:
    :return:
    """
    value = 0
    if not winners["winner"]:
        return 0
    rm = poi.rm
    fenmu = 0
    for k in range(1, poi.rm + 1):
        fenmu += 1 / k
    i = 1
    fenzi = 0
    for user in winners["winner"]:
        if rm > 0:
            fenzi += user.probability_map[poi.id-1] / i
            rm -= 1
            i += 1
        else:
            break
    value = poi.vm*(fenzi/fenmu)
    return value


def Vi(user: Person, winners_dict: dict, POIs: dict, seq=None):
    """
    计算用户user的边际价值
    :param POIs:
    :param user: 需要计算边际价值的用户
    :param winners_dict: 当前胜者列表
    :return: 用户user的边际价值
    """
    val_add_user = val_add_i(winners_dict, user, POIs, seq)  # 在胜者用户中加入user之后的总价值
    return val_add_user - winners_dict["total_value"]


# def val_add_i(winner_dict: dict, user: Person, POIs: dict) -> float:
#     """
#     在胜者用户中加入user之后的总价值
#     :param POIs:
#     :param winners: 当前胜者用户
#     :param user: 当前用户user
#     :return:
#     """
#     sum_value = winner_dict["total_value"]
#     value = 0
#     for poi in POIs.values():
#         rm = poi.rm - len(winner_dict["winner"]) - 1
#         if rm >= 0:
#             value += (poi.vm / poi.rm) * user.probability_map[poi.id - 1]
#     sum_value += value
#     return sum_value

def val_add_i(winner_dict: dict, user: Person, POIs: dict, seq=None) -> float:
    """
    在胜者用户中加入user之后的总价值
    :param POIs:
    :param winners: 当前胜者用户
    :param user: 当前用户user
    :return:
    """
    sum_value = winner_dict["total_value"]
    value = 0
    for poi in POIs.values():
        rm = poi.rm - len(winner_dict["winner"]) - 1
        fenmu = 0
        fenzi = 0
        if rm >= 0:
            fenzi = user.probability_map[poi.id - 1] / (len(winner_dict['winner']) + 1)
            fenmu = seq[poi.rm - 1]
            value += poi.vm * (fenzi / fenmu)
    sum_value += value
    return sum_value



def winners_val(winners: list, POIs: dict) -> float:
    """
    计算当前胜者用户的总价值
    :param POIs:
    :param winners: 胜者用户列表
    :return:
    """
    sum_value = 0
    if winners:
        for poi in POIs.values():
            rm = poi.rm
            value = 0
            i = 1
            fenzi = 0
            fenmu = 0
            for user in winners:
                if rm > 0:
                    # value += user.probability_map[poi.id-1]
                    fenzi += user.probability_map[poi.id-1] / i
                    i += 1
                    rm -= 1
                else:
                    break
            for j in range(1, poi.rm + 1):
                fenmu += 1 / j
            value = poi.vm * (fenzi/fenmu)
            sum_value += value
        return sum_value
    else:
        return 0.0

