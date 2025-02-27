import os
import shutil

# 元のディレクトリとバックアップ先のディレクトリを指定 1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845
# short middle long 
source_dir = "./Searchresult/GRrate_2007-2845"
backup_dir = "./Searchresult/GRrate_2007-2845-2"

# バックアップフォルダを作成（存在しない場合）
os.makedirs(backup_dir, exist_ok=True)

# CSVファイルをコピー
for filename in os.listdir(source_dir):
    if filename.endswith(".csv"):
        src_path = os.path.join(source_dir, filename)
        dst_path = os.path.join(backup_dir, filename)
        shutil.copy2(src_path, dst_path)  # メタデータも保持するコピー

print(f"バックアップ完了: {backup_dir} に {len(os.listdir(backup_dir))} 個のファイルをコピーしました。")
