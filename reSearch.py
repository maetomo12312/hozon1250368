import subprocess
import sys
import time
import argparse
import os

accuracies1 = []
accuracies2 = []

class Execute(object):
    """外部プログラムを実行。stdinとstdoutで対話する。"""
    
    # 初期化、コマンドライン引数設定
    def __init__(self, *args_1, **args_2):
        if 'encoding' in args_2:
            self.encoding = args_2.pop('encoding')
        else:
            self.encoding = 'utf-8'
        self.popen = subprocess.Popen(*args_1, stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      encoding=self.encoding, **args_2)

    def send(self, message, recieve=True, incr=False):
        message = message.rstrip('\n')
        if not incr and '\n' in message:
            raise ValueError("message in \\n!")
        self.popen.stdin.write(message + '\n')
        self.popen.stdin.flush()
        if recieve:
            return self.recieve()
        return None

    def recieve(self):
        self.popen.stdout.flush()
        return self.popen.stdout.readline()

    def recieveUntilBM(self, BM):
        """ BestMove が返ってくるまで受信を続け、最後の探索ログを返す """
        self.popen.stdout.flush()
        while True:
            line = self.popen.stdout.readline()
            if "bestmove" in line:
                BM.append(line[9:13])  # bestmoveの手を抽出
                break
        return BM

    def recieveUntilReadyOK(self):
        """ readyOK が返ってくるまで受信を続ける """
        self.popen.stdout.flush()
        while True:
            line = self.popen.stdout.readline()
            if "readyok" in line:
                break

    def terminate(self):
        try:
            self.popen.terminate()
        except ProcessLookupError:
            pass

def main(fileName, output_file):
    BM = []
    accuracy1 = 0  # 一致率 先手
    accuracy2 = 0  # 一致率 後手
    count1 = 0  # 一致数 先手
    count2 = 0  # 一致数 後手
    moves1 = 0  # 先手手数
    moves2 = 0  # 後手手数
    engineName = args.engineName
    maxnodes = args.maxnodes
    index = 0

    # engine 設定
    engine = Execute([engineName])
    engine.send("setoption name Threads value 1", recieve=False, incr=True)
    engine.send("isready", recieve=False, incr=True)
    engine.recieveUntilReadyOK()

    # 読み込んだUSIファイルを一手ずつ解析
    with open(fileName) as f:
        for line in f:
            if "position" in line:
                if index == 0:
                    engine.send("usinewgame", recieve=False, incr=True)
                    engine.send(line, recieve=False, incr=True)
                    gostr = "go nodes " + str(maxnodes)
                    engine.send(gostr, recieve=False, incr=True)
                    engine.recieveUntilBM(BM)

                engine.send("usinewgame", recieve=False, incr=True)
                engine.send(line, recieve=False, incr=True)
                gostr = "go nodes " + str(maxnodes)
                engine.send(gostr, recieve=False, incr=True)
                engine.recieveUntilBM(BM)

                # 一致率の計算
                Rmove = line[-6:-1]
                index += 1
                bestmove = str(BM[index - 1])

                if index % 2 != 0:  # 先手の手番
                    if bestmove.replace(' ', '') == Rmove.replace(' ', ''):
                        count1 += 1
                        print(f"先手の手が一致しました: {bestmove} == {Rmove}")
                    else:
                        print(f"先手の手が一致しませんでした: {bestmove} != {Rmove}")
                    moves1 += 1
                else:  # 後手の手番
                    if bestmove.replace(' ', '') == Rmove.replace(' ', ''):
                        count2 += 1
                        print(f"後手の手が一致しました: {bestmove} == {Rmove}")
                    else:
                        print(f"後手の手が一致しませんでした: {bestmove} != {Rmove}")
                    moves2 += 1

        engine.send("quit")

    if moves1 > 0:
        accuracy1 = (count1 / moves1) * 100
    if moves2 > 0:
        accuracy2 = (count2 / moves2) * 100

    accuracies1.append(accuracy1)
    accuracies2.append(accuracy2)

    # 結果を1つのファイルに保存
    with open(output_file, "a", encoding="UTF-8") as f:
        f.write(f"{fileName} の結果:\n")
        f.write(f"後手の一致率: {accuracy2:.2f}% ({moves2}手中{count2}手)\n")
        f.write(f"先手の一致率: {accuracy1:.2f}% ({moves1}手中{count1}手)\n\n")

    if isinstance(engine, Execute):
        engine.terminate()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("engineName")
    parser.add_argument("usi_folder")
    parser.add_argument("outputDir")
    parser.add_argument("outputFile")
    parser.add_argument("maxnodes", type=int)
    args = parser.parse_args()
    
    os.makedirs(args.outputDir, exist_ok=True)
    
    # すべての結果を1つのファイルにまとめて出力
    output_file = os.path.join(args.outputDir, args.outputFile)

    for filename in os.listdir(args.usi_folder):
        if filename.endswith(".usi"):
            file_path = os.path.join(args.usi_folder, filename)
            main(file_path, output_file)

    # 最終結果を出力
    with open(output_file, "a", encoding="UTF-8") as f:
        if accuracies1:
            avg_accuracy1 = sum(accuracies1) / len(accuracies1)  # 先手一致率の平均
            f.write(f"全体の先手一致率の平均: {avg_accuracy1:.2f}%\n")
        else:
            f.write("全体の先手一致率のデータがありません\n")
        
        if accuracies2:
            avg_accuracy2 = sum(accuracies2) / len(accuracies2)  # 後手一致率の平均
            f.write(f"全体の後手一致率の平均: {avg_accuracy2:.2f}%\n")
        else:
            f.write("全体の後手一致率のデータがありません\n")


