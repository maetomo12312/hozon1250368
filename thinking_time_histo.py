import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_thinking_time_from_directory(directory_path):
    """
    指定されたディレクトリからすべてのCSVファイルを読み込み、thinking_time のリストを作成する。
    """
    all_thinking_times = []

    if not os.path.exists(directory_path):
        print(f"ディレクトリが存在しません: {directory_path}")
        return []

    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            try:
                df = pd.read_csv(file_path)
                if "thinking_time" in df.columns:
                    all_thinking_times.extend(df["thinking_time"].dropna().tolist())
            except Exception as e:
                print(f"{file_path} の読み込み中にエラーが発生しました: {e}")

    return all_thinking_times

# 処理対象のディレクトリ
directories = [
    "./Searchresult/Tlong_2007-2845-2",
    "./Searchresult/Tlong_1688-2006-2",
    "./Searchresult/Tlong-test_2007-2845-2",
    "./Searchresult/Tlong-test_1688-2006-2"
]

# すべてのディレクトリから thinking_time を取得
all_thinking_times = []
for dir_path in directories:
    all_thinking_times.extend(load_thinking_time_from_directory(dir_path))

# データが空でないか確認
if not all_thinking_times:
    print("thinking_time のデータが見つかりません。処理を終了します。")
    exit()

# ヒストグラムをプロット（1秒ごとに集計）
plt.figure(figsize=(12, 6))
sns.histplot(all_thinking_times, bins=range(int(min(all_thinking_times)), int(max(all_thinking_times)) + 2), kde=False, color="blue")

# 軸ラベルとタイトルの設定
plt.xlabel("Thinking Time (seconds)")
plt.ylabel("Frequency")
plt.title("Thinking Time Distribution (1-second intervals)")

# X 軸の目盛りを 5秒ごとに表示
plt.xticks(range(int(min(all_thinking_times)), int(max(all_thinking_times)) + 1, 5))

# グラフを保存
output_path = "./Searchresult/png/TL-H.png"
plt.savefig(output_path, bbox_inches="tight")
plt.show()

print(f"thinking_time の分布を {output_path} に保存しました。")
