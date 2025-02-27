import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 出力フォルダの作成
output_dir = "./histogram5/GM_H"
os.makedirs(output_dir, exist_ok=True)

# bigerror.csv の読み込み
bigerror_df = pd.read_csv("./histogram5/GMbigerror_H.csv")

# 誤差を新しい列 'error' に追加
bigerror_df["error"] = bigerror_df["thinking_time"] - bigerror_df["predicted_thinking_time"]

# 各特徴量との相関係数を計算（thinking_time と predicted_thinking_time を除外）
correlation_matrix = bigerror_df.drop(columns=["thinking_time", "predicted_thinking_time"]).corr()
error_correlation = correlation_matrix["error"].sort_values(ascending=False)

# 統計情報の取得
error_stats = bigerror_df["error"].describe()

# 結果をテキストファイルに保存
text_output_path = os.path.join(output_dir, "GMbigerror_H.txt")
with open(text_output_path, "w") as f:
    f.write("=== 誤差との相関係数 ===\n")
    f.write(error_correlation.to_string())
    f.write("\n\n=== 誤差の統計情報 ===\n")
    f.write(error_stats.to_string())

# 誤差分布の可視化（PNG保存）
plt.figure(figsize=(8, 5))
sns.histplot(bigerror_df["error"], bins=20, kde=True)
plt.xlabel("error")
plt.ylabel("Frequency")
plt.title("Distribution of Errors")
plt.savefig(os.path.join(output_dir, "error_distribution.png"))  # PNGとして保存
plt.close()

# 各特徴量との散布図を作成（PNG保存）
features_to_check = ["cp", "previous_value", "previous_evaluation_value", "previous_poor_hand", 
                     "legal_move", "before_thinking_time", "long_thoughts", "first_piece_in_hand", "second_piece_in_hand"]

for feature in features_to_check:
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x=bigerror_df[feature], y=bigerror_df["error"])
    plt.xlabel(feature)
    plt.ylabel("error")
    plt.title(f"Relationship between error and {feature}")
    save_path = os.path.join(output_dir, f"error_vs_{feature}.png")
    plt.savefig(save_path)  # PNGとして保存
    plt.close()

print(f"解析結果を '{output_dir}' フォルダに保存しました。")
