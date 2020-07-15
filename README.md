# sudoku-solver
A simple visualisation of solving sudoku boards with a *backtracking algorithm*.
Sudoku boards are generated using [**suGOku API**](https://github.com/berto/sugoku).
GUI made in [**Pygame**](https://github.com/pygame/pygame).

## What does it do?

 - You can generate a random board and see it solved visually in the GUI
 - The actual algorithm is situated in the [/src/sudoku](https://github.com/k-xlsx/sudoku-solver/tree/master/src/sudoku) package in either the [sudoku module](https://github.com/k-xlsx/sudoku-solver/blob/master/src/sudoku/sudoku.py) or the [sudokuboard module](https://github.com/k-xlsx/sudoku-solver/blob/master/src/sudoku/sudokuboard.py), the latter being an OOP approach which I actually recommend over the functional version 
 - That's it actually, but I may some day add custom sudoku boards and solving them "by hand".
## GUI controls
|Key| Function |
|--|--|
| r | Display random board |
| esc | Reset the current board |
| space | Show solving the board |

## Files

	/assets
		config.json						// config file for colours and such
		icon.ico
	/src
		/sudoku
			__init__.py
			requestsJson.py
			sudoku.py					// module containing methods solving sudoku
			sudokuboard.py				// module containing the SudokuBoard object
			sudokuexceptions.py
			sudokusamples.py			// module containing some sample sudoku boards
		grid.py
		main.pyw						// module to run GUI
		options.py
		screens.py
		sudokugrid.py
## Cool SudokuBoard object methods
See their individual docstrings for explanations.
 - [solve](https://github.com/k-xlsx/sudoku-solver/blob/master/src/sudoku/sudokuboard.py#L150)
 - [gen_solving_step_by_step](https://github.com/k-xlsx/sudoku-solver/blob/master/src/sudoku/sudokuboard.py#L262) 
 - [print_board](https://github.com/k-xlsx/sudoku-solver/blob/master/src/sudoku/sudokuboard.py#L383)
 - [print_solving_step_by_step](https://github.com/k-xlsx/sudoku-solver/blob/master/src/sudoku/sudokuboard.py#L390)
 - [reset_board](https://github.com/k-xlsx/sudoku-solver/blob/master/src/sudoku/sudokuboard.py#L426)
