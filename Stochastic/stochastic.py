from OptOPSM import opsm_fun
import random
from Config.param_config import param
from Stochastic import stoch_fun
from map.individual_probability_map import Person
import copy


def allocation_stage(USER: dict, POIs: dict, log_display=False, budget=param['budget']) -> dict:
    """
    try_time <-- set a failure times threshold  # 这里取50
    winner <-- a space set
    win_user <-- random choice an user from user set
    while try_time > 0:
    {
        if win_user`s bid < (B/2) * (marginal_value of win_user) / (total value of winner + win_user):
            winner <-- winner + win_user
            try_time <-- initiate value
        else:
            try_time -= 1
        win_user <-- random choice an user from user set
    }

    :param USER:
    :param POIs:
    :param log_display:
    :param budget:
    :return:
    """
    print(f"{len(USER)} start to allocation")
    try_time = param["stoch_try_times"]
    winner = {"winner": [], "total_value": 0}

    budget_limit = budget

    win_user = USER[random.choice(range(1, len(USER) + 1))]
    while (try_time > 0) and (budget_limit - win_user.charge > 0):
        thresh, total_value = stoch_fun.threshold(winner, win_user, POIs, budget)
        if (win_user.charge <= thresh) and (win_user.allocated == 0):
            print(f'win user is {win_user.id}\tbid is {win_user.charge}\tthreshold is {thresh}')
            win_user.marginal_value = opsm_fun.Vi(win_user, winner, POIs)
            win_user.marginal_density = win_user.marginal_value / win_user.charge
            winner["winner"].append(win_user)
            win_user.allocated = 1
            winner["total_value"] = total_value
            try_time = param["stoch_try_times"]
            budget_limit -= win_user.charge
        else:
            try_time -= 1
        win_user = USER[random.choice(range(1, len(USER) + 1))]

    # sort_winner = {"winner": [], "total_value": 0}
    #
    # for i in range(len(winner["winner"])):
    #     max_user = stoch_fun.find_max_value_in_winner(winner["winner"], sort_winner, POIs)
    #     sort_winner["winner"].append(max_user)
    #     max_user.allocated = 1

    total_value = 0
    for user in winner["winner"]:
        if user.id != 0:
            total_value += user.marginal_value
            if log_display:
                print(f"user {user.id}  marginal_value is {user.marginal_value}, marginal_density "
                      f"is {user.marginal_density}")
    print(f"Length of winner is {len(winner['winner'])}...")
    print(f"Total value of USERs is {total_value}")

    return winner


def payment_stage(v, lock, USER: dict, POIs: dict, user: Person, winner: dict, log_display=False, budget=param['budget']):
    print(f"\nCalculate user {user.id} payment")
    min = 0
    round = 0
    user_prime = copy.deepcopy(USER)
    user_prime.pop(user.id)
    for u in user_prime.values():
        u.allocated = 0
    winner_primer = {"winner": [], "total_value": 0}
    max_user = opsm_fun.find_max_value_user(user_prime, winner_primer, POIs)

    while (max_user.charge < opsm_fun.threshold(winner_primer, max_user, POIs, budget)) and (max_user.id != 0):
        min = opsm_fun.min_pi(winner_primer, user, max_user, POIs, budget)
        if log_display:
            print(f"min p{user.id}({max_user.id}) is {min}")

        if user.pi < min:
            user.pi = min
        round += 1
        winner_primer['winner'].append(max_user)
        max_user.allocated = 1
        max_user = opsm_fun.find_max_value_user(user_prime, winner_primer, POIs)
    if user.pi < user.charge:
        user.pi = user.charge
    lock.acquire()
    v.value -= user.pi
    if v.value < 0:
        user.pi = 0
    lock.release()
    return user.pi

