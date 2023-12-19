from OPSM import data_format
from Config.param_config import param
from OptOPSM import opsm_fun
import numpy as np
import pandas as pd
from map.individual_probability_map import Person
from OPSM.data_format import POI
import copy
import json


def allocation_stage(USER: dict, POIs: dict, log_display=False, budget=param["budget"], seq=None):
    winner = {}
    winner = {"winner": [], "total_value": 0}

    winner_num = 0
    max_dv_user = opsm_fun.find_max_value_user(USER, winner, POIs, True, seq)  # dv 为 density value 的缩写
    while (max_dv_user.id != 0) and (max_dv_user.charge <= opsm_fun.threshold(winner, max_dv_user, POIs, budget, seq)):
        winner["winner"].append(max_dv_user)
        max_dv_user.allocated = 1
        winner_num += 1
        # print(f"Round {winner_num + 1}")
        max_dv_user = opsm_fun.find_max_value_user(USER, winner, POIs, True, seq)

    print(f"winner list length is {len(winner['winner'])}\t member is {[user.id for user in winner['winner'][0:5]]}...")

    total_value = 0
    if log_display:
        for user in winner['winner']:
            if user.id != 0:
                total_value += user.marginal_value
                print(f"user {user.id}  marginal_value is {user.marginal_value}, marginal_density "
                      f"is {user.marginal_density}")
        print(f"Total value of USERs is {total_value}")

    return winner


def payment_stage(USER: dict, POIs: dict, user: Person, winner: dict, log_display=False, budget=param['budget'], seq=None):
    if log_display:
        print(f"\nCalculate user {user.id} payment")
    min = 0
    round = 0
    user_prime = copy.deepcopy(USER)
    user_prime.pop(user.id)
    for u in user_prime.values():
        u.allocated = 0
    winner_primer = {"winner": [], "total_value": 0}
    max_user = opsm_fun.find_max_value_user(user_prime, winner_primer, POIs, seq=seq)

    while (max_user.charge < opsm_fun.threshold(winner_primer, max_user, POIs, budget, seq)) and (max_user.id != 0):
        min = opsm_fun.min_pi(winner_primer, user, max_user, POIs, budget, seq)
        if log_display:
            print(f"min p{user.id}({max_user.id}) is {min}")

        if user.pi < min:
            user.pi = min
        round += 1
        winner_primer['winner'].append(max_user)
        winner_primer['total_value'] += max_user.marginal_value
        max_user.allocated = 1
        max_user = opsm_fun.find_max_value_user(user_prime, winner_primer, POIs, seq=seq)
    if user == winner["winner"][-1]:
        if user.pi < user.charge:
            user.pi = user.charge
    return user.pi
