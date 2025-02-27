import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
def load_csv_files_from_directory(directory_path):
    """
    指定されたディレクトリからすべてのCSVファイルを読み込み、1つのDataFrameに結合します。
    """
    all_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path)
            all_data.append(df)
    return pd.concat(all_data, ignore_index=True) if all_data else None

# ディレクトリパスの設定
train_dir_path = "./Searchresult/long_2007-2845"
train_dir_path2 = "./Searchresult/long_1688-2006"
test_dir_path = "./Searchresult/long-test_1375-1687"
test_dir_path2 = "./Searchresult/long-test_1078-1374"
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
x_train = train_data[feature_columns]  # 特徴量
y_train = train_data['thinking_time']  # ターゲット変数
# ランダムフォレストモデルの構築とトレーニング
model = RandomForestRegressor(random_state=42)
model.fit(x_train, y_train)
# テストデータに基づいて予測
x_test = test_data[feature_columns]  # テストデータの特徴量
predictions = model.predict(x_test)
# 結果を出力
test_data['predicted_thinking_time'] = predictions
print("新しいデータの予測結果:")
print(test_data[feature_columns + ['predicted_thinking_time']])
# 予測結果をCSVファイルに保存
output_dir = "./predicted_results/LPrate_H-M"
os.makedirs(output_dir, exist_ok=True)

# 個別の予測結果ファイルを保存
for filename in os.listdir(test_dir_path):
    if filename.endswith(".csv"):
        # 各ファイルごとに予測値を適用
        test_file_path = os.path.join(test_dir_path, filename)
        test_df = pd.read_csv(test_file_path)
        test_df['predicted_thinking_time'] = predictions[:len(test_df)]
        predictions = predictions[len(test_df):]  # 予測値のインデックスを更新

        # 出力ファイル名を生成
        test_output_file = os.path.join(output_dir, f"predicted_{filename}")
        test_df.to_csv(test_output_file, index=False)
        print(f"予測結果をファイルに保存しました: {test_output_file}")
for filename in os.listdir(test_dir_path2):
    if filename.endswith(".csv"):
        # 各ファイルごとに予測値を適用
        test_file_path2 = os.path.join(test_dir_path2, filename)
        test_df2 = pd.read_csv(test_file_path2)
        test_df2['predicted_thinking_time'] = predictions[:len(test_df2)]
        predictions = predictions[len(test_df2):]  # 予測値のインデックスを更新

        test_output_file2 = os.path.join(output_dir, f"predicted_{filename}")
        test_df2.to_csv(test_output_file2, index=False)
        print(f"予測結果をファイルに保存しました: {test_output_file}")
