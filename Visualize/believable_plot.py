import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams


winner_observe_user_path = "../document/believable_result/winner/observe_USER"
winner_users_path = "../document/believable_result/winner/winner_POIs"
lose_observe_user_path = "../document/believable_result/loser/observe_USER"
lose_user_path = "../document/believable_result/loser/winner_POIs"
all_user_path = "../document/probability/1000.json"
win_ob = 0
los_ob = 0
ob_win_charge = 0
ob_lose_charge = 0

for path in os.listdir(winner_observe_user_path):
    full_path = os.path.join(winner_observe_user_path, path)
    with open(full_path, 'r') as f:
        win_ob = json.load(f)["id"]
        f.close()
    break

for path in os.listdir(lose_observe_user_path):
    full_path = os.path.join(lose_observe_user_path, path)
    with open(full_path, 'r') as f:
        los_ob = json.load(f)["id"]
        f.close()
    break

with open(all_user_path, 'r') as f:
    all_users = json.load(f)
    f.close()
    for user in all_users:
        if user["id"] == win_ob:
            ob_win_charge = user["charge"]
        elif user["id"] == los_ob:
            ob_lose_charge = user["charge"]
print("lose_charge: " + str(ob_lose_charge)+"\n"+"winner charge: " + str(ob_win_charge))

win_dir = os.listdir(winner_users_path)
win_dir = sorted(win_dir, key=lambda x: int((x.split("_")[2].split(".")[0])))

los_dir = os.listdir(lose_user_path)
los_dir = sorted(los_dir, key=lambda x: int((x.split("_")[2].split(".")[0])))

win_x = [float(_) for _ in range(6, 40, 4)]
lose_x = [float(_) for _ in range(6, 40, 4)]
win_critical_payment = 21.2554
lose_critical_payment = 17.5673
for i in range(len(win_x)):
    if win_x[i] < win_critical_payment and (win_x[i+1] > win_critical_payment):
        win_x.insert(i + 1, win_critical_payment)
        win_x.insert(i + 1, win_critical_payment)
        break

for i in range(len(lose_x)):
    if lose_x[i] < lose_critical_payment and (lose_x[i+1] > lose_critical_payment):
        lose_x.insert(i + 1, lose_critical_payment)
        lose_x.insert(i + 1, lose_critical_payment)
        break

win_y = []
for i in range(len(win_x)):
    if win_x[i] < win_critical_payment:
        win_y.append(win_critical_payment - ob_win_charge)
    elif win_x[i] == win_critical_payment:
        win_y.append(win_critical_payment - ob_win_charge)
        win_y += [0 for _ in range(i+1, len(win_x))]
        break

# for path in win_dir:
#     if "POIs." in path:
#         continue
#     full_path = os.path.join(winner_users_path, path)
#     with open(full_path, 'r') as f:
#         users = json.load(f)
#         f.close()
#     for i in range(0, len(users)):
#         if users[i]["id"] == win_ob:
#             # marginal_vlaue_density.append(np.around(users[i]["marginal_density"], 2))
#             break

lose_y = []
for i in range(len(lose_x)):
    if lose_x[i] < lose_critical_payment:
        lose_y.append(lose_critical_payment - ob_lose_charge)
    elif lose_x[i] == lose_critical_payment:
        lose_y.append(lose_critical_payment - ob_lose_charge)
        lose_y += [0 for _ in range(i+1, len(lose_x))]
        break

# plt.rc("font", family="Times New Roman")
config = {
"font.family":'Times New Roman',
"font.size": 13,
"mathtext.fontset":'stix',
"font.serif": ['SimSun'],
}
rcParams.update(config)

fig1, ax1 = plt.subplots(figsize=[5, 3.8])
# fig1 = plt.figure(figsize=[5, 4], dpi=200)
# ax121 = fig.add_subplot(211)
# plt.subplots_adjust(hspace=-0.1)
plt.plot(win_x, win_y, color="red", linestyle="--", marker="*")
ax1.yaxis.set_major_locator(ticker.MultipleLocator(4))
ax1.xaxis.set_major_locator(ticker.MultipleLocator(5))
plt.ylim(-3.9, 18.5)
plt.xlabel("Bid of User 6 (Win)", fontsize=14)
plt.ylabel("Utility of User 6 (Win)")
plt.title(r"$M=641$, $N=1000$, $B=2\times10^4$")
plt.tight_layout()
plt.savefig("../Visualize_single_fig/truthverify/believable_winner.pdf", bbox_inches='tight', pad_inches=0.05)

fig2, ax2 = plt.subplots(figsize=[5, 3.8])
# fig = plt.figure(figsize=[5, 4], dpi=200)
# ax122 = fig.add_subplot(212)
plt.plot(lose_x, lose_y, color="green", linestyle="--", marker="*")
ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax2.xaxis.set_major_locator(ticker.MultipleLocator(5))
plt.ylim(-5.2, 1.2)
plt.xlabel("Bid of User 2 (Lose)", fontsize=14)
plt.ylabel("Utility of User 2 (Lose)")
plt.title(r"$M=641$, $N=1000$, $B=2\times10^4$")

plt.tight_layout()
plt.savefig("../Visualize_single_fig/truthverify/believable_loser.pdf", bbox_inches='tight', pad_inches=0.05)
plt.show()




