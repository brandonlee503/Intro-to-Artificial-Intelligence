#include <iostream>
#include "HumanPlayer.h"

HumanPlayer::HumanPlayer(char symb) : Player(symb) {

}

HumanPlayer::~HumanPlayer() {

}

void HumanPlayer::get_move(OthelloBoard* b, int& col, int& row) {
    std::cout << "Enter col: ";
    std::cin >> col;
    std::cout << "Enter row: ";
    std::cin >> row;
}

HumanPlayer* HumanPlayer::clone() {
	HumanPlayer *result = new HumanPlayer(symbol);
	return result;
}
