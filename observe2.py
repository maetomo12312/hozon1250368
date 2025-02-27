import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import plot_tree, export_text
import matplotlib.pyplot as plt

def load_csv_files_from_directory(directory_path):
    """
    指定されたディレクトリからすべてのCSVファイルを読み込み、結合します。
    """
    all_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path)
            all_data.append(df)
    return pd.concat(all_data, ignore_index=True) if all_data else None

def main():
    test_dir_path = "./predicted_results/tamesu"
    data = load_csv_files_from_directory(test_dir_path)
    
    if data is None:
        print("CSVファイルが見つかりません。")
        return
    
    # 特徴量とターゲット変数
    feature_columns = ['match', 'turn', 'cp', 'previous_value', 'previous_evaluation_value', 
                       'previous_poor_hand', 'legal_move', 'long_thoughts', 
                       'first_piece_in_hand', 'second_piece_in_hand', 'rule']
    target_column = 'thinking_time'
    
    if target_column not in data.columns or not all(col in data.columns for col in feature_columns):
        print("指定したカラムがデータに含まれていません。")
        return
    
    x = data[feature_columns]
    y = data[target_column]

    # ランダムフォレストモデルの作成
    model = RandomForestRegressor(random_state=42, n_estimators=3)
    model.fit(x, y)

    # 決定木の可視化と保存
    output_dir = "./tree_visualizations/rate1-735"
    os.makedirs(output_dir, exist_ok=True)
    for i, tree in enumerate(model.estimators_):
        plt.figure(figsize=(60, 40))  # サイズを大きく設定
        plot_tree(tree, feature_names=feature_columns, filled=True, rounded=True, fontsize=10)
        plt.title(f"Tree {i+1}")
        plt.tight_layout()
        filename = os.path.join(output_dir, f"tree_{i+1}.png")
        plt.savefig(filename, dpi=300)  # 高解像度で保存
        plt.close()
        print(f"Tree {i+1} visualization saved as {filename}")

        # 決定木のテキスト表示
        tree_text = export_text(tree, feature_names=feature_columns)
        print(f"Tree {i+1} structure:\n{tree_text}")

if __name__ == "__main__":
    main()
