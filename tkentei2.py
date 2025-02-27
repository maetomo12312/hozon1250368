import pandas as pd
import os
from scipy import stats

# ディレクトリ内の全てのCSVファイルから誤差データを取得する関数
def load_errors_from_directory(directory):
    errors = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            df = pd.read_csv(file_path)
            if "predicted_thinking_time" in df.columns and "thinking_time" in df.columns:
                errors.extend(df["predicted_thinking_time"] - df["thinking_time"])
    return errors

# 各フォルダのパス
dir_1 = "./predicted_results/TMPrate_L/"
dir_2 = "./predicted_results/TMPrate_M-L/"
dir_3 = "./predicted_results/TMPrate_H-L-4/"

# 各フォルダのデータを取得
errors_1 = load_errors_from_directory(dir_1)
errors_2 = load_errors_from_directory(dir_2)
errors_3 = load_errors_from_directory(dir_3)

# t検定の実施（3グループ間で比較）
print("=== t検定結果 ===")

t_stat, p_value = stats.ttest_ind(errors_1, errors_2, equal_var=False)
print(f"dir1 vs dir2: t値 = {t_stat}, p値 = {p_value}")
if p_value < 0.05:
    print("有意差あり（p < 0.05）")
else:
    print("有意差なし（p >= 0.05）")

t_stat, p_value = stats.ttest_ind(errors_1, errors_3, equal_var=False)
print(f"dir1 vs dir3: t値 = {t_stat}, p値 = {p_value}")
if p_value < 0.05:
    print("有意差あり（p < 0.05）")
else:
    print("有意差なし（p >= 0.05）")

t_stat, p_value = stats.ttest_ind(errors_2, errors_3, equal_var=False)
print(f"dir2 vs dir3: t値 = {t_stat}, p値 = {p_value}")
if p_value < 0.05:
    print("有意差あり（p < 0.05）")
else:
    print("有意差なし（p >= 0.05）")
