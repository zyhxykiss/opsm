import matplotlib.pyplot as plt
from Config.param_config import param
import matplotlib.ticker as ticker
from Visualize import read_data as rd
import numpy as np
from matplotlib import rcParams


if __name__ == "__main__":
    user_change_path = {
        'opsm': '../document/opsm_result/POI_result/',
        'beacon': '../document/beacon_result/POI_result/',
        'stoch': '../document/stoch_result/POI_result/'
    }
    user_data = rd.plot_data_poi_change(user_change_path)

    # fig = plt.figure(figsize=[15, 5], dpi=200)
    config = {
        "font.family": 'Times New Roman',
        "font.size": 17,
        "mathtext.fontset": 'stix',
        "font.serif": ['SimSun'],
    }
    rcParams.update(config)

    fig1, ax1 = plt.subplots(figsize=[5, 5.2])
    # total_value
    labels = ["O-PSM", "Beacon", "Random"]
    # ax131 = fig.add_subplot(131)
    # plt.subplots_adjust(bottom=0.2)
    x = np.array(range(200, 601, 50))
    Y = {}
    for mk in user_data.keys():
        Y[mk] = []
        for k in sorted(user_data[mk].keys(), key=lambda kx: int(kx.split("_")[-1])):
            Y[mk].append(user_data[mk][k]['total_value'])
    i = 0
    for k, y in Y.items():
        plt.plot(x, np.array(y, dtype=int)[0:-1] / 1000, label=labels[i])
        i += 1
    plt.legend(fontsize=15)
    plt.xlabel("Number of POI\n(a)")
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(100))
    plt.ylabel(r"Total Value $(\times10^3)$")
    plt.title(r"$B=2\times10^4$, $N=1000$, $\varepsilon=0.45$")
    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/poichange/poi_change_winner_value.eps", bbox_inches='tight', pad_inches=0)

    # total_payment
    fig2, ax2 = plt.subplots(figsize=[5, 5.2])
    # ax132 = fig.add_subplot(132)
    # plt.subplots_adjust(bottom=0.2)
    Y = {}
    for mk in user_data.keys():
        Y[mk] = []
        for k in sorted(user_data[mk].keys(), key=lambda kx: int(kx.split("_")[-1])):
            Y[mk].append(user_data[mk][k]['total_payment'])
    width = 8
    ff = -1
    i = 0
    for k, y in Y.items():
        plt.bar(x - width * ff, np.array(y)[0:-1] / 1000, width=width, label=labels[i])
        ff += 1
        i += 1
    plt.legend(fontsize=15)
    plt.xlabel("Number of POI\n(b)")
    # ax132.xaxis.set_major_locator(ticker.MultipleLocator(100))
    plt.ylabel(r"Total Payment $(\times10^3)$")
    plt.ylim(1.21, 3.85)
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    plt.title(r"$B=2\times10^4$, $N=1000$, $\varepsilon=0.45$")
    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/poichange/poi_change_pay.eps", bbox_inches='tight', pad_inches=0)

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
        plt.bar(x + width * ff, y[0:-1], width=width, label=labels[i])
        ff += 1
        i += 1
    plt.legend(fontsize=15)
    plt.xlabel("Number of POI\n(c)")
    ax3.xaxis.set_major_locator(ticker.MultipleLocator(100))
    plt.ylabel(r"Number of Winner")
    plt.ylim(100, 145)
    plt.title(r"$B=2\times10^4$, $N=1000$, $\varepsilon=0.45$")

    plt.tight_layout()
    plt.savefig("../Visualize_single_fig/poichange/poi_change_winner_number.eps", bbox_inches='tight', pad_inches=0)
    plt.show()




