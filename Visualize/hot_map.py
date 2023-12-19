import seaborn as sns
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams


path = "../document/probability/1000.json"

with open(path, 'r') as f:
    users = json.load(f)
    f.close()

user = None

for u in users:
    if u["character"] == 5:
        user = u

opsm_map = np.around(np.array(user["probability_map"]), 2)
beacon_map = np.array(np.zeros(opsm_map.shape[0] * opsm_map.shape[1])).reshape(opsm_map.shape)
for i in range(opsm_map.shape[0]):
    for j in range(opsm_map.shape[1]):
        beacon_map[i, j] = 1 if opsm_map[i, j] >= 0.45 else 0

# plt.rc("font", family="Times New Roman")
config = {
"font.family":'Times New Roman',
"font.size": 13,
"mathtext.fontset":'stix',
"font.serif": ['SimSun'],
}
rcParams.update(config)

fig1 = plt.figure(figsize=[5, 3.5])
# ax121 = fig.add_subplot(211)
# plt.subplots_adjust(bottom=0)
ax = sns.heatmap(opsm_map)
ax.axes.xaxis.set_ticks([])
ax.axes.yaxis.set_ticks([])
# plt.xlabel("Coverage probability heatmap for O-PSM\n(a)", fontsize=14)
plt.tight_layout()
plt.savefig("../Visualize_single_fig/hotmap/hot_opsm.pdf", bbox_inches='tight', pad_inches=0)

fig2 = plt.figure(figsize=[5, 3.5])
# ax122 = fig.add_subplot(212)
# plt.subplots_adjust(bottom=0)
ax = sns.heatmap(beacon_map)
ax.axes.xaxis.set_ticks([])
ax.axes.yaxis.set_ticks([])
# plt.xlabel("Coverage heatmap for Beacon, " + r"$\varepsilon=0.45$" +"\n(b)", fontsize=14)

plt.tight_layout()
plt.savefig("../Visualize_single_fig/hotmap/hot_beacon.pdf", bbox_inches='tight', pad_inches=0)
plt.show()
