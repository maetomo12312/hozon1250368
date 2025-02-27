import subprocess

# 実行コマンドのリスト
commands = [
    #["python", "./reSearch.py", ".\\mcts_player6.bat", ".\\usistorage\\2007_2845_usi", ".\\Searchresult", "SearchR2007_2845.txt", "100"],
    #["python", "./reSearch.py", ".\\mcts_player5.bat", ".\\usistorage\\1688_2006_usi", ".\\Searchresult", "SearchR1688_2006.txt", "100"],
    #["python", "./reSearch.py", ".\\mcts_player4.bat", ".\\usistorage\\1375_1687_usi", ".\\Searchresult", "SearchR1375_1687.txt", "100"],
    #["python", "./reSearch.py", ".\\mcts_player3.bat", ".\\usistorage\\1078_1374_usi", ".\\Searchresult", "SearchR1078_1374.txt", "100"],
    #["python", "./reSearch.py", ".\\mcts_player2.bat", ".\\usistorage\\736_1077_usi", ".\\Searchresult", "SearchR736_1077.txt", "100"],
    #["python", "./reSearch.py", ".\\mcts_player.bat", ".\\usistorage\\1_735_usi", ".\\Searchresult", "SearchR1_735.txt", "100"],
    #["python", "./reSearch.py", ".\\mcts_player6.bat", ".\\usistorage\\1_735_usi", ".\\Searchresult", "SearchR-R2007_2845.txt", "100"],
    #["python", "./reSearch.py", ".\\mcts_player.bat", ".\\usistorage\\2007_2845_usi", ".\\Searchresult", "SearchR-R1_735.txt", "100"],
    #["python", "./testSearch.py", ".\\mcts_player.bat", ".\\usistorage\\2007_2845_usi", ".\\Searchresult", "SearchR-test.txt", "100"],
    #["python", "./testSearch.py", ".\\mcts_player.bat", ".\\usistorage\\hontoka", ".\\Searchresult", "SearchR-test.txt", "100"],
    #["python", "./testSearch.py", ".\\mcts_player.bat", ".\\usistorage\\hontoka2", ".\\Searchresult", ".\\csvResult\\SearchR_output", "100"],
    #["python", "./testSearch.py", ".\\mcts_player.bat", ".\\usistorage\\test_usi", ".\\Searchresult", "SearchR-test.txt", ".\\tameshi-test\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player.bat", ".\\usistorage\\test_usi", ".\\Searchresult", "SearchR-test11.txt", ".\\Rrate-test_1-735\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player.bat", ".\\usistorage\\Trate-test_1-735_usi", ".\\Searchresult", "SearchR-test1.txt", ".\\Rrate-test_1-735\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player6.bat", ".\\usistorage\\Trate_2007-2845_usi", ".\\Searchresult", "SearchR6.txt", ".\\Rrate_2007-2845\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player6.bat", ".\\usistorage\\Trate-test_2007-2845_usi", ".\\Searchresult", "SearchR-test6.txt", ".\\Rrate-test_2007-2845\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player2.bat", ".\\usistorage\\Trate_736-1077_usi", ".\\Searchresult", "SearchR2.txt", ".\\Rrate_736-1077\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player2.bat", ".\\usistorage\\Trate-test_736-1077_usi", ".\\Searchresult", "SearchR-test2.txt", ".\\Rrate-test_736-1077\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player3.bat", ".\\usistorage\\Trate_1078-1374_usi", ".\\Searchresult", "SearchR3.txt", ".\\Rrate_1078-1374\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player3.bat", ".\\usistorage\\Trate-test_1078-1374_usi", ".\\Searchresult", "SearchR-test3.txt", ".\\Rrate-test_1078-1374\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player4.bat", ".\\usistorage\\Trate_1375-1687_usi", ".\\Searchresult", "SearchR4.txt", ".\\Rrate_1375-1687\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player4.bat", ".\\usistorage\\Trate-test_1375-1687_usi", ".\\Searchresult", "SearchR-test4.txt", ".\\Rrate-test_1375-1687\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player5.bat", ".\\usistorage\\Trate_1688-2006_usi", ".\\Searchresult", "SearchR5.txt", ".\\Rrate_1688-2006\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player5.bat", ".\\usistorage\\Trate-test_1688-2006_usi", ".\\Searchresult", "SearchR-test5.txt", ".\\Rrate-test_1688-2006\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player3.bat", ".\\usistorage\\Trate_1078-1374_usi1", ".\\Searchresult", ".\\Rrate_1078-1374\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player6.bat", ".\\usistorage\\Trate_2007-2845_usi1", ".\\Searchresult", ".\\Rrate_2007-2845\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player6.bat", ".\\usistorage\\Trate_2007-2845_usi2", ".\\Searchresult", ".\\Rrate_2007-2845\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player6.bat", ".\\usistorage\\Trate_2007-2845_usiZ", ".\\Searchresult", ".\\RRrate_2007-2845\\SearchR", "100"],
    #["python", "./testSearch.py", ".\\mcts_player6.bat", ".\\usistorage\\Trate-test_2007-2845_usi", ".\\Searchresult", ".\\RRrate_2007-2845\\SearchR", "100"],
    
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
