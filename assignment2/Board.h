/**
 * Board class
 */

#ifndef BOARD_H
#define BOARD_H

#define EMPTY '.'

/** Directions enum for the Othello Board */
enum Direction {N,NE,E,SE,S,SW,W,NW};

/**
 * This is a generic board class that serves as a wrapper for a 2D array.
 * It will be used for board games like Othello, Tic-Tac-Toe and Connect 4.
 */
class Board {
public:

	/**
	 * @param cols The number of columns in the board
	 * @param rows The number of rows in the board
	 * Constructor that creates a 2D board with the given number of columns
	 * and rows
	 */
    Board(int cols, int rows);

    /**
     * @param other A reference to the Board object being copied
     * This is the copy constructor for the Board class
     */
    Board(const Board& other);

    /**
     * Destructor for the Board class
     */
    ~Board();

    /**
     * @param rhs The "right-hand side" for the assignment ie. the object
     * you are copying from.
	 * @return Returns a reference to the "left-hand side" of the assignment ie.
	 * the object the values are assigned to
     * Overloaded assignment operator for the Board class
     */
    Board& operator=(const Board& rhs);

    /**
     * @return Returns the number of rows in the board
     * An accessor that gets the number of rows in the board
     */
    int get_num_rows() const { return num_rows; }

    /**
     * @return Returns the number of columns in the board
     * An accessor to get the number of columns in the board
     */
    int get_num_cols() const { return num_cols; }

    /**
     * @param col The column of the cell you want to retrieve
     * @param row The row of the cell you want to retrieve
     * @return Returns the character at the specified cell
     * Returns the character at the specified column and row
     */
    char get_cell(int col, int row) const;

    /**
     * @param col The column of the cell you want to set
     * @param row The row of the cell you want to set
     * @param val The value you want to set the cell to
     * Sets the cell at the given row and column to the specified value
     */
    void set_cell(int col, int row, char val);

    /**
     * @param col The column of the cell you are checking
     * @param row The row of the cell you are checking
     * @return true if the cell is empty and false otherwise
     */
    bool is_cell_empty(int col, int row) const;

    /**
     * @param col The column value for the in-bounds check
     * @param row The row value for the in-bounds check
     * @return true if the column is >= 0 and < num_cols and if the row is >= 0 and < num_rows. Returns false otherwise.
     */
    bool is_in_bounds(int col, int row) const;

    /**
     * Prints the board to screen. Should probably have overloaded >> but oh well.
     */
    void display() const;

protected:

    /** The number of rows in the board */
    int num_rows;

    /** The number of columns in the board */
    int num_cols;

    /** A 2D array of chars representing the board */
    char** grid;

    /**
     * Deletes the 2D array.
     */
    void delete_grid();
};

#endif
