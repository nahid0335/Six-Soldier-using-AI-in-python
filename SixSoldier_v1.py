#---------------Library-------------
from random import randrange
import time
import copy





#---------------initialization-------------
board = [['0','1', '2', '3'],
         ['1','C', 'C', 'C'],
         ['2','C', 'C', 'C'], 
         ['3','.', '.', '.'], 
         ['4','P', 'P', 'P'],
         ['5','P', 'P', 'P']]

tempboard = copy.deepcopy(board)                                                #for check move ,copy of mainboard

movesetX = [-1,0,1,0]                                                           #only can move left , right, up and down 
movesetY = [0,-1,0,1]

dic = {}                                                                        #contain all available move with cost
pointdic = {}                                                                   #intermediate move with cost
gameEnd = True                                                                  #bool for continue the game ->true = continue, false = stop



    


#---------------Board draw-------------
def draw():
    for x in board:
        for y in x:
            print(y, end=" ")

        print("\n")


draw()
time.sleep(2)








#---------------AI next move calculation-------------
def getMovePoints(x, y):
    pointdic.clear()
    for i in range(4):
        xi = movesetX[i]
        yi = movesetY[i]
        if (1 <= (x +xi) <= 5) and (1 <= (y + yi) <= 3):                        #check valid move
            if board[x + xi][y + yi] == '.':                                    #if find any open space
                pointdic[(x+xi, y+yi)] = 2                                      #enter the cost
                tempboard[x][y]='.'                                             #temporary change the board
                tempboard[x+xi][y+yi]='C'                                       #to see if it is safe to move
                
                if isSafe(x + xi, y + yi) == -1:
                    pointdic[(x + xi, y + yi)] = 1                              #if not safe reduce the cost
                tempboard[x][y]='C'                                             #fix the tempboard like previous
                tempboard[x+xi][y+yi]='.'

            elif board[x + xi][y + yi] == 'C':                                  #if find soldier of com can't move
                pointdic[(x + xi, y + yi)] = -1
                
            elif board[x + xi][y + yi] == 'P':                                  #if find any player soldier next
                if (1 <= x + 2*xi <= 5) and (1 <= y + 2*yi <= 3):               #check if after that solder 
                    if board[x + 2 * xi][y + 2 * yi] == '.':                    #there is any empty space
                        pointdic[(x + 2*xi, y + 2*yi)] = 7
                        tempboard[x][y]='.'
                        tempboard[x+xi][y+yi]='.'
                        tempboard[x + 2 * xi][y + 2 * yi]='C'
                        #print(x, y, xi, yi, x+2*xi, y + 2*yi)
                        
                        if isSafe(x + 2 * xi, y + 2 * yi) == -1:                #if empty space has any nearby soldier
                            pointdic[(x + 2 * xi, y + 2 * yi)] = 5              #reduce the cost 
                        tempboard[x][y]='C'
                        tempboard[x+xi][y+yi]='P'
                        tempboard[x + 2 * xi][y + 2 * yi]='.'
                    else:
                        pointdic[(x + xi, y + yi)] = -1
                if (1 <= x - xi <= 5) and (1 <= y - yi <= 3):                   #if com soldier can be killed
                    if board[x - xi][y - yi] == '.':                            #use cost to get that possibility
                        pointdic[(x -xi, y -yi)] = 3
                        #print(x, y, xi, yi, x+2*xi, y + 2*yi)
                        tempboard[x][y]='.'
                        tempboard[x-xi][y-yi]='C'
                        
                        if isSafe(x - xi, y - yi) == -1:
                            pointdic[(x - xi, y - yi)] = 1
                        tempboard[x][y]='C'
                        tempboard[x-xi][y-yi]='.'
                    else:
                        pointdic[(x + xi, y + yi)] = -1
                else:
                    pointdic[(x + xi, y + yi)] = -1
           # print("x = "+str(x)+",y = "+str(y)+", xi = "+str(xi)+", yi = "+str(yi)+", pd = "+str(pointdic[(x + xi, y + yi)])+" ")

    #print(pointdic)
    #dic[(x, y)] = pointdic
    dic[(x,y)] =copy.deepcopy(pointdic)
    
    
    
    



#---------------AI move prediction-------------
def minmax():
    dic.clear()
    maxdic = {}
    global gameEnd
    
    comSoldier = sum(row.count('C') for row in board)                           #count the com soldier
    pSoldier = sum(row.count('P') for row in board)                             #count the player soldier
    if comSoldier == 0 :
        print("Congratulation !! you win the game..")
        gameEnd = False
        return [(-1,-1),(-1,-1)]                                                #if anyone win end the game
    elif pSoldier == 0 :                                                        #by making boolean gameEnd = false
        print("Alas !! You have been DEFEATED ..")                              #and returning envalid position
        gameEnd = False                                                         #(X1,Y1)=(-1,-1) (X2,Y2)=(-1,-1)
        return [(-1,-1),(-1,-1)]

    for i in range(len(board)):
        for j in range(len(board[i])):                                          #loop the board and find com
            if board[i][j] == 'C':                                              #soldier to get it's available
                getMovePoints(i, j)                                             #move

    for item in dic:
        val = sorted(dic[item].items(), key=lambda kv: kv[1], reverse=True)     #sort the dictionary
        maxdic.update({item: {val[0][0]: val[0][1]}})                           #get the maximum value at 
                                                                                #first position

    maximum = -100

    cur = None
    dest = None

    for item in maxdic:
        temp = maxdic[item]                                                     #update the max value 
        for item2 in temp:                                                      #get the current position to
            if temp[item2] > maximum:                                           #destination positon of max value
                cur = item
                dest = item2
                maximum = temp[item2]

    #print(maxdic)

    return [cur, dest]



            



#---------------valid move check-------------
def isValid(x2, y2):
    if (1<=x2<=5) and (1<=y2<=3):
        if board[x2][y2] == '.':
            return 1
        else:
            return -1
    else:
        return -1
    
    
    
    


#---------------valid soldier check-------------
def selectValid(x1, y1):
    if (1<=x1<=5) and (1<=y1<=3):
        if board[x1][y1] == 'P':
            return 1
        else:
            return -1
    else:
        return -1








#---------------position safe check-------------
def isSafe(x, y):                                                               #check if any move is safe to place
    for i in range(4):
        xi = movesetX[i]                                                        #get the 4 move
        yi = movesetY[i]
        if (1 <= x + xi <= 5) and (1 <= y + yi <= 3):                           #check valid position
                if tempboard[x + xi][y + yi] == 'P':                            #if there nearby any opponent
                    if (1 <= x - xi <= 5) and (1 <= y - yi <= 3):               #check behind position is valid
                        if tempboard[x - xi][y - yi] == 'C' or tempboard[x - xi][y - yi] == 'P':    #if any obstacle
                            return 1                                            #return safe
                        elif tempboard[x - xi][y - yi] == '.':                  #if no obstacle
                            return -1                                           #return unsafe
            
    return 1                        









#---------------initial move start-------------
#randomly select player to go first
    
print("Start the game..")
print()
print()
print("Tossing ..")
time.sleep(1)
print()
toss = randrange(1,11)                                                          #decide who will go first
#print(toss)
if(toss//2):
    
    #Ai move
    print("Computer win the toss , get First move..")
    print()
    time.sleep(1)
    
    print("Computer's turn -")
    co_ordinate = minmax()                                                      #calling the Ai function minmax()
    print("Computer move to : ", co_ordinate)                                   #getting the move
    print()

    x1 = co_ordinate[0][0]
    x2 = co_ordinate[1][0]
    y1 = co_ordinate[0][1]
    y2 = co_ordinate[1][1]
    
    #update the board

    if (abs(x1 - x2) == 1 or abs(x1 - x2) == 0) and (abs(y2 - y1) == 1 or abs(y2 - y1) == 0):
        board[x1][y1] = '.'
        board[x2][y2] = 'C'
        
        tempboard[x1][y1] = '.'
        tempboard[x2][y2] = 'C'

    elif (abs(x1 - x2) == 2 or abs(x1 - x2) == 0) and (abs(y2 - y1) == 2 or abs(y2 - y1) == 0):
        if board[(x1 + x2) // 2][(y1 + y2) // 2] == 'P':
            board[(x1 + x2) // 2][(y1 + y2) // 2] = '.'
            board[x1][y1] = '.'
            board[x2][y2] = 'C'
            
            tempboard[(x1 + x2) // 2][(y1 + y2) // 2] = '.'
            tempboard[x1][y1] = '.'
            tempboard[x2][y2] = 'C'

    draw()
    time.sleep(2)
    
else:
    print("Player win the toss , get First move..")
    time.sleep(1)







#---------------loop the game-------------
while gameEnd :
    
    print("Player's turn -")

    x1 = int(input("Select SOLDIER position x : "))
    y1 = int(input("Select SOLDIER position y : "))
    
    if selectValid(x1, y1) == -1:
        print("Envalid position ,Can't select this SOLDIER !!")
        continue

    x2 = int(input("SOLDIER to put in position x : "))
    y2 = int(input("SOLDIER to put in position y : "))

    if isValid(x2, y2) == -1:
        print("Envalid position ,Can't place the SOLDIER here !!")
        continue
    

    #update the board after player turn
    elif (abs(x1 - x2) == 1 or abs(x1 - x2) == 0) and (abs(y2 - y1) == 1 or abs(y2 - y1) == 0):
        board[x1][y1] = '.'
        board[x2][y2] = 'P'
        
        tempboard[x1][y1] = '.'
        tempboard[x2][y2] = 'P'

    elif (abs(x1 - x2) == 2 or abs(x1 - x2) == 0) and (abs(y2 - y1) == 2 or abs(y2 - y1) == 0):
        if board[(x1 + x2) // 2][(y1 + y2) // 2] == 'C':
            board[(x1 + x2) // 2][(y1 + y2) // 2] = '.'
            board[x1][y1] = '.'
            board[x2][y2] = 'P'
            
            tempboard[(x1 + x2) // 2][(y1 + y2) // 2] = '.'
            tempboard[x1][y1] = '.'
            tempboard[x2][y2] = 'P'

    draw()
    time.sleep(2)
    
    
    
    # AI move
    co_ordinate = minmax()
    if (co_ordinate[0][0]==-1) and (co_ordinate[0][1]==-1):
        continue
    
    print("Computer's turn -")
    
    
    print("Computer move to : ", co_ordinate)
    print()

    x1 = co_ordinate[0][0]
    x2 = co_ordinate[1][0]
    y1 = co_ordinate[0][1]
    y2 = co_ordinate[1][1]
    
    
    #update the board after com's turn

    if (abs(x1 - x2) == 1 or abs(x1 - x2) == 0) and (abs(y2 - y1) == 1 or abs(y2 - y1) == 0):
        board[x1][y1] = '.'
        board[x2][y2] = 'C'
        
        tempboard[x1][y1] = '.'
        tempboard[x2][y2] = 'C'

    elif (abs(x1 - x2) == 2 or abs(x1 - x2) == 0) and (abs(y2 - y1) == 2 or abs(y2 - y1) == 0):
        if board[(x1 + x2) // 2][(y1 + y2) // 2] == 'P':
            board[(x1 + x2) // 2][(y1 + y2) // 2] = '.'
            board[x1][y1] = '.'
            board[x2][y2] = 'C'
            
            tempboard[(x1 + x2) // 2][(y1 + y2) // 2] = '.'
            tempboard[x1][y1] = '.'
            tempboard[x2][y2] = 'C'

    draw()
    time.sleep(2)
