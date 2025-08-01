# Minesweeper_SAT

Minesweeper is a simple game where the player must clear a board while using hints to
determine where possible mines are. Numbered tiles will indicate how many mines surround it in
all 8 directions (up, down, left, right, and diagonals). The player wins if they clear out all spaces
without mines and the player loses if you click on a mine at any time. The player is also allowed
to flag tiles to mark them as mines.

In expert mode, which I built my algorithms around, the board is a 16x30 grid of tiles with
99 mines. Also, the first tile clicked and surrounding tiles will never be a mine, ensuring that the
player won’t get “trapped” off their first move.

I wanted to create an SAT solver that could solve Minesweeper, particularly expert
mode. In addition to this, I also wanted to create a guessing algorithm that could guess the best
possible space that is safe. Plus, I wanted to create a Minesweeper board without needing to
guess and one that requires guesses

To run the simulation, use the command:

```python simulation.py```

This will run 10 iterations of the SAT solver.
