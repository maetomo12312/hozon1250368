import subprocess
import sys
import time
import argparse
import os 


accuracies1 = []
accuracies2 = []

class Execute(object):
    """外部プログラムを実行。stdinとstdoutで対話する。"""
    """出典: https://qiita.com/kei0425/items/69fe513caab654a00e73  """
    
    # 初期化、コマンドライン引数設定
    def __init__(self, *args_1, **args_2):
        # usiの棋譜をUTF―8にエンコード
        if 'encoding' in args_2:
            self.encoding = args_2.pop('encoding')
        else:
            self.encoding = 'utf-8'
        self.popen = subprocess.Popen(*args_1, stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      encoding=self.encoding, **args_2)

    # エンジンとの送受信
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

    # 以下は追加コード
    def recieveUntilEOF(self):
        """ eofが来るまで行を読み続け, それまでの入力を返す """
        self.popen.stdout.flush()
        info = ""
        while True:
            line = self.popen.stdout.readline()
            if "eof" in line :
                break
            info = info + line
        return info
        
    def recieveUntilBM(self, BM):
        """ BestMove が返ってくるまで受信を続け、最後の探索ログを返す """
        self.popen.stdout.flush()
        info = ""
        while True:
            line = self.popen.stdout.readline()
            if "bestmove" in line :
                BM.append(line[9:13])
                #print(BM)
                #print(line.replace('bestmove', ''))
                break
            # info = info + line
            if "bound" in line :
                continue
            info = line
        return BM
        
    def recieveUntilReadyOK(self):
        """ readyOK が返ってくるまで受信を続ける """
        self.popen.stdout.flush()
        info = ""
        while True:
            line = self.popen.stdout.readline()
            if "readyok" in line :
                break;
            info = info + line
        return info

    # （強制）終了
    def terminate(self):
        try :
            self.popen.terminate()
        except ProcessLookupError:
            pass

def usage():
    print("Usage : searchUsiFile.py Engine UsiFile SearchNode ")

def main(fileName):
    BM = []
    accuracy1 = 0 # 一致率 先手
    accuracy2 = 0 # 一致率 後手
    count1 = 0 # 一致数
    count2 = 0 
    #allmoves = 0 # 総手数
    moves1 = 0 # 先手手数
    moves2 = 0 # 後手手数
    Rmove = '' # 実際の手
    engineName = args.engineName
    maxnodes   = args.maxnodes
    index = 0
     
	# engine 設定
    engine = Execute([engineName])
    engine.send("setoption name Threads value 1", recieve=False, incr=True)
    engine.send("isready", recieve=False, incr=True)
    engine.recieveUntilReadyOK()

    # 読み込んだ棋譜を一手ずつ見たい
    with open(fileName) as f:
        line = f.readline()
        while line :
            if "position" in line :
                if index == 0:
                    engine.send("usinewgame", recieve=False, incr=True)
                    engine.send('start position', recieve=False, incr=True)
                    gostr = "go nodes " + str(maxnodes)
                    engine.send(gostr, recieve=False, incr=True)
                    engine.recieveUntilBM(BM)
                
                engine.send("usinewgame", recieve=False, incr=True)
                engine.send(line, recieve=False, incr=True)
                gostr = "go nodes " + str(maxnodes)
                engine.send(gostr, recieve=False, incr=True)
                engine.recieveUntilBM(BM)

                # 後手の手の一致率を計算したい(先手も実装出来たらやる)
                Rmove = line[-6:-1]
                index += 1
                bestmove1 = str(BM[index-1])
                bestmove2 = str(BM[index-1])
                #print('BM '+str(BM)+'index '+str(index))
                #allmoves += 1
                if index % 2 != 0:
                    # 先手の一致率を計算
                    #print('先手 ' + Rmove + 'best ' + bestmove1)
                    if (bestmove1.replace(' ','') == Rmove.replace(' ','')):
                        count1 += 1
                        print('先手が一致しました',bestmove1,Rmove)
                    if bestmove1 == 'resi':
                        continue
                    moves1 += 1
                else:
                    # 後手の一致率を計算
                    #print('後手 ' + Rmove + 'best ' + bestmove2)
                    if (bestmove2.replace(' ','') == Rmove.replace(' ','')) and index > 0:
                        count2 += 1
                        print('後手が一致しました',bestmove2,Rmove)
                    if bestmove2 == 'resi' and index > 0:
                        continue
                    moves2 += 1                 
                line = f.readline()
        engine.send("quit")
    print('a')
    accuracy2 = (count2 / moves2) * 100
    accuracy1 = (count1 / moves1) * 100
    accuracies1.append(accuracy1)
    accuracies2.append(accuracy2)
    # 一致率を保存
    print('b')
    with open(args.outputDir + '/' + args.filename + '.txt',"a", encoding = "UTF-8") as f:
            f.writelines(filename + 'の後手の一致率は' + str(accuracy2) + '%, 先手の一致率は' + str(accuracy1) + 'です\n')
    print('c')
    if "engine" in locals() and isinstance(engine, Execute) :
        engine.terminate()

if __name__ == '__main__':
    # 引数を指定
    parser = argparse.ArgumentParser()
    parser.add_argument("engineName")
    parser.add_argument("usi_folder")
    parser.add_argument("outputDir")
    parser.add_argument("filename")
    parser.add_argument("maxnodes" , type=int)
    args = parser.parse_args()
    os.makedirs(args.outputDir, exist_ok=True)
    filenum = 0
    
    for filename in os.listdir(args.usi_folder):
        filenum += 1
        file_path = args.usi_folder + "\\" + filename
        main(file_path)
    print('d')
    # グラフの作成
    # 縦軸：accuracies、 横軸：filenum
    print(accuracies1)
    print(accuracies2)