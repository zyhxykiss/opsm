import numpy as np
from OPSM.data_format import POI
from map.individual_probability_map import Person
from Config.param_config import param


def find_max_value_user(USER: dict, winner: list, POIs: dict) -> Person:
    """
    找到当前边际价值最大的用户
    :param POIs:
    :param USER:
    :param winner:
    :return:
    """
    max_val = -1
    id = 0
    for user in USER.values():
        if user.allocated == 0:
            val = Vi(user, winner, POIs)
            density = val / user.charge
            if density > max_val:
                max_val = density
                id = user.id
    if id != 0:
        USER[id].marginal_value = max_val * USER[id].charge
        USER[id].marginal_density = max_val
        return USER[id]
    return Person()  # 返回空用户(id==0)


def threshold(winners: list, max_user: Person, POIs: dict) -> float:
    marginal_val = Vi(max_user, winners, POIs)  # 计算加入max_user后的边际价值
    val_add_max_user = val_add_i(winners, max_user, POIs)  # 计算加入max_user后的价值
    t = (param["budget"]/2.0)*(marginal_val/val_add_max_user)
    return t


def bij(winner_primers: list, useri: Person, userij: Person, POIs: dict):
    """
    bij = ui在A`中的边际价值*ui的要价/ij在A`中的边际价值
    :param winner_primers: ui在A`中的边际价值
    :param useri: ui
    :param userij: ij
    :param POIs:
    :return:
    """
    marginal_useri = Vi(useri, winner_primers, POIs)
    marginal_userij = Vi(userij, winner_primers, POIs)
    bij = (marginal_useri * userij.charge) / marginal_userij
    return bij


def rhoij(winner_primers: list, useri: Person, POIs: dict):
    """
    rhoij = (ui在A`中的边际价值/A`加上ui总价值) * (预算/2)
    :param winner_primers: A`
    :param useri: ui
    :param POIs:
    :return:
    """
    marginal_useri = Vi(useri, winner_primers, POIs)
    total_valu_useri = val_add_i(winner_primers, useri, POIs)
    return (marginal_useri * param["budget"]) / (total_valu_useri * 2)


def min_pi(winner_primers, useri: Person, userij: Person, POIs: dict):
    var_bij = bij(winner_primers, useri, userij, POIs)
    var_rhoij = rhoij(winner_primers, useri, POIs)
    if var_bij <= var_rhoij:
        return var_bij
    return var_rhoij


def is_last_winner(winners, winner):
    if winner.id == winners[-1].id:
        return True
    return False


def Vm(winners, poi):
    """
    计算在poi点上产生的总价值
    :param winners:
    :param poi:
    :return:
    """
    value = 0
    if not winners:
        return 0
    rm = poi.rm
    for user in winners:
        if rm > 0:
            value += user.probability_map[poi.id-1]
            rm -= 1
        else:
            break
    value = (value * poi.vm) / poi.rm
    return value


def Vi(user: Person, winners: list, POIs: dict):
    """
    计算用户user的边际价值
    :param POIs:
    :param user: 需要计算边际价值的用户
    :param winners: 当前胜者列表
    :return: 用户user的边际价值
    """
    val_add_user = val_add_i(winners, user, POIs)  # 在胜者用户中加入user之后的总价值
    val_winner = winners_val(winners, POIs)  # 当前胜者用户的价值
    return val_add_user - val_winner


def val_add_i(winners: list, user: Person, POIs: dict) -> float:
    """
    在胜者用户中加入user之后的总价值
    :param POIs:
    :param winners: 当前胜者用户
    :param user: 当前用户user
    :return:
    """
    new_winners = winners.copy()
    new_winners.append(user)
    return winners_val(new_winners, POIs)


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
            for user in winners:
                if rm > 0:
                    value += user.probability_map[poi.id-1]
                    rm -= 1
                else:
                    break
            value = value * poi.vm/poi.rm
            sum_value += value
        return sum_value
    else:
        return 0.0

