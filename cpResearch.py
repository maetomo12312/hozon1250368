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

    def recieveUntilBM(self, BM, scores):
        """ BestMove が返ってくるまで受信を続け、最後の探索ログを返す """
        self.popen.stdout.flush()
        last_score = None
        while True:
            line = self.popen.stdout.readline()
            if "bestmove" in line:
                BM.append(line.split(" ")[1])  # bestmoveの手を抽出
                scores.append(score_cp if score_cp is not None else 0)  # スコアを保存
                break
            elif "score cp" in line:
                try:
                    # スコア情報を抽出
                    score_cp = int(line.split("score cp")[1].split()[0])
                except (IndexError, ValueError):
                    score_cp = 0  # 抽出失敗時のデフォルト値

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
    scores = []  # スコアリストを追加
    scores1 = []  # 先手スコアのリスト
    scores2 = []  # 後手スコアのリスト
    accuracy1 = 0  # 一致率 先手
    accuracy2 = 0  # 一致率 後手
    count1 = 0  # 一致数 先手
    count2 = 0  # 一致数 後手
    moves1 = 0  # 先手手数
    moves2 = 0  # 後手手数
    engineName = args.engineName
    maxnodes = args.maxnodes
    index = 0
    start_move = 40  # 40手目から計測

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
                    engine.recieveUntilBM(BM, scores)

                engine.send("usinewgame", recieve=False, incr=True)
                engine.send(line, recieve=False, incr=True)
                gostr = "go nodes " + str(maxnodes)
                engine.send(gostr, recieve=False, incr=True)
                engine.recieveUntilBM(BM, scores)

                # 一致率の計算
                Rmove = line[-6:-1]
                index += 1
                bestmove = str(BM[index - 1])
                current_score = scores[index - 1]
                if index <= start_move:
                    # 40手目以前はスキップ
                    continue
                if index % 2 != 0:  # 先手の手番
                    if bestmove.replace(' ', '') == Rmove.replace(' ', ''):
                        count1 += 1
                        f.write(f"fmove-match: {bestmove} == {Rmove} cp {current_score}")
                    else:
                        f.write(f"fmove-dismatch: {bestmove} != {Rmove} cp {current_score}")
                    moves1 += 1
                else:  # 後手の手番
                    if bestmove.replace(' ', '') == Rmove.replace(' ', ''):
                        count2 += 1
                        f.write(f"smove-match: {bestmove} == {Rmove} cp {current_score}")
                    else:
                        f.write(f"smove-dismatch: {bestmove} != {Rmove} cp {current_score}")
                    moves2 += 1

        engine.send("quit")

    if moves1 > 0:
        accuracy1 = (count1 / moves1) * 100
    if moves2 > 0:
        accuracy2 = (count2 / moves2) * 100
    avg_score1 = sum(scores1) / len(scores1) if scores1 else 0  # 先手評価値の平均
    avg_score2 = sum(scores2) / len(scores2) if scores2 else 0  # 後手評価値の平均
    accuracies1.append(accuracy1)
    accuracies2.append(accuracy2)

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