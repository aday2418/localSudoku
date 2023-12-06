from __future__ import print_function
import sys
import time
import random

# Code for AI Class Local Sudoku Programming Assignment
# Written by Chris Archibald
# archibald@cs.byu.edu
# Last Updated January 30, 2020

def student_name():
    """
    This function returns your name.  This will be used for automated grading
    """

    #MODIFY THIS TO RETURN YOUR NAME

    #Change to be your name
    return 'Alison Day'

class LCell():
    """
    This class represents a variable corresponding to an 
    individual cell in the Sudoku puzzle
    If it is fixed, that means we can't change its value
    """

    def __init__(self):

        # Is this cell fixed in the input
        self.fixed = False  
        # The value assigned to this variable if it has been assigned
        # None means that it hasn't been assigned
        self.value = None

    def fix_value(self, value):
        self.fixed = True
        self.value = value

    def assign_value(self, value):
        """
        Assign [value] to be this variable's value
        """
        if not self.fixed:
            self.value = value

    def copy_cell(self, other):
        """
        Set the value of this cell to that of the input other cell
        """
        self.fixed = other.fixed
        self.value = other.value

class LSudoku():
    """
    This class contains all of the cells for an entire Sudoku puzzle
    """

    def __init__(self):
        """
        Initialize this puzzle by creating all of the cells (initially empty)
        """
        self.cells = [[ LCell() for j in range(9)] for i in range(9) ]

    def copy_puzzle(self, other):
        """
        Set all of this puzzle's cells to be the same as the other puzzle (input to function)
        """
        [[ self.cells[j][i].copy_cell(other.cells[j][i]) for j in range(9)] for i in range(9) ]

    def to_string(self):
        """
        Return a single string representation of the puzzle. For storage purposes
        """
        output_string = ''
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value:
                    output_string += str(self.cells[r][c].value)
                else:
                    output_string += '.'
        return output_string

    def print_puzzle(self):
        """
        Display the puzzle to the output, in human readable form
        """
        for r in range(9):
            if (r % 3) == 0 and r > 0:
                print('')
            for c in range(9):
                if (c % 3) == 0 and c > 0:
                    print(' ', end="")
                if self.cells[r][c].value is None:
                    print('.', end="")
                else:
                    print(self.cells[r][c].value, end="")
            print('')

    def objective(self):
        """
        Return objective score for this puzzle, which 
        is the number of conflicts between cells
        A solution will have 0
        """
        conflicts = 0
        for r in range(9):
            for c in range(9):
                conflicts += self.count_conflicts(r,c)

        return conflicts

    def count_conflicts(self, row, column):
        """ 
        This counts the number of conflicts that the cell at row, column is
        involved in.
        """
        value = self.cells[row][column].value
        grid, cell = self.get_grid_cell(row,column)

        conflicts = 0
        #Check all the other rows in this column
        for other_row in range(row + 1, 9):
            if self.cells[other_row][column].value == value:
                conflicts += 1

        #Check all the other columns in this row
        for other_column in range(column + 1, 9):
            if self.cells[row][other_column].value == value:
                conflicts += 1

        #Check all the other cells in this grid
        for other_cell in range(cell + 1, 9):
            r, c = self.get_row_column(grid, other_cell)
            if self.cells[r][c].value == value:
                conflicts += 1

        return conflicts

    def input_puzzle(self, puzzle_string):
        """
        Initialize this puzzle to match the starting state specified by [puzzle string]
        This is done by assigning all of the cells to be their given value (if specified)
        Then forward-checking is performed for every variable assingment that has been made
        """
        # Cycle through the puzzle and assign all the cells that are given in the input string
        r = 0
        c = 0
        for v in puzzle_string:
            if v != '.':
                self.cells[r][c].fix_value(int(v))
            c += 1
            if c > 8:
                c = 0
                r += 1

    def get_row_column(self, grid, cell):
        '''
        Return the row and column indices for a given [grid] and [cell] location
        '''
        base_r = 3*int(grid / 3)
        base_c = 3*(grid % 3)
        off_r = int(cell / 3)
        off_c = cell % 3
        return base_r + off_r, base_c + off_c

    def get_grid_cell(self, row, column):
        '''
        Return the grid and cell indices for a given [row] and [column] location
        '''
        grid = 3*int(row / 3) + int(column / 3)
        base_r = 3*int(grid / 3)
        base_c = 3*(grid % 3)
        off_r = row - base_r
        off_c = column - base_c
        cell = 3*int(off_r) + int(off_c)
        return grid, cell

# Other functions (not in Sudoku class)
# When [puzzle] is an input 
# it is an object of the Sudoku puzzle class [Sudoku]

def local_search(puzzle):
    #Solve the puzzle using local search techniques
    initialize_puzzle(puzzle)

    # Set a limit to the number of iterations to prevent infinite loops
    max_iterations = 10000
    for _ in range(max_iterations):
        current_conflicts = puzzle.objective()

        # Check if the puzzle is solved
        if current_conflicts == 0:
            return puzzle

        # Generate a neighbor
        neighbor = generate_neighbor(puzzle)

        # Check if the neighbor is better
        if neighbor.objective() < current_conflicts:
            puzzle.copy_puzzle(neighbor)

    # Didn't solve the puzzle
    return None

def initialize_puzzle(puzzle):
    for row in range(9):
        for col in range(9):
            if not puzzle.cells[row][col].fixed:
                possible_values = list(range(1, 10))
                random.shuffle(possible_values)
                for value in possible_values:
                    if not has_conflict(puzzle, row, col, value):
                        puzzle.cells[row][col].assign_value(value)
                        break

def has_conflict(puzzle, row, col, value):
    # Check row and column
    for i in range(9):
        if puzzle.cells[row][i].value == value or puzzle.cells[i][col].value == value:
            return True

    # Check 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if puzzle.cells[r][c].value == value:
                return True

    return False

def generate_neighbor(puzzle):
    neighbor = LSudoku()
    neighbor.copy_puzzle(puzzle)

    # Ensure that the selected row has at least two swappable cells
    valid_row = False
    for _ in range(100):  # Limit attempts to find a valid row
        row = random.randint(0, 8)
        swappable_cells = [i for i in range(9) if not neighbor.cells[row][i].fixed]
        if len(swappable_cells) >= 2:
            valid_row = True
            break

    if not valid_row:
        # If no valid row is found, return the original puzzle as the neighbor
        return puzzle

    col1, col2 = random.sample(swappable_cells, 2)

    # Swap two values
    neighbor.cells[row][col1].value, neighbor.cells[row][col2].value = \
        neighbor.cells[row][col2].value, neighbor.cells[row][col1].value

    return neighbor

if __name__ == "__main__":

    # Check the input arguments (should just be the puzzle file)
    if len(sys.argv) != 2:
        print('USAGE: python pa2.py PUZZLE_FILE.txt')
    else:
        print('Searching for solutions to puzzles from file: ', sys.argv[1])
        
        # Open puzzle file
        pf = open(sys.argv[1],'r')
               
        # Variable to keep track of the difficulty of puzzle solved
        difficulty = 1

        # Start time for solving            
        start_time = time.time()

        # Each puzzle takes up a single line in the file
        for ps in pf.readlines():
            print('\nSearching to find solution to following puzzle at level', difficulty, ':', ps)

            # Create a new puzzle to solve
            p = LSudoku()
            
            # Initialize the puzzle to match the file
            p.input_puzzle( ps.rstrip() )
            
            # Display the puzzle (before it has been solved)
            p.print_puzzle()

            # Solve the puzzle 
            success_p = local_search(p)

            # If the puzzle was solved (success_p is the puzzle, None if no solution)
            if success_p: 
                print('\n Successfully solved puzzle!  Here is solution:\n')
                
                # Display the solution to the puzzle
                success_p.print_puzzle()
                difficulty += 1
                # Update the statistics

            else:
                print('\n!! Unable to solve puzzle !!\n')
                break

        # Record end time 
        end_time = time.time()

        # Close the puzzle file
        pf.close()

        # Print Statistics
        print('\n**************\nSolved puzzles up to difficulty', difficulty, 'in', end_time - start_time, ' seconds. ')

        # Compute and display average solve time
        average_time = 0
        if difficulty > 1:
            average_time =  (end_time - start_time) / float(difficulty-1)
        print('  Average Solve Time = ', average_time, ' seconds')

