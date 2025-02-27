import os
import pandas as pd
import numpy as np

def calculate_90th_percentile(dir1, dir2, dir3, dir4):
    """
    指定されたディレクトリ内のCSVファイルからthinking_timeを収集し、
    昇順ソート後、90%のラインの数値（90パーセンタイル）を求める。
    """
    thinking_times = []

    # 指定されたディレクトリ内のCSVファイルを処理
    for directory in [dir1, dir2, dir3, dir4]:
        if not os.path.exists(directory):
            print(f"ディレクトリが見つかりません: {directory}")
            continue

        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)
                
                try:
                    df = pd.read_csv(file_path)

                    # 'thinking_time' カラムが存在するかチェック
                    if 'thinking_time' in df.columns:
                        # 数値型に変換し、NaNを削除
                        times = pd.to_numeric(df['thinking_time'], errors='coerce').dropna().tolist()
                        thinking_times.extend(times)
                    else:
                        print(f"'thinking_time'列が見つかりません: {file_path}")

                except Exception as e:
                    print(f"CSV読み込みエラー: {file_path}, エラー: {e}")

    # データが存在しない場合の処理
    if not thinking_times:
        print("データが見つかりませんでした。")
        return None

    # thinking_time を昇順ソートし、90パーセンタイルを計算
    thinking_times.sort()
    percentile_80 = np.percentile(thinking_times, 80)

    print(f"80% ラインの thinking_time: {percentile_80}")

    return percentile_80

# ディレクトリの指定（相対パスに修正）
#                     short  middle  long
#           1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845
dir_path1 = "./Searchresult/Tshort_736-1077-2"
dir_path2 = "./Searchresult/Tshort_1-735-2"
dir_path3 = "./Searchresult/Tshort_736-1077-2"
dir_path4 = "./Searchresult/Tshort_1-735-2"

# 90%のラインを計算
calculate_90th_percentile(dir_path1, dir_path2, dir_path3, dir_path4)
