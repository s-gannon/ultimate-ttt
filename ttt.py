#consts to stand in for X and O (so I don't have to use chars or strings)
from consts import X, O, EMPTY, DRAW
class ttt():
    def __init__(self):
        self.board = [EMPTY]*9  #inits the board with 9 positions marked as empty
        self.win = EMPTY        #inits win as being EMPTY as X or O hasn't won and no draw

    def getPos(self, pos):  #gets the value at the specified position
        return self.board[pos]

    def setPos(self, pos, mark):        #sets the mark at that position
        if (mark != X or mark != O) and self.board[pos] != EMPTY:
            print("Illegal mark entry") #error if not X, O, or if pos is not empty
        else:
            self.board[pos] = mark
            self.checkWin()
        
    def getWin(self):       #returns the win status of the board
        return self.win
    
    def print(self):
        pb = []                 #'printable board'
        for p in self.board:    #convert board values (ints) to strings
            if p == X:
                pb.append("X")
            elif p == O:
                pb.append("O")
            else:
                pb.append(" ")
        print(pb[0] + "|" + pb[1] + "|" + pb[2])
        print("-+-+-")
        print(pb[3] + "|" + pb[4] + "|" + pb[5])
        print("-+-+-")
        print(pb[6] + "|" + pb[7] + "|" + pb[8])

    def checkWin(self):     #checks to see if the board has been won
        if EMPTY not in self.board:
            self.win = DRAW
        b = self.board
        rows = [[b[0],b[1],b[2]],[b[3],b[4],b[5]],[b[6],b[7],b[8]]]
        columns = [[b[0],b[3],b[6]],[b[1],b[4],b[7]],[b[2],b[5],b[8]]]
        diags = [[b[0],b[4],b[8]],[b[2],b[4],b[6]]]
        for i in range(3):
            if rows[i].count(X) == 3:
                self.win = X
            elif rows[i].count(O) == 3:
                self.win = O
            elif columns[i].count(X) == 3:
                self.win = X
            elif columns[i].count(O) == 3:
                self.win = O  
        for i in range(2):
            if diags[i].count(X) == 3:
                self.win = X
            elif diags[i].count(O) == 3:
                self.win = O
                
    def reset(self):
        for i in range(len(self.board)):
            self.board[i] = EMPTY
        self.win = EMPTY
