import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_and_visualize_error(directory_path, result_file):
    """
    指定されたディレクトリ内のすべてのCSVファイルについて、誤差の平均を計算し、誤差の分布をヒストグラムで可視化し、
    TP, FP, FN, TN から正解率・適合率・再現率・F値を計算し、結果をファイルに保存します。
    """

    # TP, FP, FN, TN のカウント
    TP = FP = FN = TN = 0
    revalue = 57
    with open(result_file, 'w') as f:
        for filename in os.listdir(directory_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory_path, filename)
                df = pd.read_csv(file_path)
                
                if 'predicted_thinking_time' in df.columns and 'thinking_time' in df.columns:
                    
                    # TP, FP, FN, TN の計算 int型として判定
                    df['pred_label'] = (df['predicted_thinking_time'] >= revalue).astype(int)
                    df['true_label'] = (df['thinking_time'] >= revalue).astype(int)

                    TP += ((df['pred_label'] == 1) & (df['true_label'] == 1)).sum()
                    FP += ((df['pred_label'] == 1) & (df['true_label'] == 0)).sum()
                    FN += ((df['pred_label'] == 0) & (df['true_label'] == 1)).sum()
                    TN += ((df['pred_label'] == 0) & (df['true_label'] == 0)).sum()


        # 正解率・適合率・再現率・F1スコアの計算
        accuracy = (TP + TN) / (TP + FP + FN + TN) if (TP + FP + FN + TN) > 0 else 0
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        f_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        # 結果をファイルに書き込む
        f.write("\n--- 評価指標 ---\n")
        f.write(f"正解率 (Accuracy): {accuracy:.4f}\n")
        f.write(f"適合率 (Precision): {precision:.4f}\n")
        f.write(f"再現率 (Recall): {recall:.4f}\n")
        f.write(f"F1スコア (F1-score): {f_score:.4f}\n")


    print(f"結果を '{result_file}' に保存しました。")

# 使用するディレクトリパスを指定 1-735  736-1077 1078-1374 1375-1687 1688-2006 2007-2845
test_dir_path = "./predicted_results/LPrate_L-H"
result_file_path = "./TPFP/LPrate_L-H.txt"

calculate_and_visualize_error(test_dir_path, result_file_path)
