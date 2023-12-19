import copy
from OPSM import opsm_fun
from Config.param_config import param
from OptBEACON import beacon_fun
from map.individual_probability_map import Person


def allocation_stage(USER: dict, POIs: dict, log_display=False, budget=param["budget"]) -> dict:
    winner = {"winner": [], "total_value": 0}
    print(f"{len(USER)} USER start allocation")
    winner_num = 0
    max_dv_user = beacon_fun.find_max_value_user(USER, winner, POIs, True)  # dv 为 density value 的缩写
    while (max_dv_user.id != 0) and (max_dv_user.charge <= beacon_fun.threshold(winner, max_dv_user, POIs, budget)):
        winner["winner"].append(max_dv_user)
        max_dv_user.allocated = 1
        winner_num += 1
        max_dv_user = beacon_fun.find_max_value_user(USER, winner, POIs, True)

    print(f"winner length is {len(winner['winner'])}")

    total_value = 0

    for user in winner["winner"]:
        if user.id != 0:
            total_value += user.marginal_value
            if log_display:
                print(f"user {user.id}  marginal_value is {user.marginal_value}, marginal_density "
                      f"is {user.marginal_density}")
    print(f"Total value of USERs is {total_value}")

    return winner


def payment_stage(USER: dict, POIs: dict, user: Person, winner: dict, log_display=False, budget=param["budget"]):
    print(f"\nCalculate user {user.id} payment")
    min = 0
    round = 0
    user_prime = copy.deepcopy(USER)
    user_prime.pop(user.id)
    for u in user_prime.values():
        u.allocated = 0
    winner_primer = {"winner": [], "total_value": 0}
    max_user = beacon_fun.find_max_value_user(user_prime, winner_primer, POIs)

    while (max_user.charge < beacon_fun.threshold(winner_primer, max_user, POIs, budget)) and (max_user.id != 0):
        min = beacon_fun.min_pi(winner_primer, user, max_user, POIs, budget)
        if log_display:
            print(f"min p{user.id}({max_user.id}) is {min}")

        if user.pi < min:
            user.pi = min
        round += 1
        winner_primer["winner"].append(max_user)
        max_user.allocated = 1
        winner_primer["total_value"] += max_user.marginal_value
        max_user = beacon_fun.find_max_value_user(user_prime, winner_primer, POIs)
    if user == winner["winner"][-1]:
        if user.pi < user.charge:
            user.pi = user.charge
    return user.pi

