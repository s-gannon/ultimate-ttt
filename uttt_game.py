import uttt
from consts import X, O, EMPTY

game = uttt.uttt()
pla1, pla2 = 0,0        #holds the mark that player 1 and 2 will be
plaTurn = X             #this makes it so X goes first; can change later
lastSubboard = -1       #-1 if any board can be chosen, else it's 0-8
moves = ""

while (pla1 != X and pla1 != O):
    inp = input("Will player one be X or O?: ").upper()
    if inp[0] == "X":
        pla1 = X
    elif inp[0] == "O":
        pla1 = O

while game.getWin() == EMPTY:
    boardPos, subboardPos = -1,-1   #the board and subboard to move in
    game.print()
    if lastSubboard == -1:
        while boardPos == -1 or (boardPos > 8 or boardPos < 0):
            boardPos = int(input("\nEnter the board position to move in (1-9): "))-1
    else:
        boardPos = lastSubboard
    while subboardPos == -1 or (subboardPos > 8 or subboardPos < 0):
        subboardPos = int(input(f"\nEnter the subboard position to move in (1-9): {boardPos+1},"))-1
    hold = game.setPos(plaTurn, boardPos, subboardPos)
    while hold == -2:
        subboardPos = int(input(f"\nEnter a different subboard position to move in (1-9): {boardPos+1},"))-1
        hold = game.setPos(plaTurn, boardPos, subboardPos)
    lastSubboard = hold
    plaTurn = (O if plaTurn == X else X)    #switches player turn
    game.checkWin()     #at the end of the turn, check for a win
    moves += str(boardPos) + str(subboardPos) + ":"
moves = moves[0,len(moves)-1]
if game.getWin() == X:
    print("\n\nX wins the game!")
elif game.getWin() == O:
    print("\n\nY wins the game!")
elif game.getWin() == DRAW:
    print("\n\nDraw!")
else:
    print("\nHuge ass error!")
print("\n" + moves)
