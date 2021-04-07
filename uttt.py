import ttt
from consts import X, O, EMPTY, DRAW
class uttt():
    def __init__(self):
        self.board = []
        self.winStatus = EMPTY
        for i in range(9):
            self.board.append(ttt.ttt())
#---------------Accessor methods---------------#
    #gets the win status of the game
    def getWinStatus(self):
        return self.winStatus
    #gets the mark at position 'pos','subpos'
    def getMarkAtPos(self, pos, subpos):
        return self.getSubboard(pos).getMarkAtPos(subpos)
    #gets the smaller board (the ttt object) at the position 'pos' on the board
    def getSubboard(self, pos):
        return self.board[pos]
#---------------Mutator methods----------------#
    #sets the board at position 'pos','subpos' to value 'mark'
    def makeMove(self, mark, pos, subpos):
        self.getSubboard(pos).makeMove(mark, subpos)

    def updateWinStatus(self):
        b = []
        for i in range(len(self.board)):
            b.append(self.getSubboard(i).getWinStatus())
        rows = [[b[0],b[1],b[2]],[b[3],b[4],b[5]],[b[6],b[7],b[8]]]
        cols = [[b[0],b[3],b[6]],[b[1],b[4],b[7]],[b[2],b[5],b[8]]]
        diag = [[b[0],b[4],b[8]],[b[2],b[4],b[6]]]
        """print(rows)
        print(cols)     #lol errors go brrr
        print(diag)"""
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

    def checkLegal(self, lastSubpos, pos, subpos):
        self.updateWinStatus()
        if lastSubpos == -1:    #special case; this is for the start of the game to allow any move to be made
            if pos in range(9) and subpos in range(9):
                if self.getSubboard(pos).checkLegal(subpos):
                    return True
        if pos in range(9) and lastSubpos in range(9) and subpos in range(9):   #checks to see if all positions are in between 0-8
            if self.getSubboard(lastSubpos).getWinStatus() == EMPTY:    #checks to see if the last move pointed to a board that isn't won
                if lastSubpos == pos:   #checks to make sure that, if above is the case, lastSubpos and pos are the same (because they have to)
                    if self.getSubboard(pos).checkLegal(subpos):    #checks to see if the move is legal on the lower level (ttt object)
                        return True
            else:   #otherwise, there's the other case that you're allowed to move anywhere due to being sent to a won/drawn board
                if lastSubpos != pos:   #this has to be true because you can't mark in a won/drawn board
                    if self.getSubboard(pos).checkLegal(subpos):    #checks to see if the move is legal on the lower level (ttt object)
                        return True
        return False

    def reset(self):
        self.winStatus = EMPTY
        for i in range(9):
            self.getSubboard(i).reset()
