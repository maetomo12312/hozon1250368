import os
import random
import shutil

# ディレクトリのパスを設定
source_dir = ".\\usistorage\\Trate_2007-2845_usi"
dest_dir1 = ".\\usistorage\\Trate_2007-2845_usiR"
dest_dir2 = ".\\usistorage\\Trate_2007-2845_usiZ"

# 出力先ディレクトリを作成
os.makedirs(dest_dir1, exist_ok=True)
os.makedirs(dest_dir2, exist_ok=True)

# すべての .usi ファイルを取得
usi_files = [f for f in os.listdir(source_dir) if f.endswith(".usi")]

# ランダムに 20000 個選択
random.shuffle(usi_files)
selected_files = usi_files[:20000]
remaining_files = usi_files[20000:]

# 選択したファイルを dest_dir1 に移動
for filename in selected_files:
    source_path = os.path.join(source_dir, filename)
    dest_path = os.path.join(dest_dir1, filename)
    shutil.move(source_path, dest_path)

# 残りのファイルを dest_dir2 に移動
for filename in remaining_files:
    source_path = os.path.join(source_dir, filename)
    dest_path = os.path.join(dest_dir2, filename)
    shutil.move(source_path, dest_path)

print(f"{len(selected_files)} files moved to {dest_dir1}")
print(f"{len(remaining_files)} files moved to {dest_dir2}")