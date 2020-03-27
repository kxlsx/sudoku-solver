"""
Module containing some example sudoku boards 

    boards9 -- a tuple of 9 boards (9x9)
    boards12 -- a tuple of 2 boards (12x12)

    Index 0 of every tuple is an empty board
"""

#char meaning 'empty cell'
emp='0'

#9x9 boards
boards9=(    
            #0
            (
                [emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp],
            ),

            #1
            (
                [emp,emp,emp,'7','9',emp,emp,'5',emp],
                ['3','5','2',emp,emp,'8',emp,'4',emp],
                [emp,emp,emp,emp,emp,emp,emp,'8',emp],
                [emp,'1',emp,emp,'7',emp,emp,emp,'4'],
                ['6',emp,emp,'3',emp,'1',emp,emp,'8'],
                ['9',emp,emp,emp,'8',emp,emp,'1',emp],
                [emp,'2',emp,emp,emp,emp,emp,emp,emp],
                [emp,'4',emp,'5',emp,emp,'8','9','1'],
                [emp,'8',emp,emp,'3','7',emp,emp,emp]
            ),

            #2
            (
                [emp,emp,emp,emp,emp,'3',emp,'2','7'],
                [emp,emp,emp,emp,'6','7',emp,emp,emp],
                [emp,'9',emp,'5',emp,emp,emp,'8','3'],
                ['6',emp,'9','4','3',emp,emp,emp,emp],
                [emp,'5',emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,'2','5',emp],
                [emp,'8',emp,emp,'4',emp,emp,emp,emp],
                [emp,'3','7',emp,emp,'2',emp,'9',emp],
                ['9',emp,'2',emp,emp,emp,emp,'6',emp]
            ),

            #3
            (
                [emp,'5',emp,'8',emp,emp,emp,emp,'1'],
                [emp,emp,emp,emp,'2',emp,'3',emp,emp],
                ['2',emp,'9',emp,emp,emp,emp,'7',emp],
                [emp,'9','1',emp,emp,'7',emp,emp,emp],
                [emp,emp,emp,'2','1','6',emp,emp,emp],
                [emp,emp,emp,'9',emp,emp,'4','1',emp],
                [emp,'8',emp,emp,emp,emp,'2',emp,'5'],
                [emp,emp,'5',emp,'7',emp,emp,emp,emp],
                ['6',emp,emp,emp,emp,'3',emp,'9',emp]
            ),

            #4
            (
                [emp,emp,emp,emp,'6',emp,emp,emp,emp],
                [emp,'2',emp,'9',emp,'4',emp,'6',emp],
                ['4',emp,emp,emp,'7',emp,emp,emp,'9'],
                [emp,'3',emp,emp,emp,emp,emp,'9','2'],
                [emp,emp,'9',emp,'8',emp,'5',emp,emp],
                ['1',emp,emp,emp,emp,emp,emp,'3',emp],
                ['5',emp,emp,emp,emp,emp,emp,emp,'1'],
                [emp,'9',emp,'2',emp,'6',emp,'4',emp],
                [emp,emp,emp,emp,'5',emp,emp,emp,emp]
            ),
            
            #5
            (
                [emp,emp,emp,emp,emp,'6',emp,'7',emp],
                [emp,'7',emp,'9',emp,'4',emp,'3',emp],
                ['4',emp,emp,emp,emp,emp,emp,emp,'1'],
                ['3',emp,'6',emp,emp,emp,emp,emp,emp],
                [emp,emp,'2','8',emp,'1','9',emp,emp],
                [emp,emp,emp,emp,emp,emp,'1',emp,'5'],
                ['1',emp,emp,emp,emp,emp,emp,emp,'7'],
                [emp,'3',emp,'5',emp,'8',emp,'9',emp],
                [emp,'5',emp,'4',emp,emp,emp,emp,emp]
            ),

            #6
            (
                [emp,emp,emp,emp,'2','4','3',emp,'7'],
                ['9',emp,emp,emp,'6',emp,emp,emp,emp],
                ['7',emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,'5',emp,emp,'7','9','4'],
                [emp,'6','5',emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,'8',emp,'3',emp,emp,emp],
                [emp,'5','4',emp,emp,emp,emp,'6',emp],
                [emp,emp,emp,emp,emp,emp,emp,'5','9'],
                [emp,emp,'3','4',emp,'8',emp,emp,emp]
            ),

            #7
            (
                ['2',emp,emp,'6',emp,'7','5',emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,'9','6'],
                ['6',emp,'7',emp,emp,'1','3',emp,emp],
                [emp,'5',emp,'7','3','2',emp,emp,emp],
                [emp,'7',emp,emp,emp,emp,emp,'2',emp],
                [emp,emp,emp,'1','8','9',emp,'7',emp],
                [emp,emp,'3','5',emp,emp,'6',emp,'4'],
                ['8','4',emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,'5','2',emp,'6',emp,emp,'8']
            ),

            #8
            (
                ['7','8',emp,'4',emp,emp,'1','2',emp],
                ['6',emp,emp,emp,'7','5',emp,emp,'9'],
                [emp,emp,emp,'6',emp,'1',emp,'7','8'],
                [emp,emp,'7',emp,'4',emp,'2','6',emp],
                [emp,emp,'1',emp,'5',emp,'9','3',emp],
                ['9',emp,'4',emp,'6',emp,emp,emp,'5'],
                [emp,'7',emp,'3',emp,emp,emp,'1','2'],
                ['1','2',emp,emp,emp,'7','4',emp,emp],
                [emp,'4','9','2',emp,'6',emp,emp,emp]
            )
        )

#12x12 boards
boards12=(
            #0
            (
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp],
                [emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp,emp]
                
            ),

            #1
            (
                [emp,emp,emp,'12',emp,'2',emp,emp,emp,emp,'11',emp],
                [emp,emp,emp,'11','6',emp,emp,'4',emp,'2',emp,'7'],
                [emp,'9',emp,'10',emp,emp,'7',emp,emp,'5',emp,emp],
                ['9','10',emp,'3',emp,'4',emp,'5',emp,emp,'1',emp],
                [emp,'2','7',emp,'8',emp,'6','9',emp,emp,emp,'3'],
                [emp,emp,emp,'8',emp,emp,emp,emp,'5','11',emp,emp],
                [emp,emp,'1','4',emp,emp,emp,emp,'12',emp,emp,emp],
                ['5',emp,emp,emp,'4','12',emp,'6',emp,'7','8',emp],
                [emp,'12',emp,emp,'10',emp,'5',emp,'9',emp,'3','1'],
                [emp,emp,'8',emp,emp,'10',emp,emp,'1',emp,'4',emp],
                ['3',emp,'12',emp,'11',emp,emp,'7','6',emp,emp,emp],
                [emp,'4',emp,emp,emp,emp,'3',emp,'2',emp,emp,emp]
                
            ),
        )