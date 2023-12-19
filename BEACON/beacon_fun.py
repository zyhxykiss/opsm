from BEACON.data_format import BeaconPerson
from Config.param_config import param


def find_max_value_user(USER, winner, POIs) -> BeaconPerson:
    max_val = 0
    id = 0
    for user in USER.values():
        if user.allocated == 0:
            val = Vi(user, winner, POIs)  # 计算user的边缘价值
            density = val / user.charge  # 计算user的边缘密度
            if density > max_val:
                max_val = density
                id = user.id
    if id != 0:
        USER[id].marginal_value = max_val * USER[id].charge
        USER[id].marginal_density = max_val
        return USER[id]
    return BeaconPerson({"id": 0, "probability_map": "", "charge": 0})


def min_pi(USER, useri, userij, POIs) -> float:
    var_bij = bij(USER, useri, userij, POIs)
    var_rhoij = rhoij(USER, useri, POIs)
    if var_bij <= var_rhoij:
        return var_bij
    return var_rhoij


def bij(USER, useri, userij, POIs):
    marginal_useri = Vi(useri, USER, POIs)
    marginal_userij = Vi(userij, USER, POIs)
    bij = (marginal_useri * userij.charge) / marginal_userij
    return bij


def rhoij(USER, useri, POIs):
    marginal_useri = Vi(useri, USER, POIs)
    total_valu_useri = val_add_i(USER, useri, POIs)
    return (marginal_useri * param["budget"]) / (total_valu_useri * 2)


def threshold(winners, userij, POIs) -> float:
    marginal_val = Vi(userij, winners, POIs)  # 计算加入max_user后的边际价值
    val_add_max_user = val_add_i(winners, userij, POIs)  # 计算加入max_user后的价值
    t = (param["budget"] / 2.0) * (marginal_val / val_add_max_user)
    return t


def Vi(user, winners, POIs) -> float:
    val_add_user = val_add_i(winners, user, POIs)  # 在胜者用户中加入user之后的总价值
    val_winner = winners_val(winners, POIs)  # 当前胜者用户的价值
    return val_add_user - val_winner


def val_add_i(winners, user, POIs):
    new_winners = winners.copy()
    new_winners.append(user)
    return winners_val(new_winners, POIs)


def winners_val(winners, POIs):
    sum_value = 0
    if winners:
        for poi in POIs.values():
            rm = poi.rm
            value = 0
            for user in winners:
                if rm > 0:
                    value += user.cover_map[poi.id - 1]
                    rm -= 1
                else:
                    break
            value = value * (poi.vm / poi.rm)
            sum_value += value
        return sum_value
    else:
        return 0.0


def Vm(winners, poi):
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
