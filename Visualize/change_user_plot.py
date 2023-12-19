import matplotlib.pyplot as plt
from Config.param_config import param
import matplotlib.ticker as ticker
from Visualize import read_data as rd
import numpy as np
from matplotlib import rcParams


if __name__ == "__main__":
    user_change_path = {
        'opsm': '../document/opsm_result/USER_CHANGE/',
        'beacon': '../document/beacon_result/USER_CHANGE/',
        # 'beacon': '../document/beacon_result/USER_CHANGE/',
        'stoch': {
            "stoch_01": "../document/stoch_result/stoch_result_01/USER_CHANGE",
            "stoch_02": "../document/stoch_result/stoch_result_02/USER_CHANGE",
            "stoch_03": "../document/stoch_result/stoch_result_03/USER_CHANGE",
            "stoch_04": "../document/stoch_result/stoch_result_04/USER_CHANGE",
            "stoch_05": "../document/stoch_result/stoch_result_05/USER_CHANGE",
        }
    }
    user_data = rd.plot_data_user_change(user_change_path)

    # fig = plt.figure(figsize=[15, 5], dpi=200)
    labels = ["O-PSM", "Beacon", "Random"]

    config = {
        "font.family": 'Times New Roman',
        "font.size": 17,
        "mathtext.fontset": 'stix',
        "font.serif": ['SimSun'],
    }
    rcParams.update(config)

    # total_value
    width = 40
    fig1, ax1 = plt.subplots(figsize=[5, 5.2])
    # ax131 = fig.add_subplot(131)
    # plt.subplots_adjust(bottom=0.2)
    x = np.array(param["change_user"], dtype=int)
    Y = {}
    for mk in user_data.keys():
        Y[mk] = []
        for k in sorted(user_data[mk].keys(), key=lambda kx: int(kx.split("_")[-1])):
            Y[mk].append(user_data[mk][k]['total_value'])
    i = 0
    for k, y in Y.items():
        plt.plot(x, np.array(y, dtype=int)/1000, label=labels[i])
        i += 1
    plt.legend(fontsize=15)
    plt.xlabel("Number of User\n(a)")
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(400))
    plt.ylabel(r"Total Value $(\times10^3)$")
    plt.ylim(6.5, 13)
    plt.title(r"$B=2\times10^4$, $M=641$, $\varepsilon=0.45$")
    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/userchange/user_change_value.pdf", bbox_inches='tight', pad_inches=0)

    # total_payment
    fig2, ax2 = plt.subplots(figsize=[5, 5.2])
    # ax132 = fig.add_subplot(132)
    # plt.subplots_adjust(bottom=0.2)
    Y = {}
    for mk in user_data.keys():
        Y[mk] = []
        for k in sorted(user_data[mk].keys(), key=lambda kx: int(kx.split("_")[-1])):
            Y[mk].append(user_data[mk][k]['total_payment'])
    ff = -1
    i = 0
    for k, y in Y.items():
        plt.bar(x + (width * ff), np.array(y, dtype=int)/1000, width=width, label=labels[i])
        ff += 1
        i += 1
    plt.legend(fontsize=15)
    plt.xlabel("Number of User\n(b)")
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(400))
    plt.ylim(1.6, 4.1)
    plt.ylabel(r"Total Payment $(\times10^3)$")
    plt.title(r"$B=2\times10^4$, $M=641$, $\varepsilon=0.45$")
    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/userchange/user_change_pay.pdf", bbox_inches='tight', pad_inches=0)

    # win_rate
    fig3, ax3 = plt.subplots(figsize=[5, 5.2])
    # ax133 = fig.add_subplot(133)
    # plt.subplots_adjust(bottom=0.2)
    Y = {}
    for mk in user_data.keys():
        Y[mk] = []
        for k in sorted(user_data[mk].keys(), key=lambda kx: int(kx.split("_")[-1])):
            Y[mk].append(user_data[mk][k]['win_rate'])
    ff = -1
    i = 0
    for k, y in Y.items():
        plt.bar(x + (width*ff), y, width=width, label=labels[i])
        ff += 1
        i += 1
    plt.legend(fontsize=15)
    plt.xlabel("Number of User\n(c)")
    ax3.xaxis.set_major_locator(ticker.MultipleLocator(400))
    plt.ylabel("Number of Winners")
    plt.title(r"$B=2\times10^4$, $M=641$, $\varepsilon=0.45$")
    plt.ylim(87, 139)

    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/userchange/user_change_winner_number.pdf", bbox_inches='tight', pad_inches=0)
    # plt.savefig("../Visualize_fig/user_change_200-2000_0.6.jpg")





