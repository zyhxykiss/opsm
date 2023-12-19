import matplotlib.pyplot as plt
from Config.param_config import param
import matplotlib.ticker as ticker
from Visualize import read_data as rd
import numpy as np
from matplotlib import rcParams


if __name__ == "__main__":
    user_change_path = {
        'opsm': '../document/opsm_result/BUDGET_CHANGE/',
        'beacon': '../document/beacon_result/BUDGET_CHANGE/',
        'stoch': {
            "stoch_01": "../document/stoch_result/stoch_result_01/BUDGET_CHANGE/",
            "stoch_02": "../document/stoch_result/stoch_result_02/BUDGET_CHANGE/",
            "stoch_03": "../document/stoch_result/stoch_result_03/BUDGET_CHANGE/",
            "stoch_04": "../document/stoch_result/stoch_result_04/BUDGET_CHANGE/",
            "stoch_05": "../document/stoch_result/stoch_result_05/BUDGET_CHANGE/",
            "stoch_06": "../document/stoch_result/stoch_result_06/BUDGET_CHANGE/",
            "stoch_07": "../document/stoch_result/stoch_result_07/BUDGET_CHANGE/",
            "stoch_08": "../document/stoch_result/stoch_result_08/BUDGET_CHANGE/",
            "stoch_09": "../document/stoch_result/stoch_result_09/BUDGET_CHANGE/",
            "stoch_010": "../document/stoch_result/stoch_result_010/BUDGET_CHANGE/",
            "stoch_011": "../document/stoch_result/stoch_result_011/BUDGET_CHANGE/",
            "stoch_012": "../document/stoch_result/stoch_result_012/BUDGET_CHANGE/",
            "stoch_013": "../document/stoch_result/stoch_result_013/BUDGET_CHANGE/",
            "stoch_014": "../document/stoch_result/stoch_result_014/BUDGET_CHANGE/",
            "stoch_015": "../document/stoch_result/stoch_result_015/BUDGET_CHANGE/",
            "stoch_016": "../document/stoch_result/stoch_result_016/BUDGET_CHANGE/",
            "stoch_017": "../document/stoch_result/stoch_result_017/BUDGET_CHANGE/",
            "stoch_018": "../document/stoch_result/stoch_result_018/BUDGET_CHANGE/",
            "stoch_019": "../document/stoch_result/stoch_result_019/BUDGET_CHANGE/",
            "stoch_020": "../document/stoch_result/stoch_result_020/BUDGET_CHANGE/",
            "stoch_021": "../document/stoch_result/stoch_result_021/BUDGET_CHANGE/",
            "stoch_022": "../document/stoch_result/stoch_result_022/BUDGET_CHANGE/",
            "stoch_023": "../document/stoch_result/stoch_result_023/BUDGET_CHANGE/",
            "stoch_024": "../document/stoch_result/stoch_result_024/BUDGET_CHANGE/",
            "stoch_025": "../document/stoch_result/stoch_result_025/BUDGET_CHANGE/",
            "stoch_026": "../document/stoch_result/stoch_result_026/BUDGET_CHANGE/",
            "stoch_027": "../document/stoch_result/stoch_result_027/BUDGET_CHANGE/",
        }
    }
    user_data = rd.plot_data_budget_change(user_change_path)

    # fig = plt.figure(figsize=[15, 5])
    labels = ["O-PSM", "Beacon", "Random"]
    config = {
        "font.family": 'Times New Roman',
        "font.size": 17,
        "mathtext.fontset": 'stix',
        "font.serif": ['SimSun'],
    }
    rcParams.update(config)

    # total_value
    fig1, ax1 = plt.subplots(figsize=[5, 5.2])
    # ax131 = fig.add_subplot(131)
    # plt.subplots_adjust(bottom=0.2)
    x = np.array([int(xi/1000) for xi in param["change_budget"]],dtype=int)
    Y = {}
    for mk in user_data.keys():
        Y[mk] = []
        for k in sorted(user_data[mk].keys(), key=lambda kx: int(kx.split("_")[-1])):
            Y[mk].append(user_data[mk][k]['total_value'])
    i = 0
    for k, y in Y.items():
        plt.plot(x, np.array(y, dtype=int) / 1000, label=labels[i])
        i += 1
    plt.legend(fontsize=15)
    plt.xlabel(r"Budget $(\times10^3)$"+"\n(a)")
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))
    plt.ylabel(r"Total Value $(\times10^3)$")
    plt.ylim(6.3, 12.4)
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.title(r"$M=641$, $N=1000$, $\varepsilon=0.45$")
    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/budgetchange/budget_change_value.eps", bbox_inches='tight', pad_inches=0)

    # total_payment
    width = 0.2
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
        plt.bar(x + (width * ff), np.array(y, dtype=int) / 1000, width=width, label=labels[i])
        ff += 1
        i += 1
    plt.legend(fontsize=15)
    plt.xlabel(r"Budget $(\times10^3)$"+"\n(b)")
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
    plt.ylabel(r"Total Payment $(\times10^3)$")
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    plt.ylim(0.98, 3.1)
    plt.title(r"$M=641$, $N=1000$, $\varepsilon=0.45$")
    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/budgetchange/budget_change_pay.eps", bbox_inches='tight', pad_inches=0)

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
        plt.bar(x + (width * ff), y, width=width, label=labels[i])
        ff += 1
        i += 1
    plt.legend(fontsize=15)
    plt.xlabel(r"Budget $(\times10^3)$"+"\n(c)")
    ax3.xaxis.set_major_locator(ticker.MultipleLocator(2))
    plt.ylabel("Number of Winner")
    plt.ylim(68, 130)
    plt.title(r"$M=641$, $N=1000$, $\varepsilon=0.45$")

    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/budgetchange/budget_change_winner_number.eps", bbox_inches='tight', pad_inches=0)
    plt.show()




