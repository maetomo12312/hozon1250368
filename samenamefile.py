import os
import shutil

# 各フォルダのパス 1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845 short middle long
dir_main = "./Searchresult/GTshort_1-735"
dir_compare = "./Searchresult/Tshort-test_1-735-2"
dir_backup = "./Searchresult/Gshort-test_1-735"

# バックアップフォルダを作成（存在しない場合）
os.makedirs(dir_backup, exist_ok=True)

# `dir_compare` にあるCSVファイルのリストを取得
compare_files = set(f for f in os.listdir(dir_compare) if f.endswith(".csv"))

# `dir_main` 内のCSVファイルをチェックし、同じ名前のファイルが `dir_compare` にあるか確認
for filename in os.listdir(dir_main):
    if filename.endswith(".csv") and filename in compare_files:
        source_path = os.path.join(dir_main, filename)
        backup_path = os.path.join(dir_backup, filename)

        shutil.move(source_path, backup_path)  # ファイルを移動
        print(f"Moved: {filename} → {dir_backup}")

print("処理が完了しました。")
