#ifndef HUMAN_PLAYER
#define HUMAN_PLAYER

#include "Player.h"
#include "OthelloBoard.h"

/**
 * This class represents a human player
 */
class HumanPlayer : public Player {
public:

	/**
	 * @symb The symbol used for the human player's pieces
	 * The constructor for the HumanPlayer class
	 */
    HumanPlayer(char symb);

    /**
     * Destructor
     */
    virtual ~HumanPlayer();

    /**
     * @param b The current board for the game.
     * @param col Holds the return value for the column of the move
     * @param row Holds the return value for the row of the move
     * Obtains the (col,row) coordinates for the current move
     */
    void get_move(OthelloBoard* b, int& col, int& row);

    /**
     * @return A pointer to a copy of the HumanPlayer object
     * This is a virtual copy constructor
     */
    HumanPlayer *clone();
private:

};

#endif
