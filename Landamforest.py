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
train_dir_path = "./Searchresult/short_2007-2845"
test_dir_path = "./Searchresult/short-test_2007-2845"
#                     short  middle  long
#           1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845

# 学習データとテストデータの読み込み
train_data = load_csv_files_from_directory(train_dir_path)
test_data = load_csv_files_from_directory(test_dir_path)

if train_data is None or test_data is None:
    print("学習データまたはテストデータが見つかりません。ディレクトリの内容を確認してください。")
    exit()

# 学習データの概要確認
print("学習データの概要:")
print(train_data.head())

# 新しいデータの概要確認
print("新しいデータの概要:")
print(test_data.head())

# 学習データの特徴量とターゲット変数の設定
feature_columns = ['rule', 'match', 'turn', 'cp', 'previous_value', 'previous_evaluation_value', 
                   'previous_poor_hand', 'legal_move', 'before_thinking_time','long_thoughts', 
                   'first_piece_in_hand', 'second_piece_in_hand']
x_train = train_data[feature_columns]  # 拡張した特徴量
y_train = train_data['thinking_time']  # ターゲット変数

# ランダムフォレストモデルの構築とトレーニング
model = RandomForestRegressor(random_state=42)
model.fit(x_train, y_train)

# 新しいデータに基づいて予測
x_new = test_data[feature_columns]  # 新しいデータの特徴量
predictions = model.predict(x_new)

# 結果を出力
test_data['predicted_thinking_time'] = predictions
print("新しいデータの予測結果:")
print(test_data[feature_columns + ['predicted_thinking_time']])

# 予測結果をCSVファイルに保存 1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845
output_dir = "./predicted_results/SPrate_2007-2845"
os.makedirs(output_dir, exist_ok=True)

# 個別の予測結果ファイルを保存
for i, filename in enumerate(os.listdir(test_dir_path)):
    if filename.endswith(".csv"):
        test_file_path = os.path.join(test_dir_path, filename)
        test_output_file = os.path.join(output_dir, f"predicted_{filename}")
        test_df = pd.read_csv(test_file_path)
        test_df['predicted_thinking_time'] = predictions[:len(test_df)]
        predictions = predictions[len(test_df):]  # 予測値を更新
        test_df.to_csv(test_output_file, index=False)
        print(f"予測結果をファイルに保存しました: {test_output_file}")
