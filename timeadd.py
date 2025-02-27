import os
import csv

# パスを設定
rrrate_dir = './Searchresult/RRRrate_1-735'
trate_dir = './usistorage/TTrate_1-735'

# ファイルペアを処理する
for filename in os.listdir(rrrate_dir):
    if filename.startswith('SearchR_') and filename.endswith('.csv'):
        usi_filename = filename.replace('SearchR_', '').replace('.csv', '.usi')
        usi_path = os.path.join(trate_dir, usi_filename)
        csv_path = os.path.join(rrrate_dir, filename)

        # 29.usiのthinking_time列を取得
        if os.path.exists(usi_path):
            with open(usi_path, 'r', encoding='utf-8') as usi_file:
                usi_lines = usi_file.readlines()
                for line in usi_lines:
                    if line.startswith('thinking_time'):
                        thinking_times = list(map(int, line.strip().split()[1:]))
                        print(thinking_times)
                        break
                else:
                    print(f"thinking_time not found in {usi_filename}")
                    continue
        else:
            print(f"USI file not found: {usi_filename}")
            continue

        # SearchR_xx.csvにbefore_thinking_time列を追加
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            reader = list(csv.reader(csv_file))
            header = reader[0]
            rows = reader[1:]

        # before_thinking_time列の追加
        if 'before_thinking_time' not in header:
            header.append('before_thinking_time')

        # 40手目以降のthinking_timeと比較し、before_thinking_timeを追加
        updated_rows = []
        for i, row in enumerate(rows):
            if i >= 40:  # 40手目以降
                thinking_time = int(row[8])  # thinking_time列の値
                if thinking_time in thinking_times[i:]:
                    print('a')
                    time_index = thinking_times.index(thinking_time, i)
                    before_time = thinking_times[time_index - 1] if time_index > 0 else 0
                    row.append(str(before_time))
                else:
                    row.append('0')
            else:
                row.append('0')  # 40手目未満は0を挿入
            updated_rows.append(row)

        # CSVファイルに書き込み
        with open(csv_path, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(updated_rows)

        print(f"Updated {filename} with before_thinking_time.")
