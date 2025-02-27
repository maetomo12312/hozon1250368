import os
import shutil

# 元フォルダと出力フォルダのパスを指定 1-735 736-1077 1078-1374 1375-1687 1688-2006 2007-2845
source_folder = './usistorage/Trate_1-735_usiZ'
destination_folders = [
    './usistorage/Trate_1-735_usiZ1',
    './usistorage/Trate_1-735_usiZ2',
    './usistorage/Trate_1-735_usiZ3',
    './usistorage/Trate_1-735_usiZ4'
]

# 出力フォルダが存在しない場合は作成
for folder in destination_folders:
    os.makedirs(folder, exist_ok=True)

# USIファイルのリストを取得
usi_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

# ファイルの総数と分割サイズを計算
num_files = len(usi_files)
chunk_size = (num_files + 3) // 4  # 4分割のサイズ

# ファイルを分割してコピー
for i, folder in enumerate(destination_folders):
    start_index = i * chunk_size
    end_index = min(start_index + chunk_size, num_files)
    for file_name in usi_files[start_index:end_index]:
        src_path = os.path.join(source_folder, file_name)
        dest_path = os.path.join(folder, file_name)
        shutil.copy(src_path, dest_path)

print(f"{num_files} files have been split into 4 parts.")