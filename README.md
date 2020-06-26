# sudoku-solver
Simple sudoku solver in python using the <i>backtracking algorithm</i> (a bit modified).<br/>
GUI made in Pygame. (GUI shows a random board and solves it)</br></br>
<b>Controls</b><br/>
```
r -> display a random board
esc -> reset current board
space -> solve the board
```
<b>Files:</b></br>
<i><b>src:</b></i><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- run <b>main.pyw</b></br></br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i><b>sudoku:</b></i><br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>sudoku.py</b>    -> module containing methods to solve sudoku, print it to the console or generate it using this API: https://github.com/berto/sugoku<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>sudokuboard.py</b>  -> Module containing the class SudokuBoard used to store, solve or print the given board (board can be generated as well by passing 'r', 'rand' or 'random' as board while creating the object)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>sudokusamples.py</b> -> module containing a couple of example boards<br/>
