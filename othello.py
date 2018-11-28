# Kiet Ho hoxxx433
# I understand this is a graded, individual examination that may not be
# discussed with anyone. I also understand that obtaining solutions or
# partial solutions from outside sources, or discussing
# any aspect of the examination with anyone will result in failing the course.
# I further certify that this program represents my own work and that none of
# it was obtained from any source other than material presented as part of the
# course.
import turtle
import random

def getValidMoves(board,color):
    # use dictionary for readable color
    dict = {"white" : 2, "black" : 1}
    valid = []
    for rows in board:
        for columns in board[rows]:
            if board[rows][columns] == 0:
                if checkValidMove(board,rows,columns,dict[color]):
                    valid.append([rows,columns])
                # finding valid moves from each box by checking for color match
    drawGrid(board)
    return valid

def checkValidMove(board,row,col,color):
    n = board[row][col]
    rowOp = [row-1, row+1, row]
    colOp = [col-1, col+1, col]
    valid = False
    # going through every surrounding box options
    for rows in rowOp:
        for cols in colOp:
            if rows >-1 and cols >-1 and rows <8 and cols <8:
                if valid == True:
                    return True
                else:
                    if board[rows][cols] == color:
                        return True
                    elif board[rows][cols] == 0:
                        valid = False
                    else:
                        # if surrounding box is of opposite color, keep checking in that direction
                        valid = checkFurther(board, row, rows, col, cols, color)

    return valid

def checkFurther(matrix, row, newRow, column, newCol, color):
    # checking in the relative direction of the neighboring box until find same color or blank
    # return false if out of bounds
    if newRow < 0 or newCol <0 or newRow >7 or newCol >7:
        return False
    else:
        # return true if found matching color
        if matrix[newRow][newCol] == color:
            return True
        else:
            # return false if found blank box
            if matrix[newRow][newCol] == 0:
                return False
            else:
                if newRow == row+1:
                    newNewRow = newRow+1
                elif newRow == row-1:
                    newNewRow = newRow-1
                else:
                    newNewRow = newRow
                if newCol == column +1:
                    newNewCol = newCol+1
                elif newCol == column -1:
                    newNewCol = newCol-1
                else:
                    newNewCol = newCol
                # yay recursion!
                return checkFurther(matrix, newRow, newNewRow, newCol, newNewCol, color)

def selectNextPlay(board):
    # find all valid moves for bot
    valid = getValidMoves(board, "black")
    if valid != []:
        # return random move from list
        move = random.sample(valid, 1)[0]
        return move
    else:
        # no available moves
        return None

def setBoard():
    # creating visual
    screen = turtle.getscreen()
    screen.setworldcoordinates(-1,-8,8,2)
    screen.tracer(0)
    turtle.left(90)
    turtle.speed(0)

def createMatrix():
    # create inital matrix
    row = 0
    colNum = 0
    grid = {}
    while row <8:
        column = {}
        colNum = 0
        while colNum<8:
            column[colNum] = 0
            colNum +=1
        grid[row] = column
        row +=1
    # add initial pieces
    updateBoard(grid,3,3,"white")
    updateBoard(grid,4,4,"white")
    updateBoard(grid,3,4,"black")
    updateBoard(grid,4,3,"black")

    return grid

def isValidMove(valid_list, move):
    # check for valid move in list
    if move in valid_list:
        return True
    else:
        return False

def drawGrid(grid):
    # drawing new grid
    turtle.penup()
    turtle.shapesize(3.2,2.8,3)
    for rows in grid:
        for columns in grid[rows]:
            turtle.goto(columns, -rows)
            if grid[rows][columns] == 1:
                # add square in background
                turtle.shape("square")
                turtle.color("light green")
                turtle.stamp()
                # add piece
                turtle.shape("circle")
                turtle.color("light grey")
                turtle.stamp()
            elif grid[rows][columns] == 2:
                turtle.shape("square")
                turtle.color("light green")
                turtle.stamp()
                turtle.shape("circle")
                turtle.color("black")
                turtle.stamp()
            else:
                turtle.shape("square")
                turtle.color("light green")
                turtle.stamp()
    turtle.update()

def updateBoard(board, row, column, color):
    # add new move into board
    dict = {"white" : 2, "black" : 1}
    board[row][column] = dict[color]
    # find pieces that needs to be flipped to opposite color
    to_flip = findMatch(board,row,column,dict[color])
    for el in to_flip:
        # flipping
        board[el[0]][el[1]] = dict[color]
    return board

def findMatch(board, row, col, color):
    # find matching pieces to be flipped, similar to finding valid
    rowOp = [row-1, row+1, row]
    colOp = [col-1, col+1, col]

    flip = []
    match = False
    for rows in rowOp:
        for cols in colOp:
            if rows >-1 and cols >-1 and rows <8 and cols <8:
                to_flip = []
                if board[rows][cols] == color:
                    match =  False
                elif board[rows][cols] == 0:
                    match = False
                else:
                    # creating list of flippable pieces
                    to_flip = matchFurther(board, row, rows, col, cols, color, to_flip)
                    if to_flip != None:
                        for el in to_flip:
                            flip.append(el)
    return flip

def matchFurther(matrix, row, newRow, column, newCol, color, flip):
    # similar to check further, returning list of flippable instead of boolean
    if newRow < 0 or newCol <0 or newRow >7 or newCol >7:
        return None
    else:
        if matrix[newRow][newCol] == color:
            # only return list of flippable if there is a matching color at the other end
            return flip
        else:
            if matrix[newRow][newCol] == 0:
                return
            else:
                # keep adding new options into flippable list
                flip.append([newRow,newCol])
                if newRow == row+1:
                    newNewRow = newRow+1
                elif newRow == row-1:
                    newNewRow = newRow-1
                else:
                    newNewRow = newRow
                if newCol == column +1:
                    newNewCol = newCol+1
                elif newCol == column -1:
                    newNewCol = newCol-1
                else:
                    newNewCol = newCol
                # this concept is becoming very handy
                return matchFurther(matrix, newRow, newNewRow, newCol, newNewCol, color, flip)

def setBorder():
    # creating outside numbers to aid users in picking boxes
    x = -1
    y = -1
    z = 0
    turtle.color("green")
    while x < 8:
        while y < 8:
            if x == -1:
                turtle.goto(x,-y)
                if y !=-1:
                    turtle.write(y)
            if y == -1:
                while z <8:
                    turtle.goto(z,-y)
                    turtle.write(z)
                    z+=1
            y +=1
        x +=1
    turtle.update()

def comPlay(matrix):
    # calculating plays for bot
    # picking a random play from list of valid plays for bot
    com_play = selectNextPlay(matrix)
    if com_play != None:
        updateBoard(matrix,com_play[0],com_play[1],"black")
        drawGrid(matrix)
        return False
    else:
        print("No valid moves")
        return True

def scoreGame(matrix):
    # handling game ending
    # get frequencies of all pieces including blank
    freq = getFreq(matrix)
    print("Game Over! The Score is: ")

    print("Black: ", freq[2])
    print("White: ", freq[1])

    if freq[2] > freq[1]:
        print("Black wins!")
    elif freq[2] < freq[1]:
        print("White wins!")
    else:
        print("It's a tie!")

def getFreq(matrix):
    # getting frequencies of all pieces
    freq = {}
    for rows in matrix.keys():
        for cols in matrix[rows]:
            if matrix[rows][cols] not in freq.keys():
                freq[matrix[rows][cols]] = 1
            else:
                freq[matrix[rows][cols]] +=1
    # handling this here instead of presetting at instantiation because makes iteration logic above easier
    if 2 not in freq.keys():
        freq[2] = 0
    if 1 not in freq.keys():
        freq[1] = 0
    if 0 not in freq.keys():
        freq[0] = 0
    return freq

def main():
    # while loop conditions
    done = False
    valid_play = False
    # creating intial board
    matrix = createMatrix()
    setBoard()
    drawGrid(matrix)
    setBorder()

    # get user's inital input
    play = turtle.textinput("Pick a play: ","Enter row, column")
    while done == False:

        # more while loop conditions
        valid_play = False
        no_valid_play_com = False
        no_valid_play_human = False
        # get player's valid moves
        valid_moves = getValidMoves(matrix, "white")
        # putting input into usable format
        if valid_moves != []:
            list = play.split(',')
            play_list = []
            for items in list:
                play_list.append(int(items))
            # if the move is valid then apply changes
            if isValidMove(valid_moves, play_list):
                updateBoard(matrix,play_list[0],play_list[1],"white")
                drawGrid(matrix)
                valid_play = True
                no_valid_play_human = False
                no_valid_play_com = comPlay(matrix)
                # checking if there are any blank spaces left to call game over
                if getFreq(matrix)[0] == 0:
                    done = True
        else:
            # double checking game ending condition and calling computer play
            no_valid_play_human = True
            no_valid_play_com = comPlay(matrix)
            if getFreq(matrix)[0] == 0:
                done = True
        # another check for game over condition
        if no_valid_play_com == True and no_valid_play_human == True:
            done  = True

        if done != True:
            # handling player input prompts
            if valid_play == True:
                play = turtle.textinput("Next Play: ","Enter row, column")
            else:
                play =  turtle.textinput("Invalid input: ","Enter valid row, column")

        # handling player quitting
        if play == None or play == '':
            print("Player has quit!")
            done  = True
    scoreGame(matrix)

if __name__ == '__main__':
    main()
