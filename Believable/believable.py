import json
from map.individual_probability_map import Person


def find_observe_user():
    user_path = './document/opsm_result/USER_CHANGE/USER_CHANGE_1000_winner.json'
    original_user_path = "./document/probability/1000.json"
    with open(user_path, 'r') as file:
        user_data = json.load(file)
        file.close()
    with open(original_user_path, 'r') as file:
        oru = json.load(file)
        file.close()
    return Person(attributes=oru[user_data[0]['id']-1])


def find_loser_user():
    winner_path = './document/opsm_result/USER_CHANGE/USER_CHANGE_1000_winner.json'
    users_path = './document/probability/1000.json'
    with open(winner_path, 'r') as file:
        user_data = json.load(file)
        file.close()
    with open(users_path, 'r') as file:
        oru = json.load(file)
        file.close()
    winner_id = []
    for _ in user_data:
        winner_id.append(_["id"])
    for user in oru:
        if (user["character"] == 5) and (user["id"] not in winner_id):
            return Person(attributes=user)






