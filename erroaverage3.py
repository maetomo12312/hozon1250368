import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_mse_and_visualize_error(directory_path, result_file):
    """
    指定されたディレクトリ内のすべてのCSVファイルについて、平均二乗誤差(MSE)を計算し、
    誤差の分布をヒストグラムで可視化し、最大・最小誤差の行を特定して結果をファイルに保存します。
    """
    all_errors = []  # 全誤差のリスト
    max_error_row = None  # 最大誤差の行
    min_error_row = None  # 最小誤差の行
    max_error = float('-inf')
    min_error = float('inf')
    
    with open(result_file, 'w') as f:
        for filename in os.listdir(directory_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory_path, filename)
                
                try:
                    df = pd.read_csv(file_path)

                    if 'predicted_thinking_time' in df.columns and 'thinking_time' in df.columns:
                        df['error'] = df['predicted_thinking_time'] - df['thinking_time']
                        df['squared_error'] = df['error'] ** 2  # 二乗誤差を計算
                        all_errors.extend(df['error'].tolist())  # 全誤差をリストに追加

                        # 最大誤差の更新
                        if df['error'].max() > max_error:
                            max_error = df['error'].max()
                            max_error_row = df.loc[df['error'].idxmax()]

                        # 最小誤差の更新
                        if df['error'].min() < min_error:
                            min_error = df['error'].min()
                            min_error_row = df.loc[df['error'].idxmin()]

                except Exception as e:
                    print(f"CSV読み込みエラー: {file_path}, エラー: {e}")
                    continue

        # 平均誤差（MAE）と平均二乗誤差（MSE）の計算
        if all_errors:
            mse = sum(err ** 2 for err in all_errors) / len(all_errors)
            mae = sum(abs(err) for err in all_errors) / len(all_errors)
        else:
            mse = 0
            mae = 0

        # 結果をファイルに書き込む
        f.write(f"平均二乗誤差 (MSE): {mse:.6f}\n")
        f.write(f"平均絶対誤差 (MAE): {mae:.6f}\n")

        # 最大・最小誤差の出力
        if max_error_row is not None:
            f.write(f"\n最大誤差: {max_error:.2f}\n")
            f.write(f"{max_error_row.to_string()}\n")
        if min_error_row is not None:
            f.write(f"\n最小誤差: {min_error:.2f}\n")
            f.write(f"{min_error_row.to_string()}\n")


# 使用するディレクトリパスを指定
test_dir_path = "./predicted_results4/DLPrate_H"
result_file_path = "./histogram7/DLPrate_H.txt"

calculate_mse_and_visualize_error(test_dir_path, result_file_path)
