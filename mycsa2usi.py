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

            usistr = "position startpos moves "  # USI形式の指し手文字列の先頭部分

            # 出力するUSIファイルのパスを設定
            output_file_name = csafile.replace(".csa", ".usi")
            output_file_path = os.path.join(output_folder, output_file_name)

            # USI形式で指手を保存するためのファイルを開く
            with open(output_file_path, "w") as usi_file:
                for i, m in enumerate(moves):
                    usistr += cshogi.move_to_usi(m) + " "
                    # 一手ごとに、USI形式で棋譜をファイルに出力
                    usi_file.write(usistr + "\n")
                
                # 棋譜全体をファイルに出力
                #usi_file.write(usistr + "\n")
                print(f"Converted {csafile} to {output_file_name}")

if __name__ == '__main__':
    main()
