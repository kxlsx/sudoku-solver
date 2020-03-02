import sudokuboards as sb
import performance_test as perf

#the constMarker is for constant values that CANNOT be changed by the algorithm
constMarker = '$'

#all nums the algorithm can use <1;9>
possibleNums = tuple([str(i)
                     for i in range(1,10)])


#main 
def sudokuSolve(board):

    board = markConstants(board)
    maxBoardIndex = len(board) - 1

    rowI = elementI = 0
    while True:
        
        horizontals = pullNumHorizontals(board)
        verticals = pullNumVerticals(board)
        squares = pullNumSquares(board)

        #if it isn't taken by a constant num
        if board[rowI][elementI] == sb.emp or board[rowI][elementI] in possibleNums:

            #if it had already reached 9 before and it cannot increment further
            if board[rowI][elementI] == '9':
                
                #reset the spot
                board[rowI][elementI] = sb.emp

                #backtrack to the last available spot
                newCoords = bactrackCoordinates(rowI,elementI,board)
                if newCoords == None:

                    #the board cannot be solved
                    return

                rowI     = newCoords[0]
                elementI = newCoords[1]

            else:
                
                #go through all nums <the current one + 1; 9>
                for num in range(currentNumIncremented(rowI, elementI, board), 10):
                    
                    #if the num isn't already on the horizontal or vertical line or in a square
                    if ((str(num) not in horizontals[rowI])
                    and (str(num) not in verticals[elementI])
                    and (str(num) not in squares[squareNum(rowI, elementI)])):

                        #set the first available num on the spot
                        board[rowI][elementI] = str(num)

                        #go forward a spot
                        newCoords = forwardCoordinates(rowI, elementI, maxBoardIndex)
                        if newCoords == None:

                            #final return (with the markers deleted for good measure)
                            return removeConstantMarks(board)

                        rowI     = newCoords[0]
                        elementI = newCoords[1]

                        break
                    
                    #if none of the spots are available 
                    elif (num == 9):

                        #reset the spot
                        board[rowI][elementI] = sb.emp

                        #backtrack to the last available spot
                        newCoords = bactrackCoordinates(rowI,elementI,board)
                        if newCoords == None:

                            #the board cannot be solved
                            return

                        rowI     = newCoords[0]
                        elementI = newCoords[1]

        #if it's a constant num
        else:
            
            #go forward a spot
            newCoords = forwardCoordinates(rowI, elementI, maxBoardIndex)
            if newCoords == None:

                #final return (with the markers deleted for good measure)
                return removeConstantMarks(board)

            rowI     = newCoords[0]
            elementI = newCoords[1]


#returns a tuple of the next coordinates on the board (0 = rowI, 1 = elementI)
def forwardCoordinates(rowI, elementI, maxBoardIndex):

    #go to the next spot (if it's the last one, go down a row)
    elementI += 1
    if elementI > maxBoardIndex:
        elementI = 0
        rowI += 1

        #if it tries to go past the last item on the board
        if rowI > maxBoardIndex:
            return 

    return (rowI, elementI)

#returns a tuple of the last, previous, available coordinates (0 = rowI, 1 = elementI)
def bactrackCoordinates(rowI, elementI, board):

    #go back a spot (if it's the first one, go up a row)
    elementI -= 1
    if elementI < 0:
        rowI -= 1

        #if it tried to backtrack from the first spot
        if rowI < 0:
            return

        #it goes to the last spot of the previous row (it moves through the board like a snake)
        else:
            elementI = 8
                                               
    #while the current element it's checking is a constant
    #DOESN'T WORK PROPERLY i.e. doesn't work at all
    #UPDATE: i think it does now
    while '$' in board[rowI][elementI]:

        elementI -= 1
        if elementI < 0:
            rowI -= 1

            #if it tried to backtrack from the first spot
            if rowI < 0:
                return

            #it goes to the last spot of the previous row (it moves through the board like a snake)
            else:
                elementI = 8
    
    return (rowI, elementI)


#it's to set the lower bound to check for nums
def currentNumIncremented(rowI, elementI, board):

    if board[rowI][elementI] == sb.emp:

        return 1

    elif board[rowI][elementI] == '9':

        return int(board[rowI][elementI])

    else:

        return int(board[rowI][elementI]) + 1

#returns the square's, in which are the given coordinates, number (currently works only with board 9x9)
def squareNum(rowI, elementI):

    if rowI < 3:

        if elementI < 3:
            return 0

        elif elementI < 6:
            return 3

        elif elementI < 9:
            return 6

    elif rowI < 6:

        if elementI < 3:
            return 1

        elif elementI < 6:
            return 4

        elif elementI < 9:
            return 7

    elif rowI < 9:

        if elementI < 3:
            return 2

        elif elementI < 6:
            return 5

        elif elementI < 9:
            return 8


#returns all nums in corresponding horizontal lines 
def pullNumHorizontals(board):
    
    #pretty much copies the board without blank spaces and const markers
    horizontals = [{element.replace(constMarker, '')
                    for element in row
                    if element != sb.emp}
                   for row in board]

    return horizontals

#returns all nums in corresponding vertical lines 
def pullNumVerticals(board):

    #empty list the same size as the board but filled with empty lists|
    verticals = [set()
                 for row in board]

    for elNum in range(len(board)):
        for rowNum in range(len(board)):
            #adds only nums to save time
            if board[rowNum][elNum] != sb.emp:
                verticals[elNum].add(board[rowNum][elNum].replace(constMarker, ''))

    return verticals

#returns all nums in corresponding squares (3x3) 
def pullNumSquares(board):

    squareX = squareY = 3

    #empty list the same size as the board but filled with empty sets
    squares = [set()
               for row in board]

    for squareNum in range(len(board)):
        for y in range(squareY - 3, squareY):
            for x in range(squareX - 3, squareX):
                #adds only nums to save time
                if board[x][y] != sb.emp:
                    squares[squareNum].add(board[x][y].replace(constMarker, ''))

        squareX += 3
        if squareX > len(board):
            squareX = int(len(board)/3)
            squareY += 3

    return squares


#returns a board with the nums coming pre-set marked with constMarker
def markConstants(board):
    
    for row in board:
        for element in row:
            if element != sb.emp:
                board[board.index(row)][row.index(element)] += constMarker

    return board

#returns a board with the constMarkers removed if i'll ever need it
def removeConstantMarks(board):

    for row in board:
        for element in row:
            if element != sb.emp:
                board[board.index(row)][row.index(element)] = board[board.index(row)][row.index(element)].replace(constMarker, '')

    return board

def printBoard(*boards, empty_spot_char='0'):

    i = 0
    for board in boards:

        if i != 0:
            print()
        
        if board == None:
            return None

        for row in board:
            for element in row:
                if not(element):
                    print(empty_spot_char, end='')
                print(element.replace(constMarker,'') + '  ', end='')
            print()
            
        i+=1
