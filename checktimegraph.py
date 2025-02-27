import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ディレクトリの設定
rrrate_dir = './Searchresult/short_2007-2845'
output_dir = './histhako'  # 図の保存先 1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845

# フォルダが存在しない場合は作成
os.makedirs(output_dir, exist_ok=True)

# thinking_time を格納するリスト
thinking_times = []

# CSVファイルを走査
for filename in os.listdir(rrrate_dir):
    if filename.endswith('.csv'):
        csv_path = os.path.join(rrrate_dir, filename)

        # CSVを読み込む
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
            if 'thinking_time' in df.columns:
                thinking_times.extend(df['thinking_time'].dropna().astype(int).tolist())
        except Exception as e:
            print(f"Error reading {filename}: {e}")

# データがない場合は終了
if not thinking_times:
    print("No thinking_time data found.")
else:
    # ヒストグラムを作成
    plt.figure(figsize=(10, 5))
    sns.histplot(thinking_times, bins=50, kde=True)
    plt.xlabel("Thinking Time")
    plt.ylabel("Frequency")
    plt.title("Distribution of Thinking Time")
    plt.grid(True)
    
    hist_path = os.path.join(output_dir, "histogram_short_2007-2845.png")
    plt.savefig(hist_path)  # 画像を保存
    plt.close()
    print(f"Histogram saved at: {hist_path}")

    # 箱ひげ図を作成
    plt.figure(figsize=(8, 4))
    sns.boxplot(x=thinking_times)
    plt.xlabel("Thinking Time")
    plt.title("Boxplot of Thinking Time")
    plt.grid(True)

    boxplot_path = os.path.join(output_dir, "boxplot_short_2007-2845.png")
    plt.savefig(boxplot_path)  # 画像を保存
    plt.close()
    print(f"Boxplot saved at: {boxplot_path}")
