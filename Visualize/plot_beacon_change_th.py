import json
import matplotlib.pyplot as plt
from Config.param_config import param
import matplotlib.ticker as ticker
from Visualize import read_data as rd
import numpy as np
import os

from map.individual_probability_map import Person
from OptBEACON.data_format import BeaconPerson
from OPSM.data_format import POI
from OptOPSM.opsm_fun import Vm as opsmVm
from OptBEACON.beacon_fun import Vm as beaconVm
from matplotlib import rcParams
from matplotlib.ticker import FuncFormatter, MaxNLocator


if __name__ == "__main__":
    opsm_user_path = "../document/opsm_result/USER_CHANGE/USER_CHANGE_1000_winner.json"
    opsm_poi_path = "../document/opsm_result/USER_CHANGE/USER_CHANGE_1000_POIs.json"
    all_user_path = "../document/probability/1000.json"
    beacon_change_threshol_path = "../document/beacon_change_threshold/"

    with open(all_user_path, 'r') as f:
        all_users = json.load(f)
        f.close()

    opsm_users = []
    opsm_pois = []
    with open(opsm_user_path, "r") as f:
        opsm_user = json.load(f)
        for user in opsm_user:
            for u in all_users:
                if user['id'] == u['id']:
                    uu = Person(attributes=u)
                    uu.pi = user['pi']
                    opsm_users.append(uu)
        f.close()
    with open(opsm_poi_path, "r") as f:
        opsm_poi = json.load(f)
        for poi in opsm_poi:
            opsm_pois.append(POI(poi['id'], poi['rm'], poi['vm']))
        f.close()

    opsm_total_value = 0
    opsm_total_payment = 0
    opsm_winner_num = len(opsm_users)
    for poi in opsm_pois:
        opsm_total_value += opsmVm({"winner": opsm_users}, poi)
    for user in opsm_users:
        opsm_total_payment += user.pi

    beacon_res = rd.plot_data_beacon_threshold(beacon_change_threshol_path)

    Y = {"total_value": [], "total_payment": [], "winner_num": []}
    for k in sorted(list(beacon_res.keys()), key=lambda kx: float(kx.split("_")[-1])):
        Y["total_value"].append(beacon_res[k]["total_value"])
        Y["total_payment"].append(beacon_res[k]["total_payment"])
        Y["winner_num"].append(beacon_res[k]["winner_num"])

    x = [_ for _ in range(3, 10)]
    x_index = list([np.around(float(i/10), 1) for i in range(3, 9)])
    x_index.append('O-PSM')

    # fig = plt.figure(figsize=[15, 5], dpi=200)
    config = {
        "font.family": 'Times New Roman',
        "font.size": 17,
        "mathtext.fontset": 'stix',
        "font.serif": ['SimSun'],
    }
    rcParams.update(config)

    width = 0.5
    fig1, ax1 = plt.subplots(figsize=[5, 5.2])
    # ax131 = fig.add_subplot(131)
    # plt.subplots_adjust(bottom=0.2)  # , wspace=0.25
    plt.bar(x, np.array([0 for i in range(3, 9)] + [opsm_total_value]) / 1000, width=width, label='O-PSM')
    plt.bar(x, np.array(Y["total_value"]+[0]) / 1000, width=width, label='Beacon')
    plt.xticks(x, x_index)
    plt.ylabel(r"Total Value $(\times10^3)$")
    plt.xlabel(r"Value of $\varepsilon$" + "\n(a)")
    plt.title(r"$M=641$, $N=1000$, $B=2\times10^4$")
    plt.legend(fontsize=15)
    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/thresholdchange/change_threshold_value.eps", bbox_inches='tight', pad_inches=0)

    fig2, ax2 = plt.subplots(figsize=[5, 5.2])
    # ax132 = fig.add_subplot(132)
    plt.bar(x, np.array([0 for i in range(3, 9)] + [opsm_total_payment]) / 1000, width=width, label='O-PSM')
    plt.bar(x, np.array(Y["total_payment"] + [0])/1000, width=width, label='Beacon')
    plt.ylim(1.7, 3.0)
    plt.xticks(x, x_index)
    plt.xlabel(r"Value of $\varepsilon$" + "\n(b)")
    plt.ylabel(r"Total Payment $(\times10^3)$")
    plt.title(r"$M=641$, $N=1000$, $B=2\times10^4$")
    plt.legend(fontsize=15)
    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/thresholdchange/change_threshold_pay.eps", bbox_inches='tight', pad_inches=0)

    fig3, ax3 = plt.subplots(figsize=[5, 5.2])
    # ax133 = fig.add_subplot(133)
    plt.bar(x, [0 for i in range(3, 9)] + [opsm_winner_num], width=width, label='O-PSM')
    plt.bar(x, Y["winner_num"] + [0], width=width, label='Beacon')
    plt.ylim(110, 138)
    plt.xticks(x, x_index)
    plt.xlabel(r"Value of $\varepsilon$" + "\n(c)")
    plt.ylabel("Number of Winner")
    plt.title(r"$M=641$, $N=1000$, $B=2\times10^4$")
    plt.legend(fontsize=15)

    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/thresholdchange/change_threshold_winner_number.eps", bbox_inches='tight', pad_inches=0)
    plt.show()




