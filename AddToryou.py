#棋譜データに投了を追加するコードであった
import argparse
import re   
import os
import shutil
from tqdm import tqdm

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description= "AddToryo.py")
parser.add_argument("input_folder")

args = parser.parse_args()

counter = 1

# 進捗バーを作成
file_list = os.listdir(args.input_folder)
progress_bar = tqdm(total=len(file_list), desc="Processing Files")

def append_to_file(file_path, content_to_append):
    with open(file_path, 'a') as file:
        file.write(content_to_append)
        
for filename in os.listdir(args.input_folder):
    file_path = os.path.join(args.input_folder, filename)
    append_to_file(file_path, '%TORYO')
    
    # 進捗バーを更新
    progress_bar.update(1)


# 進捗バーを閉じる
progress_bar.close()
print("追加完了")
    
    
