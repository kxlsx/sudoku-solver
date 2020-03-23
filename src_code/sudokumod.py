import sudokuboards
from copy import deepcopy

#char meaning the spot is empty
emp = sudokuboards.emp

#the constMarker is for constant values that CANNOT be changed by the algorithm
constMarker = '$'

#main sudoku-solver 
def sudoku_solve(board, copyBoard=True):

    if copyBoard:
        brd = deepcopy(board)
    else:
        brd = board

    #general checks if the board is valid for sudoku
    if len(brd) % 3 != 0 or len(brd) == 0:
        raise Exception("Board's size must be a positive multiple of 3")
    elif not(is_board_square(brd)):
        raise Exception("Board's row count and row length must be uniform")

    brd = mark_constants(brd)

    maxBoardIndex = len(brd) - 1
    maxBoardRange = len(brd) + 1

    possibleNums = tuple([str(i)
                     for i in range(1, maxBoardRange)])

    rowI = elementI = 0
    while True:
        
        horizontals = get_horizontal_nums(brd)
        verticals = get_vertical_nums(brd)
        squares = get_nums_in_squares(brd)

        #if it isn't taken by a constant num
        if brd[rowI][elementI] == emp or brd[rowI][elementI] in possibleNums:

            #if it had already reached 9 before and it cannot increment further
            if brd[rowI][elementI] == possibleNums[-1]:
                
                #reset the spot
                brd[rowI][elementI] = emp

                #backtrack to the last available spot
                newCoords = get_bactrack_coordinates(rowI, elementI, brd)
                if newCoords == None:

                    #the board cannot be solved
                    return

                rowI     = newCoords[0]
                elementI = newCoords[1]

            else:
                
                #go through all nums <the current one + 1; 9>
                for num in range(get_current_num_incremented(rowI, elementI, brd), maxBoardRange):
                    
                    #if the num isn't already on the horizontal or vertical line or in a square
                    if ((str(num) not in horizontals[rowI])
                    and (str(num) not in verticals[elementI])
                    and (str(num) not in squares[get_square_num(rowI, elementI, len(brd))])):

                        #set the first available num on the spot
                        brd[rowI][elementI] = str(num)

                        #go forward a spot
                        newCoords = get_forward_coordinates(rowI, elementI, maxBoardIndex)
                        if newCoords == None:

                            #final return (with the markers deleted for good measure)
                            return remove_constant_marks(brd)

                        rowI     = newCoords[0]
                        elementI = newCoords[1]

                        break
                    
                    #if none of the spots are available 
                    elif (num == maxBoardRange - 1):

                        #reset the spot
                        brd[rowI][elementI] = emp

                        #backtrack to the last available spot
                        newCoords = get_bactrack_coordinates(rowI, elementI, brd)
                        if newCoords == None:

                            #the board cannot be solved
                            return

                        rowI     = newCoords[0]
                        elementI = newCoords[1]

        #if it's a constant num
        else:
            
            #go forward a spot
            newCoords = get_forward_coordinates(rowI, elementI, maxBoardIndex)
            if newCoords == None:

                #final return (with the markers deleted for good measure)
                return remove_constant_marks(brd)

            rowI     = newCoords[0]
            elementI = newCoords[1]

#sudoku-solver but it yields the board every time it places or removes a num
def step_by_step_sudoku_solve(board, copyBoard=True):

    if copyBoard:
        brd = deepcopy(board)
    else:
        brd = board

    #general checks if the board is valid for sudoku
    if len(brd) % 3 != 0 or len(brd) == 0:
        raise Exception("Board's size must be a positive multiple of 3")
    elif not(is_board_square(brd)):
        raise Exception("Board's row count and row length must be uniform")

    brd = mark_constants(brd)

    maxBoardIndex = len(brd) - 1
    maxBoardRange = len(brd) + 1

    possibleNums = tuple([str(i)
                     for i in range(1, maxBoardRange)])

    rowI = elementI = 0
    while True:
        
        horizontals = get_horizontal_nums(brd)
        verticals = get_vertical_nums(brd)
        squares = get_nums_in_squares(brd)

        #if it isn't taken by a constant num
        if brd[rowI][elementI] == emp or brd[rowI][elementI] in possibleNums:

            #if it had already reached 9 before and it cannot increment further
            if brd[rowI][elementI] == possibleNums[-1]:
                
                #reset the spot
                brd[rowI][elementI] = emp
                yield (remove_constant_marks(brd), False)

                #backtrack to the last available spot
                newCoords = get_bactrack_coordinates(rowI, elementI, brd)
                if newCoords == None:

                    #the board cannot be solved
                    yield None
                    return

                rowI     = newCoords[0]
                elementI = newCoords[1]

            else:
                
                #go through all nums <the current one + 1; 9>
                for num in range(get_current_num_incremented(rowI, elementI, brd), maxBoardRange):
                    
                    #if the num isn't already on the horizontal or vertical line or in a square
                    if ((str(num) not in horizontals[rowI])
                    and (str(num) not in verticals[elementI])
                    and (str(num) not in squares[get_square_num(rowI, elementI, len(brd))])):

                        #set the first available num on the spot
                        brd[rowI][elementI] = str(num)
                        yield (remove_constant_marks(brd), True)

                        #go forward a spot
                        newCoords = get_forward_coordinates(rowI, elementI, maxBoardIndex)
                        if newCoords == None:

                            #board solved
                            return

                        rowI     = newCoords[0]
                        elementI = newCoords[1]

                        break
                    
                    #if none of the spots are available 
                    elif (num == maxBoardRange - 1):

                        #reset the spot
                        brd[rowI][elementI] = emp
                        yield (remove_constant_marks(brd), False)

                        #backtrack to the last available spot
                        newCoords = get_bactrack_coordinates(rowI, elementI, brd)
                        if newCoords == None:

                            #the board cannot be solved
                            return

                        rowI     = newCoords[0]
                        elementI = newCoords[1]

        #if it's a constant num
        else:
            
            #go forward a spot
            newCoords = get_forward_coordinates(rowI, elementI, maxBoardIndex)
            if newCoords == None:

                #board solved
                yield (remove_constant_marks(brd), True)
                return

            rowI     = newCoords[0]
            elementI = newCoords[1]

#prints the board to the console
def print_board(*boards):

    if boards == None:
        print('No Solution')

    i = 0
    for board in boards:

        if i != 0:
            print()
        
        if board == None:
            return None

        for row in board:
            for element in row:
                if not(element):
                    print(emp, end='')
                print(element.replace(constMarker,'') + '  ', end='')
            print()
            
        i+=1

#prints every step (board) of the algorithm solving the board
def print_solving_step_by_step(board):

    print_board(board)
    print('Going forward...')

    solveStepByStep = step_by_step_sudoku_solve(board)

    while True:
        try:
            step  = next(solveStepByStep)
        except StopIteration:
            print('Done!')
            break
        else:
            try:
                print_board(step[0])
            except TypeError:
                print('No solution!')
                break
            else:
                if step[1]:
                    print('Going forward...')
                else:
                    print('Going back...')
                
                print()


#returns a tuple of the next coordinates on the board (0 = rowI, 1 = elementI)
def get_forward_coordinates(rowI, elementI, maxBoardIndex):

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
def get_bactrack_coordinates(rowI, elementI, board):

    maxBoardIndex = len(board) - 1

    #go back a spot (if it's the first one, go up a row)
    elementI -= 1
    if elementI < 0:
        rowI -= 1

        #if it tried to backtrack from the first spot
        if rowI < 0:
            return

        #it goes to the last spot of the previous row (it moves through the board like a snake)
        else:
            elementI = maxBoardIndex
                                               
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
                elementI = maxBoardIndex
    
    return (rowI, elementI)


#it's to set the lower bound to check for nums
def get_current_num_incremented(rowI, elementI, board):

    if board[rowI][elementI] == emp:

        return 1

    elif board[rowI][elementI] == str(len(board)):

        return int(board[rowI][elementI])

    else:

        return int(board[rowI][elementI]) + 1

#returns the square's index, in which are the given coordinates 
#squares are marked vertically (left corner square is index 0, and the one below it is index 1)
def get_square_num(rowI, elementI, boardLen):

    squareSize = int(boardLen / 3)
    squareMaxYs = tuple(filter(lambda x: x % 3 == 0, range(3, boardLen + 1)))
    squareMaxXs = tuple(filter(lambda x: x % squareSize == 0, range(squareSize, boardLen + 1)))

    base = 0
    for maxY in squareMaxYs:

        if rowI < maxY:
            
            mod = 0
            for maxX in squareMaxXs:

                if elementI < maxX:
                    return base + mod

                mod += squareSize

        base+=1

#returns a list of nums in corresponding horizontal lines 
def get_horizontal_nums(board):
    
    #pretty much copies the board without blank spaces and const markers
    horizontals = [{element.replace(constMarker, '')
                    for element in row
                    if element != emp}
                   for row in board]

    return horizontals

#returns a list of nums in corresponding vertical lines 
def get_vertical_nums(board):

    #empty list the same size as the board but filled with empty lists|
    verticals = [set()
                 for row in board]

    for elNum in range(len(board)):
        for rowNum in range(len(board)):
            #adds only nums to save time
            if board[rowNum][elNum] != emp:
                verticals[elNum].add(board[rowNum][elNum].replace(constMarker, ''))

    return verticals

#returns a list of nums in corresponding(check explanation above get_square_num) squares (3x3) 
def get_nums_in_squares(board):

    squareSize = int(len(board) / 3)
    squareY = 3
    squareX = squareSize

    #empty list the same size as the board but filled with empty sets
    squares = [set()
               for row in board]

    for squareNum in range(len(board)):
        for y in range(squareY - 3, squareY):
            for x in range(squareX - squareSize, squareX):
                #adds only nums to save time
                if board[x][y] != emp:
                    squares[squareNum].add(board[x][y].replace(constMarker, ''))

        squareX += squareSize
        if squareX > len(board):
            squareX = int(len(board)/3)
            squareY += 3

    return squares


#checks whether the board's length is the same as each row's length 
def is_board_square(board):

    try:

        for row in board:
           if len(board) != len(row):
                return False

        return True

    except:
        raise Exception('Board must be two-dimensional')


#returns a board with the nums coming pre-set marked with constMarker
def mark_constants(board):
    
    for row in board:
        for element in row:
            if element != emp:
                board[board.index(row)][row.index(element)] += constMarker

    return board

#returns a board with the constMarkers removed if i'll ever need it
def remove_constant_marks(board):

    for row in board:
        for element in row:
            if element != emp:
                board[board.index(row)][row.index(element)] = board[board.index(row)][row.index(element)].replace(constMarker, '')

    return board

print_solving_step_by_step(sudokuboards.generate_board_from_api(difficulty='easy'))