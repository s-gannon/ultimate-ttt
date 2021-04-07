import ttt

test = ttt.ttt()

def setBoard(tttObj, moves):
    for i in range(len(tttObj.board)):
        tttObj.setPos(moves[i], i)

def getMarkTest(tttObj, pos, expected):
    print("Input: getMark({})".format(pos))
    print("Output: {}".format(tttObj.getMark(pos)))
    print("Expect: {}".format(expected))

def setPosTest(tttObj, mark, pos, expected):
    print("Input: setPos({},{})".format(mark, pos))
    tttObj.setPos(mark, pos)
    print("Output: {}".format(tttObj.board[pos]))
    print("Expect: {}".format(expected))
