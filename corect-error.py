import pandas as pd
import os
import glob

# フォルダのパス
folder_path = "./predicted_results/SPrate_L/"

# CSV ファイルの取得
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# 全データの集計用
total_count = 0
correct_count = 0

# 各ファイルの処理
for file in csv_files:
    df = pd.read_csv(file)
    
    # thinking_time と predicted_thinking_time の絶対誤差を計算
    df["error"] = abs(df["thinking_time"] - df["predicted_thinking_time"])
    
    # 5秒以内の誤差のデータ数をカウント
    correct_count += (df["error"] <= 6).sum()
    
    # 全体のデータ数をカウント
    total_count += len(df)

# 正解率の計算
accuracy = correct_count / total_count if total_count > 0 else 0

print(f"x秒以内の正解率: {accuracy:.4f} ({correct_count}/{total_count})")
