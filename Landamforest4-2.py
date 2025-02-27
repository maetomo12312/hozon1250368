import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

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

# ディレクトリパスの設定 1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845 short middle long
train_dir_path = "./Searchresult/Gshort_2007-2845"
train_dir_path2 = "./Searchresult/Gshort_1688-2006"
test_dir_path = "./Searchresult/short-test_2007-2845"
test_dir_path2 = "./Searchresult/short-test_1688-2006"
feature_importance_file = "./predicted_results4/GSP_H.txt"
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
x_test = test_data[feature_columns]
y_test = test_data['thinking_time']

# ランダムフォレストモデルの構築とトレーニング n_estimators=100, max_depth=10, 
model = RandomForestRegressor(random_state=42)
#model = RandomForestRegressor(random_state=42,n_estimators=100, max_depth=10,)
model.fit(x_train, y_train)

# スコア計算（過学習確認）
train_score = model.score(x_train, y_train)
test_score = model.score(x_test, y_test)

# 過学習の可能性をチェック
print(f"トレーニングデータのスコア: {train_score:.4f}")
print(f"テストデータのスコア: {test_score:.4f}")

if train_score > 0.95 and test_score < 0.7:
    print("過学習の可能性が高いです！")

# MAE と MSE の計算
y_train_pred = model.predict(x_train)
y_test_pred = model.predict(x_test)

mae_train = mean_absolute_error(y_train, y_train_pred)
mse_train = mean_squared_error(y_train, y_train_pred)

mae_test = mean_absolute_error(y_test, y_test_pred)
mse_test = mean_squared_error(y_test, y_test_pred)

print(f"トレーニングデータの MAE: {mae_train:.4f}, MSE: {mse_train:.4f}")
print(f"テストデータの MAE: {mae_test:.4f}, MSE: {mse_test:.4f}")

if mae_test > mae_train * 1.5:
    print("テストデータの MAE がトレーニングデータよりも大幅に高く、過学習の可能性があります！")

# 特徴量の重要度を出力し、TXTファイルに保存
feature_importances = model.feature_importances_
importance_df = pd.DataFrame({'Feature': feature_columns, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("\n特徴量の重要度:")
print(importance_df)

# 特徴量の重要度を TXT ファイルに保存

importance_df.to_csv(feature_importance_file, sep='\t', index=False)
print(f"特徴量の重要度を {feature_importance_file} に保存しました。")



