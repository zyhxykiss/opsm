import json
import os
from map.individual_probability_map import Person
from OptBEACON.data_format import BeaconPerson
from OPSM.data_format import POI
from OptOPSM.opsm_fun import Vm as opsmVm
from OptBEACON.beacon_fun import Vm as beaconVm
from Reviewer.reviewer_fun import Vm as reviewerVm


def read_files(path):
    """
    将json文件读取为字典
    :param path: 该path不是某个具体json文件的path，而应该是json文件所在文件夹的路径
    :return: 格式
            user:
                {"key": [{...}, {...}, ...], "key": [{...}, {...}, ...], ...}
            POI:
                {"key": [{...}, {...}, ...], "key": [{...}, {...}, ...], ...}
    """
    if path[-1] != '/':
        path = path + '/'
    user_dict = {}
    poi_dict = {}
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        with open(file_path, 'r') as f:
            texture = json.load(f)
            f.close()
        if (file.split('.')[0]).split('_')[-1] == "POIs":
            poi_dict[file.split('.')[0]] = texture
        else:
            user_dict[file.split('.')[0]] = texture
    return user_dict, poi_dict


def plot_data_beacon_threshold(path):
    pois = {}
    users = {}
    all_user_path = "../document/probability/1000.json"

    with open(all_user_path, 'r') as f:
        all_users = json.load(f)
        f.close()

    for file_path in os.listdir(path):
        full_path = os.path.join(path, file_path)
        with open(full_path, 'r') as f:
            texture = json.load(f)
            f.close()
        if 'POIs' not in file_path:
            users[file_path.replace("_winner.json", "")] = []
            for u in texture:
                for user in all_users:
                    if u['id'] == user['id']:
                        acc_user = BeaconPerson(attributes=user, t=float(file_path.split("_")[-2]))
                        acc_user.pi = u["pi"]
                        users[file_path.replace("_winner.json", "")].append(acc_user)
        else:
            pois[file_path.replace("_POIs.json", "")] = []
            for poi in texture:
                pois[file_path.replace("_POIs.json", "")].append(POI(poi['id'], poi['rm'], poi['vm']))

    res = {}
    for k, v in users.items():
        res[k] = {}
        total_value = 0
        total_payment = 0
        for poi in pois[k]:
            total_value += beaconVm({"winner": v}, poi, t=float(k.split("_")[-1]))
        for user in v:
            total_payment += user.pi
        winner_num = len(v)
        res[k] = {"total_value": total_value, "total_payment": total_payment, "winner_num": winner_num}

    return res


def decode_poi(poi_files: dict):
    """
    将poi解析为POI类
    :param select:
    :param poi_files: 格式：{"key": [{...}, {...}, ...], "key": [{...}, {...}, ...], ...}
    :return: 格式：{"key": [], "key": [], ...}
    """
    res_dict = {}
    for k, v in poi_files.items():
        res_dict[k.replace("_POIs", "")] = []
        for poi in v:
            res_dict[k.replace("_POIs", "")].append(POI(poi['id'], poi['rm'], poi['vm']))
    return res_dict


"""
    将user解析为Person类
    :param change_param:
    :param method:
    :param user_file:文件列表,格式：{"key": [{...}, {...}, ...], "key": [{...}, {...}, ...], ...}
                                           user   user                 user   user
    :param select:
    :return: 格式：{"key": [user, user, ...], "key": [user, user, ...], ...}
    """


def decode_user(user_file: dict, change_param: str, select="", method='opsm'):
    res_dict = {}
    users_file_path = "../document/probability/"  # 初始用户文件
    select_maps_path = select  # 选择映射地图文件
    users_path = os.listdir(users_file_path)
    for k, v in user_file.items():
        res_dict[k.replace("_winner", "")] = []
        select_map_path = None
        if select != "":
            for smp in os.listdir(select_maps_path):
                if smp.split(".")[0].split("_")[-1] == k.split("_")[-1]:
                    select_map_path = os.path.join(select_maps_path, smp)
        user_file_path = ''
        if change_param == 'user':
            for user_path in users_path:
                if user_path.split('.')[0] == k.split('_')[-2]:
                    user_file_path = os.path.join(users_file_path, user_path)
        else:
            user_file_path = '../document/probability/1000.json'
        with open(user_file_path, 'r') as f:
            initiate_users = json.load(f)
            f.close()

        for user in v:

            p_user = None
            if (method == 'opsm') or (method == 'stoch') or (method == 'reviewer'):
                p_user = Person(attributes=initiate_users[user['id'] - 1], select_map=select_map_path)
            elif method == 'beacon':
                p_user = BeaconPerson(attributes=initiate_users[user['id'] - 1], select_map=select_map_path)
            p_user.pi = user['pi']
            p_user.marginal_value = user['marginal_value']
            p_user.marginal_density = user['marginal_density']
            res_dict[k.replace("_winner", "")].append(p_user)

    return res_dict


def plot_data_user_change(file_path: dict):
    """

    :param file_path:
        格式：{
                “opsm": user_file_path
                "beacon": user_file_path
                "stoch":{
                            "stoch_01": user_file_path
                                ......
                            "stoch_05: user_file_path
                        }
            }
    :return:
    """
    res = {}
    users = {}
    pois = {}
    for k, v in file_path.items():
        if k != "stoch":
            undecode_user, undecode_poi = read_files(v)
            users[k] = decode_user(undecode_user, "user", method=k)
            pois[k] = decode_poi(undecode_poi)
        else:
            users[k] = {}
            pois[k] = {}
            for sk, sv in v.items():
                stoch_undecode_user, stoch_undecode_poi = read_files(sv)
                users[k][sk] = decode_user(stoch_undecode_user, "user", method=k)
                pois[k][sk] = decode_poi(stoch_undecode_poi)

    for k, v in users.items():
        res[k] = {}
        if k != "stoch":
            for name, winner in v.items():
                total_value = 0
                total_payment = 0
                for poi in pois[k][name]:
                    if (k != "beacon") and (k != "reviewer"):
                        total_value += opsmVm({"winner": winner}, poi)
                    elif k == "reviewer":
                        total_value += opsmVm({"winner": winner}, poi)
                    else:
                        total_value += beaconVm({"winner": winner}, poi)
                for user in winner:
                    total_payment += user.pi
                win_num = len(winner)
                res[k][name] = {"total_value": total_value, "total_payment": total_payment, "win_rate": win_num}
        else:
            for sk, sv in v.items():
                for name, winner in sv.items():
                    if name not in list(res[k].keys()):
                        res[k][name] = {"total_value": 0, "total_payment": 0, "win_rate": 0}
                    total_value = 0
                    total_payment = 0
                    for poi in pois[k][sk][name]:
                        total_value += opsmVm({"winner": winner}, poi)
                    for user in winner:
                        total_payment += user.pi
                    win_num = len(winner)
                    res[k][name]['total_value'] += total_value / len(file_path['stoch'])
                    res[k][name]['total_payment'] += total_payment / len(file_path['stoch'])
                    res[k][name]['win_rate'] += win_num / len(file_path['stoch'])
    return res


def plot_data_budget_change(file_path: dict):
    """

    :param file_path:
        格式：{
                “opsm": user_file_path
                "beacon": user_file_path
                "stoch":{
                            "stoch_01": user_file_path
                                ......
                            "stoch_05: user_file_path
                        }
            }
    :return:
    """
    res = {}
    users = {}
    pois = {}
    for k, v in file_path.items():
        if k != "stoch":
            undecode_user, undecode_poi = read_files(v)
            users[k] = decode_user(undecode_user, "budget", "", method=k)
            pois[k] = decode_poi(undecode_poi)
        else:
            users[k] = {}
            pois[k] = {}
            for sk, sv in v.items():
                stoch_undecode_user, stoch_undecode_poi = read_files(sv)
                users[k][sk] = decode_user(stoch_undecode_user, "budget", "", method=k)
                pois[k][sk] = decode_poi(stoch_undecode_poi)

    for k, v in users.items():
        res[k] = {}
        if k != "stoch":
            for name, winner in v.items():
                total_value = 0
                total_payment = 0
                for poi in pois[k][name]:
                    if k != "beacon":
                        total_value += opsmVm({"winner": winner}, poi)
                    else:
                        total_value += beaconVm({"winner": winner}, poi)
                for user in winner:
                    total_payment += user.pi
                win_num = len(winner)
                res[k][name] = {"total_value": total_value, "total_payment": total_payment, "win_rate": win_num}
        else:
            for sk, sv in v.items():
                for name, winner in sv.items():
                    if name not in list(res[k].keys()):
                        res[k][name] = {"total_value": 0, "total_payment": 0, "win_rate": 0}
                    total_value = 0
                    total_payment = 0
                    for poi in pois[k][sk][name]:
                        total_value += opsmVm({"winner": winner}, poi)
                    for user in winner:
                        total_payment += user.pi
                    win_num = len(winner)
                    res[k][name]['total_value'] += total_value / len(file_path['stoch'])
                    res[k][name]['total_payment'] += total_payment / len(file_path['stoch'])
                    res[k][name]['win_rate'] += win_num / len(file_path['stoch'])
    return res


def plot_data_poi_change(file_path: dict):
    undecode_users = {}
    undecode_pois = {}
    res = {}

    select = {"01": '../document/InputData/POI_select_map_01',
              "02": '../document/InputData/POI_select_map_02',
              "03": '../document/InputData/POI_select_map_03',
              "04": '../document/InputData/POI_select_map_04',
              "05": '../document/InputData/POI_select_map_05'}
    for k, v in file_path.items():
        undecode_users[k] = {}
        undecode_pois[k] = {}
        for path in os.listdir(v):
            undecode_user, undecode_poi = read_files(os.path.join(v, path))
            undecode_users[k][path] = decode_user(undecode_user, 'poi', select=select[path.split("_")[-1]], method=k)
            undecode_pois[k][path] = decode_poi(undecode_poi)

    for k, v in undecode_users.items():
        res[k] = {}
        for pk, pv in v.items():
            for name, winner in pv.items():
                if name not in list(res[k].keys()):
                    res[k][name] = {"total_value": 0, "total_payment": 0, "win_rate": 0}
                total_value = 0
                total_payment = 0
                for poi in undecode_pois[k][pk][name]:
                    if k != "beacon":
                        total_value += opsmVm({"winner": winner}, poi)
                    else:
                        total_value += beaconVm({"winner": winner}, poi)
                for user in winner:
                    total_payment += user.pi
                win_num = len(winner)
                res[k][name]['total_value'] += total_value / len(select)
                res[k][name]['total_payment'] += total_payment / len(select)
                res[k][name]['win_rate'] += win_num / len(select)
    return res


# def decode_file_as_attribute(files: dict, *args):
#     """
#     解析文件, 不确定参数应该为需要返回的属性
#     :param files: 文件列表,格式：{"key": [{...}, {...}, ...], "key": [{...}, {...}, ...], ...}
#     :return:
#     """
#     decode_res = {}
#     for param in args:
#         decode_res[param] = []
#         for file in files:
#             for elem in file:
#                 try:
#                     decode_res[param].append(elem[param])
#                 except KeyError as ke:
#                     print(f"No such an attribute as <{param}>")
#     return decode_res


def data_pre(change_param='user', path=None):
    """
    画图数据准备，一次准备的数据为user/budget/poi变化的数据
    :param change_param:
    :param path: {'opsm': path, 'beacon': path, 'stoch': path}
    :return: users: {'opsm': {}, 'beacon': {}, 'stoch': {}}
            pois: {'opsm': {}, 'beacon': {}, 'stoch': {}}
    """
    users = {}  # {'opsm': [], 'beacon': [], 'stoch': []}
    pois = {}
    for k, v in path.items():
        undecode_users, undecode_pois = read_files(v)
        users[k] = decode_user(undecode_users, change_param, " ", method=k)
        pois[k] = decode_poi(undecode_pois)

    res = {}
    for k, v in users.items():
        res[k] = {}
        for name, winner in v.items():
            total_value = 0
            total_payment = 0
            for poi in pois[k][name]:
                if k != "beacon":
                    total_value += opsmVm({"winner": winner}, poi)
                else:
                    total_value += beaconVm({"winner": winner}, poi)
            for user in winner:
                total_payment += user.pi
            win_rate = len(winner) / float(name.split("_")[-1]) if change_param == 'user' else len(winner) / 1000
            res[k][name] = {"total_value": total_value, "total_payment": total_payment, "win_rate": win_rate}
    return res

# if __name__ == '__main__':
#     opsm_user_path = '../document/opsm_result/USER_CHANGE/'
#     beacon_user_path = '../document/beacon_result/USER_CHANGE/'
#
#     opsm_user, opsm_poi = read_files(opsm_user_path)
#     beacon_user, beacon_poi = read_files(beacon_user_path)
#
#     opsm_user_to_class = decode_user(opsm_user, method='opsm')
#     opsm_poi_to_class = decode_poi(opsm_poi)
#     beacon_user_to_class = decode_user(beacon_user, method='beacon')
#     print(0)

# opsm_user_attri = decode_file_as_attribute(opsm_user, 'charge', 'pi')
# beacon_user_attri = decode_file_as_attribute(beacon_user, 'charge', 'pi')
# count = 0
#
# for i in range(0, len(opsm_user_attri['charge'])):
#     if opsm_user_attri['charge'][i] > opsm_user_attri['pi'][i]:
#         count += 1
#         print(f"{count}th error!")
#         print(f'charge: {opsm_user_attri["charge"][i]} \t pi: opsm_user_attri["pi"][i]')
# print(count)
#
# count = 0
# for i in range(0, len(beacon_user_attri['charge'])):
#     if beacon_user_attri['charge'][i] > beacon_user_attri['pi'][i]:
#         count += 1
# print(count)
