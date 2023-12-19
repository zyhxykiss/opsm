import copy
from OPSM import opsm_fun
from Config.param_config import param
from BEACON import beacon_fun
from map.individual_probability_map import Person


def allocation_stage(USER: dict, POIs: dict, log_display=False) -> list:
    winner = []

    winner_num = 0
    max_dv_user = beacon_fun.find_max_value_user(USER, winner, POIs)  # dv 为 density value 的缩写
    while (max_dv_user.id != 0) and (max_dv_user.charge <= beacon_fun.threshold(winner, max_dv_user, POIs)):
        winner.append(max_dv_user)
        max_dv_user.allocated = 1
        winner_num += 1
        print(f"Round {winner_num + 1}")
        max_dv_user = beacon_fun.find_max_value_user(USER, winner, POIs)

    print(f"winner list is {[user.id for user in winner]}")

    total_value = 0
    if log_display:
        for user in winner:
            if user.id != 0:
                total_value += user.marginal_value
                print(f"user {user.id}  marginal_value is {user.marginal_value}, marginal_density "
                      f"is {user.marginal_density}")
        print(f"Total value of USERs is {total_value}")

    return winner


def payment_stage(USER: dict, POIs: dict, user: Person, winner: list, log_display=False):
    if log_display:
        print(f"\nCalculate user {user.id} payment")
    min = 0
    round = 0
    user_prime = copy.deepcopy(USER)
    user_prime.pop(user.id)
    for u in user_prime.values():
        u.allocated = 0
    winner_primer = []
    max_user = beacon_fun.find_max_value_user(user_prime, winner_primer, POIs)

    while (max_user.charge < beacon_fun.threshold(winner_primer, max_user, POIs)) and (max_user.id != 0):
        min = beacon_fun.min_pi(winner_primer, user, max_user, POIs)
        if log_display:
            print(f"min p{user.id}({max_user.id}) is {min}")

        if user.pi < min:
            user.pi = min
        round += 1
        winner_primer.append(max_user)
        max_user.allocated = 1
        max_user = beacon_fun.find_max_value_user(user_prime, winner_primer, POIs)
    print(f"------------{user.pi}")
    if user == winner[-1]:
        if user.pi < user.charge:
            user.pi = user.charge
    print(user.pi)
    return user.pi

