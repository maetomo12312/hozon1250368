import sys
import cshogi
import os
from cshogi import CSA

def main():
    if len(sys.argv) != 3:
        print("Usage: csa2usi.py input_folder output_folder")
        return

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    # 出力フォルダが存在しない場合は作成
    os.makedirs(output_folder, exist_ok=True)

    # input_folder内のすべてのファイルを処理
    for csafile in os.listdir(input_folder):
        if csafile.endswith(".csa"):
            input_file_path = os.path.join(input_folder, csafile)
            parser = cshogi.CSA.Parser()  # CSAをパースするオブジェクト
            parser.parse_csa_file(input_file_path)  # 指定のCSAファイルをパースする
            moves = parser.moves  # 指手のリスト
            times = parser.times  # 思考時間のリスト

            # 出力するUSIファイルのパスを設定
            output_file_name = csafile.replace(".csa", ".usi")
            output_file_path = os.path.join(output_folder, output_file_name)

            # USI形式で指手を保存するためのファイルを開く
            with open(output_file_path, "w") as usi_file:
                usistr = "position startpos moves "  # 最初の行のベース部分
                time_str = "thinking_time "  # 思考時間用のベース部分

                for i, m in enumerate(moves):
                    # 現在の指し手と時間をUSI形式で追加
                    usistr += cshogi.move_to_usi(m) + " "
                    time_str += f"{times[i]} "

                    # 書き込み: 現在の指し手と時間
                    usi_file.write(usistr.strip() + "\n")
                    usi_file.write(time_str.strip() + "\n")

            print(f"Converted {csafile} to {output_file_name}")

if __name__ == '__main__':
    main()
