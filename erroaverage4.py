import os
import pandas as pd

def extract_big_errors(directory_path, result_file, output_csv):
    """
    誤差の絶対値が最も大きい上位5%のデータを集約し、bigerror.csv に保存する。
    """
    all_errors = []  # (誤差, ファイル名, 行番号) のリスト
    extracted_rows = []  # 大きな誤差を持つ行を保存

    with open(result_file, 'r') as f:
        lines = f.readlines()

    # 誤差の上位5%の行を抽出
    extracting = False
    for line in lines:
        if "=== 誤差の上位5% (外れ値) ===" in line:
            extracting = True
            continue
        if extracting and line.strip():
            parts = line.split(", ")
            if len(parts) == 3:
                filename = parts[0].split(": ")[1]
                row_index = int(parts[1].split(": ")[1]) - 1  # CSVの行番号を0-indexに修正
                all_errors.append((filename, row_index))

    # 各ファイルから該当する行を抽出
    for filename, row_index in all_errors:
        file_path = os.path.join(directory_path, filename)
        try:
            df = pd.read_csv(file_path)
            if row_index < len(df):
                extracted_rows.append(df.iloc[row_index])
        except Exception as e:
            print(f"ファイル読み込みエラー: {file_path}, エラー: {e}")

    # 1つの新しいCSVファイルに保存
    if extracted_rows:
        bigerror_df = pd.DataFrame(extracted_rows)
        bigerror_df.to_csv(output_csv, index=False)
        print(f"誤差が大きいデータを '{output_csv}' に保存しました。")
    else:
        print("抽出できるデータがありませんでした。")

# 使用するディレクトリパスと出力ファイルパス
test_dir_path = "./predicted_results/GTMPrate_H"
result_file_path = "./histogram6/GTMPrate_H.txt"
bigerror_csv_path = "./histogram6/GTMbigerror_H.csv"

extract_big_errors(test_dir_path, result_file_path, bigerror_csv_path)
