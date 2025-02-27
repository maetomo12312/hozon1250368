import os
import pandas as pd
import shutil
# ディレクトリパス設定
usi_dir = "./usistorage/Trate_2007-2845_usiR"
csv_dir = "./Searchresult/Rrate_2007-2845-2"
#usi_dir = "./usistorage/a-test"
#csv_dir = "./Searchresult/a-test"

# 閾値の決定ルール 1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845
threshold_map = {0: 60, 1: 900, 2: 1800}

# CSVと対応するUSIファイルの処理
for csv_filename in os.listdir(csv_dir):
    if csv_filename.endswith(".csv"):
        csv_path = os.path.join(csv_dir, csv_filename)
        usi_filename = csv_filename.replace("SearchR_", "").replace(".csv", ".usi")
        usi_path = os.path.join(usi_dir, usi_filename)

        if not os.path.exists(usi_path):
            print(f"対応するUSIファイルが見つかりません: {usi_path}")
            continue

        # CSVファイルからルールの読み取り
        try:
            df_csv = pd.read_csv(csv_path)
            if "rule" in df_csv.columns:
                rule_value = df_csv["rule"].iloc[0]
                threshold = threshold_map.get(rule_value, 60)  # デフォルトは60
            else:
                print(f"CSVに'rule'列がありません: {csv_filename}")
                continue
        except Exception as e:
            print(f"CSVファイルの読み込みエラー: {csv_filename}, エラー: {e}")
            os.remove(csv_path)
            continue

        # USIファイルからthinking_timeを抽出
        try:
            odd_total_time = 0   # 奇数手合計
            even_total_time = 0  # 偶数手合計
            move_count = 0       # 手数カウント

            with open(usi_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("thinking_time"):
                        parts = line.strip().split()
                        if parts[-1].isdigit():  # 最も右の数値を取得
                            time_value = int(parts[-1])
                            move_count += 1  # 手数カウント

                            # 奇数手・偶数手に振り分け
                            if move_count % 2 == 1:
                                odd_total_time += time_value
                            else:
                                even_total_time += time_value

                            # どちらかが閾値を超えたか確認
                            if odd_total_time >= threshold or even_total_time >= threshold:
                                if move_count >= 40:
                                    # 40手以上なら move_count - 40 以降を削除
                                    rows_to_keep = move_count - 40
                                    df_csv = df_csv.iloc[:rows_to_keep]
                                    df_csv.to_csv(csv_path, index=False)
                                    print(f"{csv_filename}: {move_count}手目で閾値超過 → {rows_to_keep}行目以降削除")
                                else:
                                    # 40手未満ならファイルを削除
                                    os.remove(csv_path)
                                    print(f"{csv_filename}: {move_count}手目で閾値超過 → CSV削除")
                                break  # ループを抜ける

        except Exception as e:
            print(f"USIファイルの処理エラー: {usi_filename}, エラー: {e}")
            os.remove(csv_path)
            continue
