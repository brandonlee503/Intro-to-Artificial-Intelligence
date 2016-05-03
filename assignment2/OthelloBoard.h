/*
 * OthelloBoard.h
 *
 *  Created on: Apr 18, 2015
 *      Author: wong
 */

#ifndef OTHELLOBOARD_H_
#define OTHELLOBOARD_H_

#include "Board.h"

/**
 * This class is a specialized version of the Board class for Othello. The OthelloBoard
 * class respects the rules of Othello and also keeps track of the symbols for Player
 * 1 and Player 2.
 */
class OthelloBoard : public Board {
public:

	/**
	 * @cols The number of columns in the game of Othello
	 * @rows The number of rows in the game of Othello
	 * @p1_symbol The symbol used for Player 1's pieces on the board
	 * @p2_symbol The symbol used for Player 2's pieces on the board
	 * This is a constructor for an OthelloBoard clas.
	 */
	OthelloBoard(int cols, int rows, char p1_symbol, char p2_symbol);

	/**
	 * @param other The OthelloBoard object you are copying from.
	 * This is the copy constructor for the OthelloBoard class.
	 */
	OthelloBoard(const OthelloBoard& other);

	/**
	 * The destructor for the OthelloBoard class.
	 */
	virtual ~OthelloBoard();

	/**
	 * Initializes the Othello board to the starting position of the pieces
	 * for Players 1 and 2
	 */
	void initialize();

	/**
	 * @param rhs The right-hand side object of the assignment
	 * @return The left-hand side object of the assignment
	 * This is the overloaded assignment operator for the OthelloBoard class
	 */
	OthelloBoard& operator=(const OthelloBoard& rhs);

	/**
	 * @param col The column for where your piece goes
	 * @param row The row for where your piece goes
	 * @return true if the move is legal, false otherwise.
	 * Checks the legality of a move that places a piece at the specified col and
	 * row.
	 */
    bool is_legal_move(int col, int row, char symbol) const;

    /**
     * @param symbol This is the symbol for the current player.
     * @param col The column for where your piece goes
     * @param row The row for where your piece goes
     * Flips the in-between pieces once you put down a piece the specified
     * col and row position. The symbol argument specifies who the
     * current move belongs to.
     */
    int flip_pieces(int col, int row, char symbol);

    /**
     * @param symbol This symbol specifies the symbol for the current player (i.e.
     * who the current move belongs to)
     * @return true if there are still moves remaining, false otherwise
     * Checks if the game is over.
     */
    bool has_legal_moves_remaining(char symbol) const;

    /**
     * @param symbol The symbol representing a particular player.
     * Returns the score for the player with the specified symbol.
     */
    int count_score(char symbol) const;

    /**
     * @param col The column where the piece goes
     * @param row The row where the piece goes
     * Plays the move by placing a piece, with the given symbol, down at the specified
     * col and row. Then, any pieces sandwiched in between the two endpoints are flipped.
     */
    void play_move(int col, int row, char symbol);

    /**
     * @return Returns the symbol for Player 1 (the maximizing player)'s pieces
     * Returns the symbol for Player 1's pieces
     */
    char get_p1_symbol() { return p1_symbol; }

    /**
     * @return Returns the symbol for Player 2 (the minimizing player)'s pieces
     * Returns the symbol for Player 2's pieces
     */
    char get_p2_symbol() { return p2_symbol; }

private:

    /** The symbol for Player 1's pieces */
    char p1_symbol;

    /** The symbol for Player 2's pieces */
    char p2_symbol;

    /**
     * @param col The column of the starting point
     * @param row The row of the starting point
     * @param next_col The return value for the column
     * @param next_row The return value for the row
     * @param dir The direction you want to move
     * Sets the coordinates of next_col and next_row to be the coordinates if you were
     * moving in the direction specified by the argument dir starting at position (col,row)
     */
    void set_coords_in_direction(int col, int row, int& next_col, int& next_row, int dir) const;

    /**
     * @param col The column of the starting point
     * @param row The row of the starting point
     * @param symbol The symbol of the current player. You will match (or not match) this symbol
     * at the endpoint
     * @param dir The direction you are moving in
     * @param match_symbol If true, it will return true if the arg symbol matches the endpoint. If false,
     * it will return true if the arg symbol doesn't match the endpoint.
     * If you start at (col,row) and move in direction dir, this function will check the endpoint
     * of a trail of pieces. If match_symbol is true, it will return true if the endpoint matches
     * the argument symbol (and false otherwise). If match_symbol is false, it will return true
     * if the endpoint doesn't match the argument symbol (and false otherwise).
     */
    bool check_endpoint(int col, int row, char symbol, int dir,
			 bool match_symbol) const;

    /**
     * @param col The column of the starting point
     * @param row The row of the starting point
     * @param symbol This is the symbol at the endpoint that terminates the row of pieces flipped
     * @param dir The direction you are moving
     * This is a helper function for the recursive flip_pieces function.
     */
    int flip_pieces_helper(int col, int row, char symbol, int dir);
};

#endif /* OTHELLOBOARD_H_ */
