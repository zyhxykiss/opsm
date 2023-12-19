from map.individual_probability_map import Person
from Config.param_config import param
from OptOPSM import opsm_fun


def find_max_value_in_winner(USER: list, winner: dict, POIs: dict) -> Person:
    """
    找到当前边际价值最大的用户
    :param POIs:
    :param USER:
    :param winner:
    :return:
    """
    max_val = -1
    max_index = 0
    index = 0
    for user in USER:
        if user.allocated == 0:
            val = opsm_fun.Vi(user, winner, POIs)
            density = val / user.charge
            if density > max_val:
                max_val = density
                max_index = index
        index += 1
    USER[max_index].marginal_value = max_val * USER[max_index].charge
    USER[max_index].marginal_density = max_val
    return USER[max_index]


def find_max_value(USER: dict, winner: dict, POIs: dict) -> Person:
    """
    找到当前边际价值最大的用户
    :param POIs:
    :param USER:
    :param winner:
    :return:
    """
    max_val = -1
    for user in USER.values():
        if user.allocated == 0:
            val = opsm_fun.Vi(user, winner, POIs)
            density = val / user.charge
            if density > max_val:
                max_val = density
    return max_val


def threshold(winner_dict: dict, user: Person, POIs: dict, budget=param['budget']):
    marginal_value = opsm_fun.Vi(user, winner_dict, POIs)  # 计算user的边缘价值
    val_add_max_user = opsm_fun.val_add_i(winner_dict, user, POIs)  # 计算加上user后winner的总价值
    t = (budget/2) * (marginal_value/val_add_max_user)
    return t, val_add_max_user
