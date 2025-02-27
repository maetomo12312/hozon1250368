import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def load_csv_files_from_directory(directory_path):
    """
    指定されたディレクトリからすべてのCSVファイルを読み込み、結合し、データのクリーニングを行う。
    """
    all_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path)
            all_data.append(df)

    if all_data:
        df = pd.concat(all_data, ignore_index=True)

        # NaN, inf を処理
        df.replace([np.inf, -np.inf], np.nan, inplace=True)  # inf を NaN に変換
        df.dropna(inplace=True)  # NaN を削除
        df = df.astype(np.float32)  # データを float32 に変換

        return df
    return None

# ディレクトリパスの設定
train_dir_path = "./Searchresult/long_2007-2845"
train_dir_path2 = "./Searchresult/long_1688-2006"
test_dir_path = "./Searchresult/long-test_2007-2845"
test_dir_path2 = "./Searchresult/long-test_1688-2006"
#                     short  middle  long
#           1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845
# 学習データとテストデータの読み込み
train_data1 = load_csv_files_from_directory(train_dir_path)
train_data2 = load_csv_files_from_directory(train_dir_path2)
test_data1 = load_csv_files_from_directory(test_dir_path)
test_data2 = load_csv_files_from_directory(test_dir_path2)

# データが正しく読み込まれたか確認
if train_data1 is None or train_data2 is None or test_data1 is None or test_data2 is None:
    print("学習データまたはテストデータが見つかりません。ディレクトリの内容を確認してください。")
    exit()

# 学習データを結合
train_data = pd.concat([train_data1, train_data2], ignore_index=True)
test_data = pd.concat([test_data1, test_data2], ignore_index=True)

# 学習データの特徴量とターゲット変数の設定
feature_columns = [
    'rule', 'match', 'turn', 'cp', 'previous_value', 
    'previous_evaluation_value', 'previous_poor_hand', 
    'legal_move', 'before_thinking_time', 'long_thoughts', 
    'first_piece_in_hand', 'second_piece_in_hand'
]

# NaN の処理（再確認）
train_data = train_data.dropna()
test_data = test_data.dropna()

# 特徴量とターゲット変数の抽出
x_train = train_data[feature_columns]
y_train = train_data['thinking_time']

# ランダムフォレストモデルの構築とトレーニング
model = RandomForestRegressor(random_state=42)
model.fit(x_train, y_train)

# テストデータに基づいて予測
x_test = test_data[feature_columns]
predictions = model.predict(x_test)

# 結果を出力
test_data['predicted_thinking_time'] = predictions
print("新しいデータの予測結果:")
print(test_data[feature_columns + ['predicted_thinking_time']])

# 予測結果をCSVファイルに保存
output_dir = "./predicted_results/LPrate_H2"
os.makedirs(output_dir, exist_ok=True)

# 個別の予測結果ファイルを保存
for test_dir, test_df in [(test_dir_path, test_data1), (test_dir_path2, test_data2)]:
    for filename in os.listdir(test_dir):
        if filename.endswith(".csv"):
            test_file_path = os.path.join(test_dir, filename)
            test_df_individual = pd.read_csv(test_file_path)

            # NaN の処理（個別ファイル）
            test_df_individual.replace([np.inf, -np.inf], np.nan, inplace=True)
            test_df_individual.dropna(inplace=True)

            test_df_individual['predicted_thinking_time'] = predictions[:len(test_df_individual)]
            predictions = predictions[len(test_df_individual):]  # 予測値のインデックスを更新

            # 出力ファイル名を生成
            test_output_file = os.path.join(output_dir, f"predicted_{filename}")
            test_df_individual.to_csv(test_output_file, index=False)
            print(f"予測結果をファイルに保存しました: {test_output_file}")
