import pandas as pd
import os
import numpy as np
from scipy import stats

# ディレクトリ内のすべてのCSVファイルから MSE データを取得する関数
def load_mse_from_directory(directory):
    mse_values = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            df = pd.read_csv(file_path)
            if "predicted_thinking_time" in df.columns and "thinking_time" in df.columns:
                errors_squared = (df["predicted_thinking_time"] - df["thinking_time"]) ** 2
                mse_values.extend(errors_squared)
    return np.array(mse_values)

# ブートストラップ法で MSE の信頼区間を計算
def bootstrap_confidence_interval(data, num_samples=10000, confidence_level=0.95):
    bootstrap_samples = np.random.choice(data, (num_samples, len(data)), replace=True).mean(axis=1)
    lower_bound = np.percentile(bootstrap_samples, (1 - confidence_level) / 2 * 100)
    upper_bound = np.percentile(bootstrap_samples, (1 + confidence_level) / 2 * 100)
    return lower_bound, upper_bound

# 各フォルダのパス
dir_1 = "./predicted_results/TLPrate_H4/"
dir_2 = "./predicted_results/TLPrate_L-H-4/"
dir_3 = "./predicted_results/TLPrate_M-H-4/"

# 各フォルダのデータを取得（MSE）
mse_1 = load_mse_from_directory(dir_1)
mse_2 = load_mse_from_directory(dir_2)
mse_3 = load_mse_from_directory(dir_3)

# MSE のブートストラップ信頼区間を計算
ci_1 = bootstrap_confidence_interval(mse_1)
ci_2 = bootstrap_confidence_interval(mse_2)
ci_3 = bootstrap_confidence_interval(mse_3)

# ブートストラップの結果を表示
print("=== MSE のブートストラップ信頼区間 ===")
print(f"dir1: {ci_1}")
print(f"dir2: {ci_2}")
print(f"dir3: {ci_3}")

# F検定（MSEの分散の違いを検定）
print("\n=== MSE の分散に対する F検定 ===")
f_stat, p_value = stats.levene(mse_1, mse_2)
print(f"dir1 vs dir2: F値 = {f_stat}, p値 = {p_value}")
if p_value < 0.05:
    print("有意差あり（p < 0.05）")
else:
    print("有意差なし（p >= 0.05）")

f_stat, p_value = stats.levene(mse_1, mse_3)
print(f"dir1 vs dir3: F値 = {f_stat}, p値 = {p_value}")
if p_value < 0.05:
    print("有意差あり（p < 0.05）")
else:
    print("有意差なし（p >= 0.05）")

f_stat, p_value = stats.levene(mse_2, mse_3)
print(f"dir2 vs dir3: F値 = {f_stat}, p値 = {p_value}")
if p_value < 0.05:
    print("有意差あり（p < 0.05）")
else:
    print("有意差なし（p >= 0.05）")
