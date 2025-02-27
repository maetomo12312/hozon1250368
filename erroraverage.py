import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_and_visualize_error(directory_path, result_file, plot_file):
    """
    指定されたディレクトリ内のすべてのCSVファイルについて、誤差の平均を計算し、誤差の分布をヒストグラムで可視化し、
    最大・最小誤差の行を特定して結果をファイルに保存します。
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
                df = pd.read_csv(file_path)
                
                if 'predicted_thinking_time' in df.columns and 'thinking_time' in df.columns:
                    df['error'] = df['predicted_thinking_time'] - df['thinking_time']
                    all_errors.extend(df['error'].tolist())  # 全誤差をリストに追加
                    
                    # 最大誤差の更新
                    if df['error'].max() > max_error:
                        max_error = df['error'].max()
                        max_error_row = df.loc[df['error'].idxmax()]

                    # 最小誤差の更新
                    if df['error'].min() < min_error:
                        min_error = df['error'].min()
                        min_error_row = df.loc[df['error'].idxmin()]

        # 平均誤差の計算
        mean_error = sum(abs(err) for err in all_errors) / len(all_errors) if all_errors else 0
        f.write(f"誤差の平均: {mean_error}\n")
        
        # 最大・最小誤差の出力
        if max_error_row is not None:
            f.write(f"\n最大誤差: {max_error:.2f}\n")
            f.write(f"{max_error_row.to_string()}\n")
        if min_error_row is not None:
            f.write(f"\n最小誤差: {min_error:.2f}\n")
            f.write(f"{min_error_row.to_string()}\n")
    
    # 誤差のヒストグラムを作成して保存
    #plt.figure(figsize=(10, 6))
    #plt.hist(all_errors, bins=20, color='blue', alpha=0.7)
    #plt.title('Error Distribution')
    #plt.xlabel('Error (predicted_thinking_time - thinking_time)')
    #plt.ylabel('Frequency')
    #plt.grid(True)
    #plt.savefig(plot_file)
    #print(f"結果を '{result_file}' に保存しました。")
    #print(f"ヒストグラムを '{plot_file}' に保存しました。")

# 使用するディレクトリパスを指定 1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845
test_dir_path = "./predicted_results/LPrate_L3"
result_file_path = "./histogram8/LPrate_L3.txt"
plot_file_path = "./histogram8/LPrate_L3.png"
calculate_and_visualize_error(test_dir_path, result_file_path, plot_file_path)
