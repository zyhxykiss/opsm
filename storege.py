from OPSM.data_format import POI
from map.individual_probability_map import Person
import json
import numpy as np
from OptBEACON.data_format import BeaconPerson


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


def storage_all(winner: list, POIs: dict, folder: str, change_param):
    file_prefix = folder.split('/')[-2] + '_' + str(change_param)
    save_winner = []
    save_POIs = []
    for user in winner:
        if isinstance(user, BeaconPerson):
            save_winner.append(user.beacon_to_dict())
        else:
            save_winner.append(user.to_dict_base())

    for poi in POIs.values():
        save_POIs.append(poi.to_dict())

    with open(folder+file_prefix+"_winner.json", "w") as file:
        json.dump(save_winner, file, cls=MyEncoder)
        file.close()

    with open(folder+file_prefix+"_POIs.json", "w") as file:
        json.dump(save_POIs, file, cls=MyEncoder)
        file.close()


def storage_observe_user(folder: str, observe_user: Person, charge):
    save_dict = observe_user.to_dict_base()
    with open(folder+ str(charge) + ".json", 'w') as file:
        json.dump(save_dict, file, cls=MyEncoder)
        file.close()