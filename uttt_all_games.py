from consts import X, O, DRAW, EMPTY, ASCII_OFFSET

from dask.distributed import Client, progress
#import multiprocessing as mp
import time
import uttt

def recursiveMakeMove(utttObj, mark, lastpos, gamestr="", filename=""):
    if utttObj.getWinStatus() != EMPTY:
        winchar = ""
        if utttObj.getWinStatus() == O:
            winchar = "0"
        elif utttObj.getWinStatus() == X:
            winchar = "1"
        elif utttObj.getWinStatus() == DRAW:
            winchar = "2"
        allGames = open(filename + ".txt", "a")
        allGames.write(gamestr + winchar + "\n")
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
                        filename = (filename if filename != "" else (str(sb) + str(p) + "_games"))
                        if utttObj.getSubboard(p).getWinStatus() != EMPTY:
                            recursiveMakeMove(utttObj, (O if mark == X else X), -1, gamestr + chr(int(str(sb) + str(p)) + ASCII_OFFSET), filename)
                        else:
                            recursiveMakeMove(utttObj, (O if mark == X else X), p, gamestr + chr(int(str(sb) + str(p)) + ASCII_OFFSET), filename)
                        utttObj.makeMove(EMPTY, sb, p)
                        utttObj.updateWinStatus()
        else:               #else if it's just a normal move
            for p in range(9):
                if utttObj.checkLegal(lastpos, lastpos, p):  #if it's a legal move
                    utttObj.makeMove(mark, lastpos, p)
                    utttObj.updateWinStatus()
                    filename = (filename if filename != "" else (str(lastpos) + str(p) + "_games"))
                    if utttObj.getSubboard(p).getWinStatus() != EMPTY:
                        recursiveMakeMove(utttObj, (O if mark == X else X), -1, gamestr + chr(int(str(lastpos) + str(p)) + ASCII_OFFSET), filename)
                    else:
                        recursiveMakeMove(utttObj, (O if mark == X else X), p, gamestr + chr(int(str(lastpos) + str(p)) + ASCII_OFFSET), filename)
                    utttObj.makeMove(EMPTY, lastpos, p)
                    utttObj.updateWinStatus()

if __name__ == "__main__":
    futures = []
    ips = ["192.168.59.4", "192.168.59.5", "192.168.59.6", "192.168.59.7"]
    port = "5959"

    startingSubboard = int(input("Enter in a starting subboard or -1 to start from beginning: "))
    startingPos = -1
    if startingSubboard != -1:
        startingPos = int(input("Enter in a starting position or -1 to start from beginning: "))
        if startingPos != -1:   #startingSubboard and startingSubpos specified
            gameString = chr(int(str(startingSubboard) + str(startingPos)) + ASCII_OFFSET)
            mathString = str(startingSubboard+1) + str(startingPos+1)
            for i in range(9):
                game = uttt()

                game.makeMove(X, startingSubboard, startingPos)
                if game.checkLegal(startingPos, startingPos, i):
                    client = Client(ips[i % len(ips)] + ":" + port) #we left off here; whoops
                    gameString += chr(int(str(startingPos) + str(i)) + ASCII_OFFSET)

                    game.makeMove(O, startingPos, i)
                    futures.append(client.submit(recursiveMakeMove, (game, X, i, gameString, mathString + "_games")))
        else:   #startingSubboard is specified but startingPos is not
            for i in range(9):
                client = Client(ips[i % len(ips)] + ":" + port)
                game = uttt.uttt()
                gameString = chr(int(str(startingSubboard) + str(i)) + ASCII_OFFSET)
                mathString = str(startingSubboard+1) + str(i+1)

                game.makeMove(X, startingSubboard, i)
                futures.append(client.submit(recursiveMakeMove, (game, O, i, gameString, mathString + "_games")))
    else: #no startingSubboard or startingPos (by default)
        for i in range(9):
            client = Client(ips[i % len(ips)] + ":" + port)
            game = uttt.uttt()

            futures.append(client.submit(recursiveMakeMove, (game, X, i, "",)))

    for future in futures:
        future.close()

    print("Finally done with the job. Passed arguments: ({},{})\n".format(startingSubboard, startingPos))
