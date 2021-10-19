from consts import X, O, EMPTY, DRAW

import multiprocessing as mp
import time
import uttt

global winList
global numGames

winList = [0,0,0]
numGames = [0]

def recursiveMakeMove(utttObj, mark, lastpos):
    if utttObj.getWinStatus() != EMPTY:
        numGames[0] += 1
        if utttObj.getWinStatus() == X:
            winList[0] += 1
        elif utttObj.getWinStatus() == O:
            winList[1] += 1
        elif utttObj.getWinStatus() == DRAW:
            winList[2] += 1
        print(str(numGames[0]))
        return
    else:
        nextpos = -1
        nextSubboard = lastpos
        if lastpos == -1:   #if we're allowed to move anywhere
            for sb in range(9):
                for p in range(9):
                    if utttObj.checkLegal(lastpos, sb, p):  #if it's a legal move
                        utttObj.makeMove(mark, sb, p)
                        utttObj.updateWinStatus()
                        if utttObj.getSubboard(p).getWinStatus() != EMPTY:
                            recursiveMakeMove(utttObj, (O if mark == X else X), -1)
                        else:
                            recursiveMakeMove(utttObj, (O if mark == X else X), p)
                        utttObj.makeMove(EMPTY, sb, p)
                        utttObj.updateWinStatus()
        else:               #else if it's just a normal move
            for p in range(9):
                if utttObj.checkLegal(lastpos, lastpos, p):  #if it's a legal move
                    utttObj.makeMove(mark, lastpos, p)
                    utttObj.updateWinStatus()
                    if utttObj.getSubboard(p).getWinStatus() != EMPTY:
                        recursiveMakeMove(utttObj, (O if mark == X else X), -1)
                    else:
                        recursiveMakeMove(utttObj, (O if mark == X else X), p)
                    utttObj.makeMove(EMPTY, lastpos, p)
                    utttObj.updateWinStatus()

if __name__ == "__main__":
    processList = []
    startingMove = [4,4]
    for i in range(4):
        gameString = str(startingMove[0]) + str(i) + "-"
        mathString = str(startingMove[0]+1) + str(i+1)
        game = uttt.uttt()

        game.makeMove(X, startingMove[0], startingMove[1])
        game.makeMove(O, startingMove[1], i)
        processList.append(mp.Process(target=recursiveMakeMove, args=(game, X, i)))
    for i in range(5,9):
        gameString = str(startingMove[0]) + str(i) + "-"
        mathString = str(startingMove[0]+1) + str(i+1)
        game = uttt.uttt()

        game.makeMove(X, startingMove[0], startingMove[1])
        game.makeMove(O, startingMove[1], i)
        processList.append(mp.Process(target=recursiveMakeMove, args=(game, X, i)))

    for p in processList:
        p.start()
    for p in processList:
        p.join()
    for p in processList:
        p.close()

    print("For the starting move " + str(int(startingMove[0])+1) + str(int(startingMove[1])+1) + " here are some results: ")
    print("Wins [X,O,DRAW]: " + str(winList))
    print("We're no strangers to love. You know the rules, and so do I")
    input("")
