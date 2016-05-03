#ifndef GAMEDRIVER_H
#define GAMEDRIVER_H

#include "OthelloBoard.h"
#include "Player.h"
#include "HumanPlayer.h"
#include "MinimaxPlayer.h"

/**
 * This class represents the main driver for the game. The driver controls the turn-based behavior
 * of the game.
 */
class GameDriver {
public:

	/**
	 * @param p1type A string (human or minimax) describing the type of Player1
	 * @param p2type A string (human or minimax) describing the type of Player2
	 * @param num_rows The number of rows in Othello
	 * @param num_cols The number of columns in Othello
	 * This is the constructor for the GameDriver
	 */
    GameDriver(char* p1type, char* p2type, int num_rows, int num_cols);

    /**
     * @param other The GameDriver object you are copying from
     * Copy constructor for the GameDriver class
     */
    GameDriver(const GameDriver& other);

    /**
     * @param rhs The right-hand side of the assignment
     * @return The left-hand side of the assignment
     * Overloaded assignment operator for the GameDriver class.
     */
    GameDriver& operator=(const GameDriver& rhs);

    /**
     * Destructor for the GameDriver class
     */
    virtual ~GameDriver();

    /**
     * Runs the game and keeps track of the turns.
     */
    void run();

    /**
     * Displays the game.
     */
    void display();

private:

    /** Internal Othello board object */
    OthelloBoard* board;

    /** Player 1 object */
    Player* p1;

    /** Player 2 object */
    Player* p2;

   /**
    * @param curr_player A pointer to the player that has the current move
    * @param opponent A pointer to the opponent for the player that has the current move
    * Handles actually making a move in the game.
    */
    void process_move(Player* curr_player, Player* opponent);
};

#endif
