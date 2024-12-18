import numpy as np
import glob
import os
import json
import copy
def get_datapath(data_dir: str):
    """
    data_dir以下のrecorded_data_*.npyのパスを番号が小さい順に返す
    """
    return sorted(glob.glob(data_dir + 'recorded_data_*.npy')) # ファイル名のリストを返す

def main(data_dir: str):
    """
    1つのrecorded_data_*.npyからscenexのデータフォルダを作成する
    """
    data_paths = get_datapath(data_dir)
    for i, data_path in enumerate(data_paths):
        data_dtype = [
            ('timestamp', 'f8'),
            ('color', 'u1', (480, 640, 3)),
            ('depth', 'u2', (480, 640)),
            ('encoder', 'f4', (8,))
        ]
        print(data_path)
        data = np.memmap(data_path, dtype=data_dtype, mode='r')
        sub_dir = 'scene' + str(i+1)
        os.makedirs(data_dir + sub_dir, exist_ok=True)
        # print(data['timestamp'])
        for j in range(len(data)):
            # npyとして保存
            file_name = str(data['timestamp'][j]) + '.npy'
            save_data = {}
            # timestamp -> time
            save_data['time'] = float(data['timestamp'][j])
            # color -> image
            save_data['image'] = data['color'][j]
            save_data['depth'] = data['depth'][j]
            # encoder -> robot_left
            save_data['robot_left'] = data['encoder'][j][0:4] # 0,1,2,3
            # encoder -> robot_right
            save_data['robot_right'] = data['encoder'][j][4:8] # 4,5,6,7
            
            np.save(data_dir + sub_dir + '/' + file_name, save_data)
            
            # # 確認
            # print(data_dir + sub_dir + '/' + file_name)
            # data = np.load(data_dir + sub_dir + '/' + file_name)
            # print(data['timestamp'])
            # exit()
            
        # meta.jsonを作成
        timestamps = data['timestamp']
        start_time = timestamps[0] - 0.1
        stop_time = timestamps[-1] + 0.1
        meta = {
            'start_time': start_time,
            'stop_time': stop_time,
            'timestamps': timestamps.tolist()
        }
        with open(data_dir + sub_dir + '/meta.json', 'w') as f:
            json.dump(meta, f, indent=4)
        

if __name__ == '__main__':
    # data_dir = 'data/pick_box-in-the-wild/'
    data_dir = 'data/pick_box/'
    main(data_dir)
