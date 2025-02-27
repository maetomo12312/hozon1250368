import subprocess

# 実行コマンドのリスト
commands = [
    ["python", "./rem-csa_to_hcpeT.py", "./kifudata/tamesu/", "./train.hcpe", "./test.hcpe"],
    #["python", "./rem-csa_to_hcpeT.py", "./kifudata/Trate_1_735/", "./train.hcpe", "./test.hcpe"],
    #["python", "./pydlshogi2/logtrain.py", "./train.hcpe", "./test.hcpe", "--epoch", "10", "--checkpoint", "./checkpoints/Tcheckpoint1_735.pth"],
    #["python", "./rem-csa_to_hcpeT.py", "./kifudata/Trate_736_1077/", "./train.hcpe", "./test.hcpe"],
    #["python", "./pydlshogi2/logtrain.py", "./train.hcpe", "./test.hcpe", "--epoch", "10", "--checkpoint", "./checkpoints/Tcheckpoint736_1077.pth"],
    #["python", "./rem-csa_to_hcpeT.py", "./kifudata/Trate_1078_1374/", "./train.hcpe", "./test.hcpe"],
    #["python", "./pydlshogi2/logtrain.py", "./train.hcpe", "./test.hcpe", "--epoch", "10", "--checkpoint", "./checkpoints/Tcheckpoint1078_1374.pth"],
    #["python", "./rem-csa_to_hcpeT.py", "./kifudata/Trate_1375_1687/", "./train.hcpe", "./test.hcpe"],
    #["python", "./pydlshogi2/logtrain.py", "./train.hcpe", "./test.hcpe", "--epoch", "10", "--checkpoint", "./checkpoints/Tcheckpoint1375_1687.pth"],
    #["python", "./rem-csa_to_hcpeT.py", "./kifudata/Trate_1688_2006/", "./train.hcpe", "./test.hcpe"],
    #["python", "./pydlshogi2/logtrain.py", "./train.hcpe", "./test.hcpe", "--epoch", "10", "--checkpoint", "./checkpoints/Tcheckpoint1688_2006.pth"],
    #["python", "./rem-csa_to_hcpeT.py", "./kifudata/Trate_2007_2845/", "./train.hcpe", "./test.hcpe"],
    #["python", "./pydlshogi2/logtrain.py", "./train.hcpe", "./test.hcpe", "--epoch", "10", "--checkpoint", "./checkpoints/Tcheckpoint2007_2845.pth"],
]

# コマンドを順次実行
for i, command in enumerate(commands):
    print(f"実行中のコマンド: {' '.join(command)}")
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"エラーが発生しました。コマンドの実行を停止します。: {' '.join(command)}")
        break
    print(f"コマンド {i+1} が正常に完了しました。")
else:
    print("すべてのコマンドが正常に完了しました。")
