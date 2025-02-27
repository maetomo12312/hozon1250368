import subprocess
import sys
import time
import argparse
import os
import csv
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

    def recieveUntilBM(self, BM, scores, piece_in_hand1, piece_in_hand2, legal_moves_list):
        """ BestMove が返ってくるまで受信を続け、合法手情報をデバッグ確認 """
        self.popen.stdout.flush()
        legal_moves = []  # 合法手リスト
        score_cp = None
        pv = []  # 最良手のリスト
        while True:
            line = self.popen.stdout.readline()
            
            # デバッグ用：受信行の出力
            #print(f"デバッグ: 受信行: {line.strip()}")
            
            if "bestmove" in line:
                BM.append(line.split(" ")[1])  # bestmoveの手を抽出
                scores.append(score_cp if score_cp is not None else 0)  # スコアを保存
                break
            if "score cp" in line:
                try:
                    # スコア情報を抽出
                    score_cp = int(line.split("score cp")[1].split()[0])
                    # デバッグ用: 抽出されたスコアの出力
                    #print(f"デバッグ: 抽出されたスコア: {score_cp}")
                except (IndexError, ValueError):
                    #print(f"デバッグ: スコア抽出に失敗: {line.strip()}")  # スコア抽出失敗の警告
                    score_cp = 0  # 抽出失敗時のデフォルト値
            if "pih1" in line:
                try:
                # 持ち駒の総数を抽出
                    pih_count = int(line.split("pih1")[1].split()[0])
                # デバッグ用: 抽出された持ち駒の総数を出力
                    #print(f"デバッグ: 抽出された持ち駒の総数: {pih_count}")
                except (IndexError, ValueError):
                    pih_count = 0  # 抽出失敗時のデフォルト値
                piece_in_hand1.append(pih_count)
            if "pih2" in line:
                try:
                # 持ち駒の総数を抽出
                    pih_count = int(line.split("pih2")[1].split()[0])
                # デバッグ用: 抽出された持ち駒の総数を出力
                    #print(f"デバッグ: 抽出された持ち駒の総数: {pih_count}")
                except (IndexError, ValueError):
                    pih_count = 0  # 抽出失敗時のデフォルト値
                piece_in_hand2.append(pih_count)
            if "info" in line and "pv" in line:
                try:
                    # lmから合法手を抽出
                    lm_index = line.index("lm") + 3
                    lm = line[lm_index:].strip().split()
                    #print(lm)
                    # デバッグ用: 抽出されたPVと合法手
                    #print(f"デバッグ: 抽出されたPV: {extractpv}")
                    
                    legal_moves = [move for move in lm]
                    
                    # 重複を削除（順序を保持する方法）
                    legal_moves = list(dict.fromkeys(legal_moves))
                    
                    legal_moves_list.append(legal_moves)  # 合法手リストを保存

                except (IndexError, ValueError):
                    #print(f"デバッグ: PV抽出に失敗: {line.strip()}")
                    pv = []
        #print(f"デバッグ: 合法手の数 (lmcount): {len(legal_moves)}")
        # デバッグ用: 最終的な合法手一覧を出力
        #print(f"デバッグ: 最善手一覧 : {extractpv}")
        # PVのみを表示
        #print(f"デバッグ: 合法手一覧: {legal_moves}")
        
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

def rulejudge(thinking_times):
    quick_judge_total1 = 60
    quick_judge_total2 = 60
    quick_judge_total3 = 900
    quick_judge_total4 = 900
    Quick_Juudge = 0 
    
    for i, time in enumerate(thinking_times):
        if i % 2 == 0:  # 先手の手
            quick_judge_total1 -= time
            if quick_judge_total1 < 0 and time >= 31:
                Quick_Juudge = 1
            quick_judge_total3 -= time
            if Quick_Juudge == 1 and quick_judge_total3 < 0 and time >= 61:
                return 2  # すぐに3を返す
        else:  # 後手の手
            quick_judge_total2 -= time
            if quick_judge_total2 < 0 and time >= 31:
                Quick_Juudge = 1
            quick_judge_total4 -= time
            if Quick_Juudge == 1 and quick_judge_total4 < 0 and time >= 61:
                return 2  # すぐに3を返す
    
    return Quick_Juudge
def main(fileName, csv_output_file):

    engineName = args.engineName
    maxnodes = args.maxnodes

    # 現在の棋譜ファイルに基づいたCSVファイル名を生成
    base_name = os.path.splitext(os.path.basename(fileName))[0]
    csv_output_file = f"{csv_output_file}_{base_name}.csv"
    # CSVヘッダー
    csv_headers = ["rule", "match", "turn", "cp", "previous_value", "previous_evaluation_value", "previous_poor_hand", "legal_move", "before_thinking_time", "thinking_time", "long_thoughts", "first_piece_in_hand", "second_piece_in_hand"]

    # CSVファイルを初期化
    with open(csv_output_file, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_headers)

    # engine 設定
    engine = Execute([engineName])
    engine.send("setoption name Threads value 1", recieve=False, incr=True)
    engine.send("isready", recieve=False, incr=True)
    engine.recieveUntilReadyOK()
    
    for pass_count in range(2):  # 2周する
        BM = []
        scores = []  # スコアリストを追加
        legal_moves_list = []  # 合法手リスト
        scores1 = []  # 先手スコアのリスト
        scores2 = []  # 後手スコアのリスト
        count1 = 0  # 一致数 先手
        count2 = 0  # 一致数 後手
        moves1 = 0  # 先手手数
        moves2 = 0  # 後手手数
        thinking_times = []  # 各手のthinking_timeを格納するリスト
        index = 0
        piece_in_hand1 = []
        piece_in_hand2 = []
        start_move = 40  # 40手目から計測
        long_rule_time_F = 1800
        middle_rule_time_F = 900
        short_rule_time_F = 60
        long_rule_time_S = 1800
        middle_rule_time_S = 900
        short_rule_time_S = 60
        long_rule_havetime = 59
        middle_rule_havetime = 48
        short_rule_havetime = 15
        long_rule_notime = 57
        middle_rule_notime = 55
        short_rule_notime = 25
        zero = 0
        one = 1
        two = 2
    # 読み込んだUSIファイルを一手ずつ解析
        with open(fileName) as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "position" in line:
                    # `thinking_time`行を読み取る
                    if i + 1 < len(lines) and "thinking_time" in lines[i + 1]:
                        thinking_time_str = lines[i + 1].split("thinking_time")[1].strip()
                        thinking_time_values = thinking_time_str.split()
                        thinking_times = list(map(int, thinking_time_values))
                    else:
                        thinking_times = []  # デフォルトで空リスト
                    if "moves" in line:
                        parts = line.split("moves")
                        moves = parts[1].strip().split()  # "moves"以降を分割
                        if moves:  # movesが空でない場合
                            trimmed_moves = " ".join(moves[:-1])  # 最後の要素を除去
                            trimmed_line = f"{parts[0]}moves {trimmed_moves}".strip()
                        else:
                            trimmed_line = parts[0].strip()  # movesが空の場合は"position"部分のみ
                    else:
                        trimmed_line = line.strip()  # "moves"が含まれない場合はそのまま
                    if pass_count == 1:
                        #print(trimmed_line)  # 修正後のlineを出力
                        engine.send("usinewgame", recieve=False, incr=True)
                        engine.send(trimmed_line, recieve=False, incr=True)
                        gostr = "go nodes " + str(maxnodes)
                        engine.send(gostr, recieve=False, incr=True)
                        engine.recieveUntilBM(BM, scores, piece_in_hand1, piece_in_hand2,legal_moves_list)
                        # 一致率の計算
                        Rmove = line[-6:-1]
                        index += 1
                        turn = index % 2
                        bestmove = str(BM[index - 1])
                        if bestmove.strip() == "resign":
                            if pass_count == 0:
                                rule = rulejudge(thinking_times)
                            break
                        current_score = scores[index - 1]
                        #print(f"ターン: {index}")
                        current_thinking_time = thinking_times[index - 1] if index - 1 < len(thinking_times) else 0
                        if pass_count == 1:
                            if rule == zero and turn == one:
                                short_rule_time_F -= current_thinking_time
                            elif rule == zero and turn == zero:
                                short_rule_time_S -= current_thinking_time
                            elif rule == one and turn == one:
                                middle_rule_time_F -= current_thinking_time
                            elif rule == one and turn == zero:
                                middle_rule_time_S -= current_thinking_time
                            elif rule == two and turn == one:
                                long_rule_time_F -= current_thinking_time
                            elif rule == two and turn == zero:
                                long_rule_time_S -= current_thinking_time
                                
                        # 合法手の数を取得
                        legal_move_count = len(legal_moves_list[index - 1]) if index - 1 < len(legal_moves_list) else 0
                        #print(f"{legal_moves_list}")
                        if current_score == 0 and legal_move_count == 0:#積み
                            break
                        if index == 1:
                            piece_in_hand1.remove(0)#先読みの関係でずれているため
                            piece_in_hand2.remove(0)
                        if index <= start_move or pass_count == 0:
                            # 40手目以前はスキップ
                            continue
                        precp = scores[index - 2]
                        prevacp = scores[index - 3]
                        poor =  precp + prevacp
                        pih1 = piece_in_hand1[index - 2]
                        pih2 = piece_in_hand2[index - 2]
                        #print(f"持ち駒: {pih}")
                        before_thinking_time = thinking_times[index - 2] if index - 1 < len(thinking_times) else "N/A"
                        if rule == zero and turn == one and short_rule_time_S >= zero:
                            if before_thinking_time < short_rule_havetime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        elif rule == zero and turn == one and short_rule_time_S < zero:
                            if before_thinking_time < short_rule_notime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        elif rule == zero and turn == zero and short_rule_time_F >= zero:
                            if before_thinking_time < short_rule_havetime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        elif rule == zero and turn == zero and short_rule_time_F < zero:
                            if before_thinking_time < short_rule_notime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        elif rule == one and turn == one and middle_rule_time_S >= zero:
                            if before_thinking_time < middle_rule_havetime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        elif rule == one and turn == one and middle_rule_time_S < zero:
                            if before_thinking_time < short_rule_notime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        elif rule == one and turn == zero and middle_rule_time_F >= zero:
                            if before_thinking_time < middle_rule_havetime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        elif rule == one and turn == zero and middle_rule_time_F < zero:
                            if before_thinking_time < middle_rule_notime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        elif rule == two and turn == one and long_rule_time_S >= zero:
                            if before_thinking_time < long_rule_havetime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        elif rule == two and turn == one and long_rule_time_S < zero:
                            if before_thinking_time < long_rule_notime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        elif rule == two and turn == zero and long_rule_time_F >= zero:
                            if before_thinking_time < long_rule_havetime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        elif rule == two and turn == zero and long_rule_time_F < zero:
                            if before_thinking_time < long_rule_notime:
                                lgtime = 0
                            else:
                                lgtime = 1
                        
                            
                        match = 1 if bestmove.replace(' ', '') == Rmove.replace(' ', '') else 0
                        #print(rule)
                        row_data = [rule, match, turn, current_score, precp, prevacp, poor,legal_move_count, before_thinking_time ,current_thinking_time, lgtime, pih1, pih2]

                        with open(csv_output_file, 'a', encoding='utf-8', newline='') as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerow(row_data)

                        if index % 2 != 0:  # 先手の手番 1
                            if bestmove.replace(' ', '') == Rmove.replace(' ', ''):
                                count1 += 1
                            moves1 += 1
                            scores1.append(current_score)
                        else:  # 後手の手番 0
                            if bestmove.replace(' ', '') == Rmove.replace(' ', ''):
                                count2 += 1
                            moves2 += 1
                            scores2.append(current_score)
            if pass_count == 0:
                rule = rulejudge(thinking_times)
    engine.send("quit")




    if isinstance(engine, Execute):
        engine.terminate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV Search Tool")
    parser.add_argument("engineName", help="Path to the engine executable")
    parser.add_argument("usi_folder")
    parser.add_argument("outputDir", help="Directory to save output files")
    parser.add_argument("csv_output_file", help="CSV output file name")
    parser.add_argument("maxnodes", type=int, help="Max nodes for engine search")
    args = parser.parse_args()

    os.makedirs(args.outputDir, exist_ok=True)
    csv_output_file = os.path.join(args.outputDir, args.csv_output_file)

    for filename in os.listdir(args.usi_folder):
        if filename.endswith(".usi"):
            file_path = os.path.join(args.usi_folder, filename)
            main(file_path, csv_output_file)


        


