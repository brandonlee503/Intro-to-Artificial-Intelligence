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

int MinimaxPlayer::maximumValue(int &row, int &column, char playerSymbol, OthelloBoard *board) {
	vector<OthelloBoard*> boardVector;
	int maximumRow = 0;
	int maximumColumn = 0;
	int theMax = -32767;

	if (playerSymbol == 'X') {
		boardVector = evaluatePossibleStates('X', board);
	}

	if (playerSymbol == 'O') {
		boardVector = evaluatePossibleStates('O', board);
	}

	if (boardVector.size() == 0) {
		return cost(board);
	}

	for (int i = 0; i < boardVector.size(); i++) {
		if (minimumValue(row, column, playerSymbol, boardVector[i]) > theMax) {
			maximumRow = boardVector[i]->getRow();
			maximumColumn = boardVector[i]->getColumn();
			theMax = minimumValue(row, column, playerSymbol, boardVector[i]);
		}
	}

	row = maximumRow;
	column = maximumColumn;
	return theMax;
}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}
