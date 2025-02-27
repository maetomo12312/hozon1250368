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

# thinking_time を10%ごとの範囲に分割
percentiles = np.percentile(all_thinking_times, np.arange(0, 110, 10))  # 0% から 100% まで 10% 刻み
percentile_labels = [f"{int(p1)} - {int(p2)}" for p1, p2 in zip(percentiles[:-1], percentiles[1:])]

# 各範囲のデータ数をカウント
percentile_counts = np.histogram(all_thinking_times, bins=percentiles)[0]

# データを DataFrame に変換
df_percentiles = pd.DataFrame({
    "Range": percentile_labels,
    "Count": percentile_counts
})

# ヒストグラムをプロット
plt.figure(figsize=(12, 6))
sns.barplot(x="Range", y="Count", data=df_percentiles, palette="viridis")
plt.xticks(rotation=45)
plt.xlabel("Thinking Time Percentile Ranges")
plt.ylabel("Frequency")
plt.title("Thinking Time Distribution (10% Percentiles)")

# グラフを保存
output_path = "./Searchresult/png/TL-H.png"
plt.savefig(output_path, bbox_inches="tight")
plt.show()

print(f"thinking_time の分布を {output_path} に保存しました。")
