import pandas as pd
import os

# ディレクトリのパス1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845 
# short middle long
dir_source = "./Searchresult/Tlong_1688-2006-2/"
dir_source1 = "./Searchresult/Tlong_2007-2845-2/"
dir_target = "./Searchresult/Tlong-test_1688-2006-2/"
dir_target2 = "./Searchresult/Tlong-test_2007-2845-2/"
dir_output = "./predicted_results/ATL_H/"

# 出力ディレクトリを作成（存在しない場合）
os.makedirs(dir_output, exist_ok=True)

# "thinking_time" の平均を計算する関数
def calculate_mean_thinking_time(directories):
    thinking_times = []
    for directory in directories:
        for file in os.listdir(directory):
            if file.endswith(".csv"):
                file_path = os.path.join(directory, file)
                df = pd.read_csv(file_path)
                if "thinking_time" in df.columns:
                    thinking_times.extend(df["thinking_time"].dropna().tolist())
    return sum(thinking_times) / len(thinking_times) if thinking_times else None

# "thinking_time" の平均を計算
mean_thinking_time = calculate_mean_thinking_time([dir_source, dir_source1])

if mean_thinking_time is None:
    raise ValueError("thinking_time のデータが見つかりませんでした。")

print(f"計算された思考時間の平均: {mean_thinking_time}")

# test データに "predicted_thinking_time" を追加して保存する関数
def add_predicted_time_and_save(directories, output_dir, predicted_time):
    for directory in directories:
        for file in os.listdir(directory):
            if file.endswith(".csv"):
                file_path = os.path.join(directory, file)
                df = pd.read_csv(file_path)

                # "predicted_thinking_time" 列を追加
                df["predicted_thinking_time"] = predicted_time

                # 新しいファイルとして保存
                output_path = os.path.join(output_dir, file)
                df.to_csv(output_path, index=False)

# `predicted_thinking_time` を追加し、新しいファイルとして保存
add_predicted_time_and_save([dir_target, dir_target2], dir_output, mean_thinking_time)

print(f"処理が完了しました。予測結果は '{dir_output}' に保存されました。")
