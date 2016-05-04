/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include "MinimaxPlayer.h"

using std::vector;

MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}

int MinimaxPlayer::cost(OthelloBoard *board) {
	return board->count_score(board->get_p1_symbol()) - board->count_score(board->get_p2_symbol());
}

// Evaluate the moves possible moves remaining in the game...
vector<OthelloBoard*> MinimaxPlayer::evaluatePossibleStates(char playerSymbol, OthelloBoard *board) {
	int stateCounter = 0;
	int boardDimensions = 4;
	vector<OthelloBoard*> boardVector;

	// Check every spot in the 2D array
	for (int i = 0; i < boardDimensions; i++) {
		for (int j = 0; j < boardDimensions; j++) {

			// Check the possible moves and simulate all possible boards
			if (board->is_legal_move(i, j, playerSymbol)) {
				boardVector.push_back(new OthelloBoard(*board));
				boardVector.back()->play_move(i, j, symbol);

				// TODO: if error its cause i flipped these
				boardVector.back()->setColumn(i);
				boardVector.back()->setRow(j);
			}
		}
	}

	return boardVector;
}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}
