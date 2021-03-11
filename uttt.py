import ttt
from consts import X, O, EMPTY, DRAW
class uttt(ttt.ttt):
    def __init__(self):
        self.bigBoard = []
        self.bigWin = EMPTY
        for i in range(9):
            self.bigBoard.append(ttt.ttt())

    def getPos(self, pos, subPos):  #gets the mark at [pos, subPos]
        return self.bigBoard[pos].getPos(subPos)

    def setPos(self, mark, pos, subPos):#sets the pos at [pos, subPos] to mark
        if (mark != X or mark != O) and self.bigBoard[pos].getPos(subPos) != EMPTY:
            print("Illegal mark entry")
            return -2
        else:
            self.bigBoard[pos].setPos(subPos, mark)
        if(self.bigBoard[subPos].getWin() != EMPTY):
            return -1
        else:
            return subPos
        
    def getWin(self):
        return self.bigWin;

    def getSubboard(self, pos):
        return self.bigBoard[pos]
    
    def print(self):        #prints the board in a readable format
        for w in range(3):  #"It just works" - Todd Howard
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        mark = ""
                        if self.getPos(y + (w*3), z + (x*3)) == X:
                            mark = "X"
                        elif self.getPos(y + (w*3), z + (x*3)) == O:
                            mark = "O"
                        else:
                            mark = " " #could change to a # easily
                        print(mark,end="")
                        if not y == z == 2:
                            print("|",end="")
                if x != 2:
                    print("\n-+-+-|-+-+-|-+-+-")
            if w != 2:
                print("\n-----+-----+-----")
        print()

    def checkWin(self):     #updates the win condition of the big board
        w = []              #all of the smaller board wins
        for i in self.bigBoard:
            w.append(i.getWin())
        if EMPTY not in w:
            self.bigWin = DRAW
        rows = [[w[0],w[1],w[2]],[w[3],w[4],w[5]],[w[6],w[7],w[8]]]
        columns = [[w[0],w[3],w[6]],[w[1],w[4],w[7]],[w[2],w[5],w[8]]]
        diags = [[w[0],w[4],w[8]],[w[2],w[4],w[6]]]
        for i in range(3):
            if rows[i].count(X) == 3:
                self.bigWin = X
            elif rows[i].count(O) == 3:
                self.bigWin = O
            elif columns[i].count(X) == 3:
                self.bigWin = X
            elif columns[i].count(O) == 3:
                self.bigWin = O  
        for i in range(2):
            if diags[i].count(X) == 3:
                self.bigWin = X
            elif diags[i].count(O) == 3:
                self.bigWin = O

    def reset(self):    #resets the entire board
        for i in range(len(self.bigBoard)):
            self.bigBoard[i].reset()
        self.bigWin = EMPTY
