import numpy as np
import random
class Env():
    def __init__(self, rows, cols, currX, currY,difficulty):
        self.totalMoves=0
        self.grid = np.full((rows,cols),-1)
        self.posX = currX
        self.posY = currY
        self.board = np.full((rows,cols),0)
        self.level = difficulty
        self.rows = rows
        self.cols = cols
        for i in range(self.rows):
            for j in range(self.cols):
                if random.uniform(0, 1) < self.level:
                    self.board[i][j] = 9
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 9:
                    count=0
                    n = self.rows
                    m = self.cols
                    if(i-1>=0 and j-1>=0 and self.board[i-1][j-1]==9):
                        count = count +1
                    if(i-1>=0 and self.board[i-1][j]==9):
                        count = count +1
                    if(i-1>=0 and j+1<m and self.board[i-1][j+1]==9):
                        count = count +1
                    if(j-1>=0 and self.board[i][j-1]==9):
                        count = count +1
                    if(j+1<m and self.board[i][j+1]==9):
                        count = count +1
                    if(i+1<n and j-1>=0 and self.board[i+1][j-1]==9):
                        count = count +1
                    if(i+1<n and self.board[i+1][j]==9):
                        count = count +1
                    if(i+1<n and j+1<m and self.board[i+1][j+1]==9):
                        count = count +1
                    self.board[i][j]=count

    def getStates(self):
        states = np.full((1,9),-2)

        tempX = self.posX-1
        tempY = self.posY-1
        itr=0;
        for i in range(3):
            for j in range(3):
                if(tempX+i < 0 or tempX+i>=self.rows or tempY+j<0 or tempY+j >= self.cols):
                    states[0][itr]= -2
                else:
                    states[0][itr]= self.grid[tempX][tempY]
                itr=itr+1
        return states

    def step(self,action):
        self.totalMoves = self.totalMoves +1
        self.makeMove(action)
        reward=0
        flag = False
        if(self.validMove()):
            if(self.grid[self.posX][self.posY]== -1):
                if(self.board[self.posX][self.posY]==9):
                    reward = 2
                else:
                    reward = 1
            else:
                reward = -0.5
            self.grid[self.posX][self.posY] =  self.board[self.posX][self.posY]
        else:
            reward = -1
            flag = True
        if self.totalMoves >= (self.rows * self.cols)/2:
            flag = True
        return self.getStates(), reward, flag

    def makeMove(self,action):
        if  (action ==0):
            self.posX= self.posX -1
            self.posY= self.posY -1
        elif(action ==1):
            self.posX= self.posX -1
        elif(action ==2):
            self.posX= self.posX -1
            self.posY= self.posY +1
        elif(action ==3):
            self.posY= self.posY -1
        elif(action ==4):
            self.posY= self.posY +1
        elif(action ==5):
            self.posX= self.posX +1
            self.posY= self.posY -1
        elif(action ==6):
            self.posX= self.posX +1
        elif(action ==7):
            self.posX= self.posX +1
            self.posY= self.posY +1

    def validMove(self):
        if(self.posX<0 or self.posX>=self.rows or self.posY<0 or self.posY>=self.cols):
            return False
        else:
            return True

    def reset(self):
        self.posX=0
        self.posY=0
        self.totalMoves=0
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j]=-1
        return self.getStates()

    def printGrid(self):
        print()
        for i in range(self.rows):
            for j in range(self.cols):
                if(self.grid[i][j] == -1):
                    print("\u058E ", end='')
                elif(self.grid[i][j] == 9):
                    print("\u00A4 ", end='')
                else:
                    print(self.grid[i][j],"", end='')
            print()

    def getTotalMoves(self):
        return self.totalMoves

    def getTotalMines(self):
        numMines=0;
        for i in range(self.rows):
            for j in range(self.cols):
                if(self.board[i][j] ==9):
                    numMines = numMines+1
        return numMines

    def getMinesDestroyed(self):
        minesDestroyed=0
        for i in range(self.rows):
            for j in range(self.cols):
                if(self.grid[i][j] ==9):
                    minesDestroyed = minesDestroyed +1
        return minesDestroyed
