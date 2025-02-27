import os
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# 予測結果が格納されているディレクトリ
predicted_results_dir = "./predicted_results2/TLPrate_H"
results_dir = "./predicted_results2"
# 評価指標の初期化
all_y_true = []
all_y_pred = []

# ディレクトリ内のすべてのCSVファイルを処理
for filename in os.listdir(predicted_results_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(predicted_results_dir, filename)

        try:
            # CSVファイルの読み込み
            df = pd.read_csv(file_path)

            # 必要なカラムが存在するか確認
            if "player_long_thought" in df.columns and "predicted_player_long_thought" in df.columns:
                y_true = df["player_long_thought"].astype(int)  # 正解ラベル
                y_pred = df["predicted_player_long_thought"].astype(int)  # 予測ラベル

                # リストに追加
                all_y_true.extend(y_true)
                all_y_pred.extend(y_pred)

                #print(f"{filename} のデータを処理しました。")
            else:
                print(f"{filename} に必要なカラムがありません。")

        except Exception as e:
            print(f"{filename} の処理中にエラーが発生しました: {e}")

# 全データの評価指標を計算
if all_y_true and all_y_pred:
    accuracy = accuracy_score(all_y_true, all_y_pred)
    precision = precision_score(all_y_true, all_y_pred, zero_division=0)
    recall = recall_score(all_y_true, all_y_pred, zero_division=0)
    f1 = f1_score(all_y_true, all_y_pred, zero_division=0)

    # 結果を表示
    print("\n全体の評価指標:")
    print(f"正解率 (Accuracy): {accuracy:.4f}")
    print(f"適合率 (Precision): {precision:.4f}")
    print(f"再現率 (Recall): {recall:.4f}")
    print(f"F1スコア: {f1:.4f}")

    # クラス分類レポート
    report = classification_report(all_y_true, all_y_pred, zero_division=0)
    print("\n分類レポート:")
    print(report)

    # 結果をTXTファイルに保存
    report_file = os.path.join(results_dir, "TLPrate_H.txt")
    with open(report_file, "w") as f:
        f.write(f"正解率 (Accuracy): {accuracy:.4f}\n")
        f.write(f"適合率 (Precision): {precision:.4f}\n")
        f.write(f"再現率 (Recall): {recall:.4f}\n")
        f.write(f"F1スコア: {f1:.4f}\n\n")
        f.write("分類レポート:\n")
        f.write(report)
    
    print(f"分類レポートを {report_file} に保存しました。")

else:
    print("評価に使用できるデータがありません。")
