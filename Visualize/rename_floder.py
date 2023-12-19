import os

user_change_path = {
        'opsm': '../document/opsm_result/POI_result/',
        'beacon': '../document/beacon_result/POI_result/',
        'stoch': '../document/stoch_result/POI_result/'
    }

for k, v in user_change_path.items():
    for path in os.listdir(v):
        files_path = os.path.join(v, path)
        for file_path in os.listdir(files_path):
            new_name = file_path.replace(f"_{path.split('_')[-1]}", "")
            os.rename(os.path.join(files_path, file_path), os.path.join(files_path, new_name))