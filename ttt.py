from consts import X, O, EMPTY, DRAW    #consts to keep X, O, EMPTY, and DRAW the same across all files
class ttt():
    def __init__(self):
        self.board = [EMPTY]*9
        self.winStatus = EMPTY
#---------------Accessor methods---------------#
    #gets the win status of the game
    def getWinStatus(self):
        self.updateWinStatus()  #again, probably shouldn't put this here
        return self.winStatus
    #gets the mark at position 'pos'
    def getMarkAtPos(self, pos):
        return self.board[pos]
#---------------Mutator methods----------------#
    #changes the value on the board at position 'pos' to value 'mark'
    def makeMove(self, mark, pos):
        self.board[pos] = mark
    #updates the winStatus variable
    def updateWinStatus(self):
        b = self.board
        rows = [[b[0],b[1],b[2]],[b[3],b[4],b[5]],[b[6],b[7],b[8]]]
        cols = [[b[0],b[3],b[6]],[b[1],b[4],b[7]],[b[2],b[5],b[8]]]
        diag = [[b[0],b[4],b[8]],[b[2],b[4],b[6]]]
        if [X,X,X] in rows or [X,X,X] in cols or [X,X,X] in diag:
            self.winStatus = X
        elif [O,O,O] in rows or [O,O,O] in cols or [O,O,O] in diag: #if there's a line of 3 O's or X's, then that mark wins the game
            self.winStatus = O
        elif EMPTY not in b:  #if there are no more empty spaces in the board and there's still no win status
            self.winStatus = DRAW   #it's safe to assume that the board has been drawn
        else:
            self.winStatus = EMPTY
#----------------Other methods-----------------#
    #prints the board
    def print(self):
        b = self.board
        for i in range(3):
            print("{0}|{1}|{2}".format(b[3*i],b[3*i + 1],b[3*i + 2]))
            if i != 2:
                print("-+-+-")
    #checks to see if moving at position 'pos' is a legal move
    def checkLegal(self, pos):
        self.updateWinStatus()  #probably shouldn't put this here... oh well
        if pos in range(9): #if the position 'pos' is between 0-8
            if self.board[pos] == EMPTY:    #if there is an open space at that position
                if self.winStatus == EMPTY:     #if the game hasn't been won yet
                    return True                     #we are good to go
        return False    #else, it's not a legal move

    def reset(self):
        self.board = [EMPTY]*9
        self.winStatus = EMPTY
