import pandas as pd
import os
from scipy import stats

# データを格納するリストdir_2
errors_1 = []
errors_2 = []

# ディレクトリ内の全てのCSVファイルを読み込む関数
def load_errors_from_directory(directory):
    errors = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            df = pd.read_csv(file_path)
            if "predicted_thinking_time" in df.columns and "thinking_time" in df.columns:
                errors.extend(df["predicted_thinking_time"] - df["thinking_time"])
    return errors

# 各フォルダのデータを取得
dir_1 = "./predicted_results/TSPrate_H-4/"
dir_2 = "./predicted_results/ATS_H/"

errors_1 = load_errors_from_directory(dir_1)
errors_2 = load_errors_from_directory(dir_2)

# t検定（独立した2標本 t検定）
t_stat, p_value = stats.ttest_ind(errors_1, errors_2, equal_var=False)

# 結果の出力
print(f"t値: {t_stat}")
print(f"p値: {p_value}")

# 有意水準5%での判定
if p_value < 0.05:
    print("有意差あり（p < 0.05）")
else:
    print("有意差なし（p >= 0.05）")
