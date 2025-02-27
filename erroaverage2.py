import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_and_visualize_error(train_dir_path, train_dir_path2, test_dir_path, test_dir_path2, result_file, plot_file):
    """
    Train データ (train_dir_path, train_dir_path2) の thinking_time 平均を計算し、
    Test データ (test_dir_path, test_dir_path2) の thinking_time との誤差を求め、
    絶対誤差の平均を出力し、ヒストグラムを作成する。
    """
    # Train データの thinking_time の平均を求める
    total_train_time = 0
    train_count = 0
    
    for train_path in [train_dir_path, train_dir_path2]:
        for filename in os.listdir(train_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(train_path, filename)
                df = pd.read_csv(file_path)
                if 'thinking_time' in df.columns:
                    total_train_time += df['thinking_time'].sum()
                    train_count += df['thinking_time'].count()
    
    average_train = total_train_time / train_count if train_count > 0 else 0
    print(f"Train データの thinking_time 平均: {average_train}")
    
    # Test データの誤差計算
    all_train_diffs = []  # thinking_time と average_train の誤差リスト
    max_error_row = None  # 最大誤差の行
    min_error_row = None  # 最小誤差の行
    max_error = float('-inf')
    min_error = float('inf')
    
    with open(result_file, 'w') as f:
        f.write(f"Train データの thinking_time の平均: {average_train}\n")
        
        for test_path in [test_dir_path, test_dir_path2]:
            for filename in os.listdir(test_path):
                if filename.endswith(".csv"):
                    file_path = os.path.join(test_path, filename)
                    df = pd.read_csv(file_path)
                    
                    if 'thinking_time' in df.columns:
                        df['train_diff'] = df['thinking_time'] - average_train
                        all_train_diffs.extend(df['train_diff'].tolist())
                        
                        # 最大誤差の更新
                        if df['train_diff'].max() > max_error:
                            max_error = df['train_diff'].max()
                            max_error_row = df.loc[df['train_diff'].idxmax()]

                        # 最小誤差の更新
                        if df['train_diff'].min() < min_error:
                            min_error = df['train_diff'].min()
                            min_error_row = df.loc[df['train_diff'].idxmin()]

        # 絶対誤差の平均計算
        mean_train_diff = sum(abs(err) for err in all_train_diffs) / len(all_train_diffs) if all_train_diffs else 0
        
        f.write(f"thinking_time と average_train の絶対誤差の平均: {mean_train_diff}\n")
        
        if max_error_row is not None:
            f.write(f"\n最大誤差: {max_error:.2f}\n")
            f.write(f"{max_error_row.to_string()}\n")
        if min_error_row is not None:
            f.write(f"\n最小誤差: {min_error:.2f}\n")
            f.write(f"{min_error_row.to_string()}\n")
    
    # ヒストグラム作成
    plt.figure(figsize=(10, 6))
    plt.hist(all_train_diffs, bins=20, color='blue', alpha=0.5, label='Train Avg Difference')
    plt.title('Error Distribution')
    plt.xlabel('Error Value')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_file)
    print(f"結果を '{result_file}' に保存しました。")
    print(f"ヒストグラムを '{plot_file}' に保存しました。")

# ディレクトリパス指定  1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845 short middle long
train_dir_path = "./Searchresult/long_1688-2006"
train_dir_path2 = "./Searchresult/long_2007-2845"
test_dir_path = "./predicted_results/LPrate_1688-2006"
test_dir_path2 = "./predicted_results/LPrate_2007-2845"
result_file_path = "./histogram2/LPrate_H.txt"
plot_file_path = "./histogram2/LPrate-H.png"

calculate_and_visualize_error(train_dir_path, train_dir_path2, test_dir_path, test_dir_path2, result_file_path, plot_file_path)
