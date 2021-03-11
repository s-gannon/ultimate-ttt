import uttt
import random as rand
from consts import X, O, EMPTY, DRAW

game = uttt.uttt()
pla1, pla2 = X,O        #holds the mark that player 1 and 2 will be
plaTurn = X             #this makes it so X goes first; can change later
keepGeneratingFlag = True
while keepGeneratingFlag:
    lastSubboard = -1       #-1 if any board can be chosen, else it's 0-8
    moves = ""
    game.reset()
    print()
    while game.getWin() == EMPTY:
        boardPos, subboardPos = (lastSubboard if lastSubboard != -1 else rand.randint(0,8)), rand.randint(0,8)   #the board and subboard to move in
        while game.getPos(boardPos, subboardPos) != EMPTY:
            if lastSubboard == -1:
                boardPos = rand.randint(0,8)
            else:
                boardPos = lastSubboard
            subboardPos = rand.randint(0,8)
        lastSubboard = game.setPos(plaTurn, boardPos, subboardPos)
        plaTurn = (O if plaTurn == X else X)    #switches player turn
        game.checkWin()     #at the end of the turn, check for a win
        moves += str(boardPos+1) + str(subboardPos+1) + ":"
    game.print()
    moves = moves[0:len(moves)-1]
    if game.getWin() == X:
        print("\n\nX wins the game!")
    elif game.getWin() == O:
        print("\n\nO wins the game!")
    elif game.getWin() == DRAW:
        print("\n\nDraw!")
    else:
        print("\nError!")
    print("\n" + moves)
    
    if input("Generate another game? (y/n):").lower()[0] == "n":
        keepGeneratingFlag = False
    

