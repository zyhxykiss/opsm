from Config.my_Enum import PersonalCharacter as PC
import json

param = {
    # opsm相关参数
    "budget": 20000,  # 预算
    
    # 数据生成器的相关参数
    "map_rows": 31,  # 地图行数
    "map_columns": 41,  # 地图列数
    "visit_upper_limit": 20,  # 每个点的最大访问次数
    "noise_upper_limit": 0.05,  # 概率噪声上限
    "sample_amount": 1000,  # 需要生成的样本数
    "stochastic_marginal_value_threshold": 0.6,  # 随机方法中的边缘密度门槛
    "processes": 10,  # 多进程使用的核心数量
    "stoch_try_times": 10,  #
    "beacon_threshold": 0.45,  # 在beacon的cover map中，若概率大于此值取1，否则取0

    "change_budget": [b for b in range(5000, 20000+1000, 1000)],
    "change_user": [u for u in range(200, 2000+200, 200)],
    "change_poi": [p for p in range(191, 641+50, 50)],

    "task_map_random": {"col": 1.5, "scale": 0.8, "min": 1, "max": 2},

    "loss_interval": {  # 不同性格的人概率向周围递减的正态分布参数
        PC.ESPECIALLY_INACTIVITY.value: {
            "col": 0.2, "scale": 0.1, "min": 0.2, "max": 0.32
        },

        PC.INACTIVITY.value: {
            "col": 0.2, "scale": 0.1, "min": 0.2, "max": 0.3
        },

        PC.ACTIVITY.value: {
            "col": 0.2, "scale": 0.1, "min": 0.15, "max": 0.28
        },

        PC.VERY_ACTIVITY.value: {
            "col": 0.15, "scale": 0.1, "min": 0.15, "max": 0.25
        },

        PC.HIGHLY_ACTIVITY.value: {
            "col": 0.15, "scale": 0.1, "min": 0.1, "max": 0.2
        }
    },

    "initiate_probability": {  # 不同性格的人在附加建筑上的初始概率的正态分布参数
        PC.ESPECIALLY_INACTIVITY.value: {
            "col": 0.55, "scale": 0.2, "min": 0.4, "max": 0.8
        },

        PC.INACTIVITY.value: {
            "col": 0.55, "scale": 0.2, "min": 0.4, "max": 0.8
        },

        PC.ACTIVITY.value: {
            "col": 0.6, "scale": 0.2, "min": 0.4, "max": 0.8
        },

        PC.VERY_ACTIVITY.value: {
            "col": 0.65, "scale": 0.2, "min": 0.4, "max": 0.8
        },

        PC.HIGHLY_ACTIVITY.value: {
            "col": 0.65, "scale": 0.2, "min": 0.4, "max": 0.8
        }
    },

    "academy_probability": {"col": 0.8, "scale": 0.3, "min": 0.4, "max": 0.8},  # 在学院附近的概率正态分布参数

    "tb_probability": {"col": 0.7, "scale": 0.3, "min": 0.4, "max": 0.8},  # 在教学楼附近的概率正态分布参数

    "bid_base": {  # 不同性格的人的要价基数
        PC.ESPECIALLY_INACTIVITY.value: 30,
        PC.INACTIVITY.value: 26,
        PC.ACTIVITY.value: 22,
        PC.VERY_ACTIVITY.value: 18,
        PC.HIGHLY_ACTIVITY.value: 14
    },

}

# sequence = []
# for i in range(1, 200):
#     x = 0
#     for j in range(1, i+1):
#         x += 1 / j
#     sequence.append(x)
# sequence = {"sequence": sequence}
# with open("../document/sequence/sequence.json", "w") as file:
#     json.dump(sequence, file)
#     file.close()

