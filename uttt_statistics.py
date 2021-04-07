#-----------------Imports---------------#
import re
import uttt
import time
import numpy as np
import matplotlib.pyplot as plt
import random as rand
from consts import X, O, EMPTY, DRAW
#----------------Functions--------------#
def generateLegalMoveList(utttObj, lastSubpos):
    legal = []
    for p in range(9):
        sublegal = []
        for sp in range(9):
            sublegal.append(utttObj.checkLegal(lastSubpos, p, sp))
        legal.append(sublegal)
    return legal
#---------------Variables---------------#
numMoves = []       #list of the num of moves to average later
numGames = 0            #the number of games to be played
plaTurn = X             #denotes who's turn it is; whatever this is set to is who will always go first in a given game
lastSubboard = -1       #keeps track of last subpos to use in legal move generation
pos, subpos = 0,0       #inits the pos and subpos
startMove = [-1,-1]     #starting move
numWins = [0,0,0]       #X wins, O wins, and draws
midMovesGot = [0, 0]    #number of x5 moves got by winner and loser
centerMovesGot = [0, 0] #number of 55 moves got by winner and loser
winSubboards = [0]*9    #subboards the winner claims
loseSubboards = [0]*9   #subboards the loser claims
game = uttt.uttt()      #uttt object

times = []
#-----------------Main------------------#
for t in range(int(input("Enter the number of simulations to run: "))):
    times.append(0)
    startTime = time.time()
    for g in range(t+1):
        #the below resets any values critical to the game back to default
        pos, subpos = 0, 0
        game.reset()    #very important; hopefully this doesn't break shit by not working correctly, but I have faith
        lastSubboard = startMove[1]     #big brain time: startMove is init to -1,-1 so if no start move is chosen, this should be -1
        plaTurn = (X if startMove[1] == -1 else O)  #X if no startMove, O otherwise
        numMoves.append(0)

        ###   MAIN GAME LOOP   ###
        if startMove != [-1,-1]:
            game.makeMove(X, startMove[0], startMove[1])
            game.updateWinStatus()
        while game.getWinStatus() == EMPTY:
            winningMoveFlag = False
            legalMoves = generateLegalMoveList(game, lastSubboard)  #generates all legal moves at the top of each move
            ###'Check for winning move' code below
            game.updateWinStatus()
            for p in range(9):  #for every subboard
                for sp in range(9): #for every pos in the subboard (denoted as subposition)
                    if not winningMoveFlag: #if a winning move has not been found
                        if legalMoves[p][sp]:   #if the move is a legal move
                            game.makeMove(plaTurn, p, sp)       #make 'potential' move (potential because it may be reverted)
                            game.updateWinStatus()              #update win status
                            if game.getWinStatus() != EMPTY:    #if the win status is now not empty
                                winningMoveFlag = True              #we have a winning move, set the flag to true
                                pos, subpos = p, sp
                            else:
                                game.makeMove(EMPTY, p, sp)     #if the move isn't a winning one, set the position back to EMPTY val (revert back)
                                game.updateWinStatus()          #update win back to original value
            if not winningMoveFlag: #if no winning move was found
                pos, subpos = rand.randint(0,8), rand.randint(0,8)  #pick a random move
                while not legalMoves[pos][subpos]:                  #if that move is not a legal move (the value in the array is False)
                    pos, subpos = rand.randint(0,8), rand.randint(0,8)  #pick another random move until you get a legal one
                game.makeMove(plaTurn, pos, subpos)                 #makes move that has been determined to be legal
            game.updateWinStatus()  #update win status
            numMoves[g] += 1
            lastSubboard = subpos   #the last subboard will be = to the subpos move made this round
            plaTurn = (O if plaTurn == X else X)    #switches players
        ###   STATISTICS SHIT   ###
        winner = game.getWinStatus()    #bad code below; I'm lazy and don't feel like flexing on this part/making this good
        if winner == X: #if X is the winner
            numWins[0] += 1 #adds 1 to the X win part of the array
            for i in range(9):  #for every subboard
                sb = game.getSubboard(i)    #get subboard at position i
                if sb.getWinStatus() == X:  #if the subboard was won by X (the winner)
                    winSubboards[i] += 1        #add it to the list of boards claimed by winner
                elif sb.getWinStatus() == O:#if subboard was won by O (the loser)
                    loseSubboards[i] += 1
                if sb.getMarkAtPos(4) == X: #if the mark at x5 is X, add to winner stats
                    if i == 4:                  #if it's the 55 position
                        centerMovesGot[0] += 1
                    midMovesGot[0] += 1
                elif sb.getMarkAtPos(4) == O:   #if the mark at x5 is O, add to loser stats
                    if i == 4:                      #if it's the 55 position
                        centerMovesGot[1] += 1
                    midMovesGot[1] += 1
        elif winner == O: #if O is the winner
            numWins[1] += 1     #adds 1 to the O win part of the array
            for i in range(9):  #for every subboard
                sb = game.getSubboard(i)        #get subboard at position i
                if sb.getWinStatus() == O:      #if the subboard was won by O (the winner)
                    winSubboards[i] += 1            #add it to the list of boards claimed by winner
                elif sb.getWinStatus() == X:    #if subboard was won by X (the loser)
                    loseSubboards[i] += 1
                if sb.getMarkAtPos(4) == O:     #if the mark at x5 is O, add to winner stats
                    if i == 4:                      #if it's the 55 position
                        centerMovesGot[0] += 1          #add 1 to center moves got by winner
                    midMovesGot[0] += 1             #add 1 to mid moves got by winner
                elif sb.getMarkAtPos(4) == X:   #if the mark at x5 is X, add to loser stats
                    if i == 4:                      #if it's the 55 position
                        centerMovesGot[1] += 1
                    midMovesGot[1] += 1
        elif winner == DRAW:
            numWins[2] += 1
        else:
            print("If you're seeing this, something fucked up along the way and you should email me to fix it")
    avrgMoves = sum(numMoves)
    avrgMoves /= (t+1)
    endTime = time.time()
    times[t] = endTime - startTime
    print("Series {} completed".format(t+1))
plt.scatter(range(1,len(times)+1), times)
m, b = np.polyfit(range(1,len(times)+1), times, 1)
plt.plot(range(1,len(times)+1), m*range(1,len(times)+1) + b)
plt.xlabel("Number of games simulated")
plt.ylabel("Time (in seconds)")
plt.title("Time taken")
plt.show()
print("\ny = {}x + {}".format(m, b))
print(sum(times))
#DEMANDS
#BE ABLE TO SPECIFY WHICH MOVE WE START WITH, BUT HAVE THE OPTION OF RANDOM START AS WELL 	    DONE
#REQUIRE THAT IF WINNING MOVE IS AVAILABLE, COMPUTER MAKES THAT MOVE                            DONE
#RUN 100s OF GAMES WITH AN OUTPUT ANALYSIS                                                      in progress
    #OUTPUT ANALYSIS SHOULD INCLUDE:
    #PERCENTAGE OF GAMES X WON AND PERCENTAGE OF GAMES O WON AND GAMES DRAWN                    DONE
    #x5 MOVES THAT THE WINNER CLAIMED VS x5 MOVES THAT THE LOSER CLAIMED                        DONE
    #SUBBOARDS THE WINNER CLAIMED VS SUBBOARDS THE LOSER CLAIMED
    #HOW OFTEN WINNER CLAIMED MIDDLEMOST MOVE VS HOW OFTEN LOSER CLAIMED MIDDLE MOST MOVE       DONE
    #ANYTHING ELSE THAT COULD TRACK PATTERNS LIKE THIS