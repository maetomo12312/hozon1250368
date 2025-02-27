import os
import pandas as pd

# 処理対象のディレクトリリスト 1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845 
# short middle long
csv_dirs = [
    "./Searchresult/Tlong_2007-2845-2",
    "./Searchresult/Tlong_1688-2006-2",
    "./Searchresult/Tlong-test_2007-2845-2",
    "./Searchresult/Tlong-test_1688-2006-2"
]

# 各ディレクトリ内のCSVファイルを処理
for csv_dir in csv_dirs:
    if not os.path.exists(csv_dir):  # ディレクトリが存在するかチェック
        print(f"ディレクトリが見つかりません: {csv_dir}")
        continue

    for csv_filename in os.listdir(csv_dir):
        if csv_filename.endswith(".csv"):
            csv_path = os.path.join(csv_dir, csv_filename)

            try:
                # CSVファイルの読み込み
                df = pd.read_csv(csv_path)

                # "thinking_time" 列が存在するか確認
                if "thinking_time" in df.columns:
                    # 新しい列 "player_long_thought" を作成
                    df["player_long_thought"] = df["thinking_time"].apply(lambda x: 1 if x >= 51 else 0)

                    # 上書き保存
                    df.to_csv(csv_path, index=False)
                    #print(f"{csv_path} に 'player_long_thought' を追加しました。")
                else:
                    print(f"{csv_path} に 'thinking_time' 列が見つかりません。")

            except Exception as e:
                print(f"{csv_path} の処理中にエラーが発生しました: {e}")
