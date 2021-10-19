from consts import X, O, EMPTY

import multiprocessing as mp
import time
import uttt

def recursiveMakeMove(utttObj, mark, lastpos, gamestr, filename):
    if utttObj.getWinStatus() != EMPTY:
        mathString = ""
        allGames = open(filename + ".txt", "a")
        #converting the cs 0-index string into a 1-index string the math people can read
        for i in gamestr[:-1].split("-"):
            mathString += str(int(i) + 11) + "-"
        mathString = mathString[:-1]
        #prints out this debug statement every 1000 games in order to be sure that things are happening
        # if gamestr[:-1] in games:
        #     raise AlreadyGeneratedError(gamestr[:-1], games.index(gamestr[:-1]))
        # games.append(gamestr[:-1])
        allGames.write(mathString + "\n")
        allGames.close()
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
                            recursiveMakeMove(utttObj, (O if mark == X else X), -1, gamestr + str(sb) + str(p) + "-", filename)
                        else:
                            recursiveMakeMove(utttObj, (O if mark == X else X), p, gamestr + str(sb) + str(p) + "-", filename)
                        utttObj.makeMove(EMPTY, sb, p)
                        utttObj.updateWinStatus()
        else:               #else if it's just a normal move
            for p in range(9):
                if utttObj.checkLegal(lastpos, lastpos, p):  #if it's a legal move
                    utttObj.makeMove(mark, lastpos, p)
                    utttObj.updateWinStatus()
                    if utttObj.getSubboard(p).getWinStatus() != EMPTY:
                        recursiveMakeMove(utttObj, (O if mark == X else X), -1, gamestr + str(lastpos) + str(p) + "-", filename)
                    else:
                        recursiveMakeMove(utttObj, (O if mark == X else X), p, gamestr + str(lastpos) + str(p) + "-", filename)
                    utttObj.makeMove(EMPTY, lastpos, p)
                    utttObj.updateWinStatus()

if __name__ == "__main__":
    processList = []
    startingSubboard = 0
    for i in range(9):
        gameString = str(startingSubboard) + str(i) + "-"
        mathString = str(startingSubboard+1) + str(i+1)
        game = uttt.uttt()

        game.makeMove(X, startingSubboard, i)
        processList.append(mp.Process(target=recursiveMakeMove, args=(game, O, i, gameString, mathString + "_games")))

    for p in processList:
        p.start()
    for p in processList:
        p.join()
    for p in processList:
        p.close()

    print("We're no strangers to love. You know the rules, and so do I")
