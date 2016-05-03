/**
 * Player class
 */

#ifndef PLAYER_H
#define PLAYER_H

#include "OthelloBoard.h"

/**
 * This is an abstract base class for a Player
 */
class Player {
public:
	/**
	 * @param symb The symbol for the player's pieces
	 */
    Player(char symb);

    /**
     * Destructor
     */
    virtual ~Player();

    /**
     * @return The player's symbol
     * Gets the symbol for the player's pieces
     */
    char get_symbol() { return symbol; }

    /**
     * @param b The current board
     * @param col Holds the column of the player's move
     * @param row Holds the row of the player's move
     * Gets the next move for the player
     */
    virtual void get_move(OthelloBoard* b, int& col, int& row) = 0;

    /**
     * @return A copy of the Player object
     * Virtual copy constructor
     */
    virtual Player* clone() = 0;
protected:

    /** The symbol for the player's pieces*/
    char symbol;
};

#endif
