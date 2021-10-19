import ttt
from consts import X, O, EMPTY, DRAW
class uttt():
#------------------Constructor-----------------#
    def __init__(self):
        self.board = []
        self.winStatus = EMPTY
        for i in range(9):
            self.board.append(ttt.ttt())
#---------------Accessor methods---------------#
    #gets the win status of the game
    def getWinStatus(self):
        return self.winStatus
    #gets the mark at the position on that subboard
    def getMarkAtPos(self, subboard, pos):
        return self.getSubboard(subboard).getMarkAtPos(pos)
    #gets the smaller board (the ttt object) at the specified position 'subboard' on the big board
    def getSubboard(self, subboard):
        return self.board[subboard]
#---------------Mutator methods----------------#
    #sets the value on the suboard at the specified position 'pos' to a value 'mark'
    def makeMove(self, mark, subboard, pos):
        self.getSubboard(subboard).makeMove(mark, pos)
    #updates the winStatus of the UTTT object
    def updateWinStatus(self):
        b = []
        for i in range(len(self.board)):
            b.append(self.getSubboard(i).getWinStatus())
        rows = [[b[0],b[1],b[2]],[b[3],b[4],b[5]],[b[6],b[7],b[8]]]
        cols = [[b[0],b[3],b[6]],[b[1],b[4],b[7]],[b[2],b[5],b[8]]]
        diag = [[b[0],b[4],b[8]],[b[2],b[4],b[6]]]
        if [X,X,X] in rows or [X,X,X] in cols or [X,X,X] in diag:
            self.winStatus = X
        elif [O,O,O] in rows or [O,O,O] in cols or [O,O,O] in diag: #if there's a line of 3 O's or X's, then that mark wins the game
            self.winStatus = O
        elif EMPTY not in b:  #if there are no more empty spaces in the board
            self.winStatus = DRAW   #it's safe to assume that the board has been drawn
        else:
            self.winStatus = EMPTY
#----------------Other methods-----------------#
    #prints the board (man this code has been brought over from every iteration)
    def print(self):
        for w in range(3):  #"It just works" - Todd Howard
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        mark = ""
                        if self.getMarkAtPos(y + (w*3), z + (x*3)) == X:
                            mark = "X"
                        elif self.getMarkAtPos(y + (w*3), z + (x*3)) == O:
                            mark = "O"
                        else:
                            mark = " " #could change to a # if wanted
                        print(mark,end="")
                        if not y == z == 2:
                            print("|",end="")
                if x != 2:
                    print("\n-+-+-|-+-+-|-+-+-")
            if w != 2:
                print("\n-----+-----+-----")
        print()
    #converts the board to a string that looks like a UTTT board
    def asciiString(self):
        boardStr = ""
        for w in range(3):  #"It just works" - Todd Howard
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        mark = ""
                        if self.getMarkAtPos(y + (w*3), z + (x*3)) == X:
                            mark = "X"
                        elif self.getMarkAtPos(y + (w*3), z + (x*3)) == O:
                            mark = "O"
                        else:
                            mark = " " #could change to a # if wanted
                        boardStr += mark
                        if not y == z == 2:
                            boardStr += "|"
                if x != 2:
                    boardStr += "\n-+-+-|-+-+-|-+-+-\n"
            if w != 2:
                boardStr += "\n-----+-----+-----\n"
        return (boardStr + "\n")
    #checks the legality of a move; returns true if legal, false if illegal
    def checkLegal(self, lastpos, subboard, pos):
        self.updateWinStatus()
        if lastpos == -1:    #special case; this is for the start of the game to allow any move to be made
            if subboard in range(9) and pos in range(9):
                if self.getSubboard(subboard).checkLegal(pos):
                    return True
        if subboard in range(9) and lastpos in range(9) and pos in range(9):   #checks to see if all positions are in between 0-8
            if self.getSubboard(lastpos).getWinStatus() == EMPTY:    #checks to see if the last move pointed to a board that isn't won
                if lastpos == subboard:   #checks to make sure that, if above is the case, lastpos and subboard are the same (because they have to)
                    if self.getSubboard(subboard).checkLegal(pos):    #checks to see if the move is legal on the lower level (ttt object)
                        return True
            else:   #otherwise, there's the other case that you're allowed to move anywhere due to being sent to a won/drawn board
                if lastpos != subboard:   #this has to be true because you can't mark in a won/drawn board
                    if self.getSubboard(subboard).checkLegal(pos):    #checks to see if the move is legal on the lower level (ttt object)
                        return True
        return False
    #resets the board to all empty and the win status to empty
    def reset(self):
        self.winStatus = EMPTY
        for i in range(9):
            self.getSubboard(i).reset()
    #generates the legal move list given the position in the subboard of the last move
    def generateLegalMoveList(self, pos):
        legal = []
        for sb in range(9):
            sublegal = []
            for p in range(9):
                sublegal.append(self.checkLegal(pos, sb, p))
            legal.append(sublegal)
        return legal
