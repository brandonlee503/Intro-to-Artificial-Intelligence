#include <iostream>
#include <cstring>
#include <stdlib.h>
#include "GameDriver.h"

GameDriver::GameDriver(char* p1type, char* p2type, int num_rows, int num_cols) {
	if( strcmp(p1type,"human") == 0 ) {
		p1 = new HumanPlayer('X');
	} else if( strcmp(p1type,"minimax") == 0 ) {
		p1 = new MinimaxPlayer('X');
	} else {
		std::cout << "Invalid type of player for player 1" << std::endl;
	}

	if( strcmp(p2type,"human") == 0 ) {
		p2 = new HumanPlayer('O');
	} else if( strcmp(p2type,"minimax") == 0 ) {
		p2 = new MinimaxPlayer('O');
	} else {
		std::cout << "Invalid type of player for player 2" << std::endl;
	}

	board = new OthelloBoard(num_rows, num_cols,p1->get_symbol(), p2->get_symbol());
	board->initialize();
}

GameDriver::GameDriver(const GameDriver& other) {
	board = new OthelloBoard(*(other.board));
	p1 = other.p1->clone();
	p2 = other.p2->clone();
}

GameDriver& GameDriver::operator=(const GameDriver& rhs) {
	if (this == &rhs) {
		return *this;
	} else {
		if( board != NULL ) {
			delete board;
		}
		board = new OthelloBoard(*(rhs.board));
		if( p1 != NULL ) {
			delete p1;
			p1 = rhs.p1->clone();
		}
		if( p2 != NULL ) {
			delete p2;
			p2 = rhs.p2->clone();
		}
		return *this;
	}
}
GameDriver::~GameDriver() {
	delete board;
	delete p1;
	delete p2;
}

void GameDriver::display() {
	std::cout << std::endl << "Player 1 (" << p1->get_symbol() << ") score: "
			<< board->count_score(p1->get_symbol()) << std::endl;
	std::cout << "Player 2 (" << p2->get_symbol() << ") score: "
			<< board->count_score(p2->get_symbol()) << std::endl << std::endl;

	board->display();
}

void GameDriver::process_move(Player* curr_player, Player* opponent) {
	int col = -1;
	int row = -1;
	bool invalid_move = true;
	while (invalid_move) {
		curr_player->get_move(board, col, row);
		if (!board->is_legal_move(col, row, curr_player->get_symbol())) {
			std::cout << "Invalid move.\n";
			continue;
		} else {
			std::cout << "Selected move: col = " << col << ", row = " << row << std::endl;
			board->play_move(col,row,curr_player->get_symbol());
			invalid_move = false;
		}
	}
}

void GameDriver::run() {
    int toggle = 0;
    int cant_move_counter=0;
    Player* current = p1;
    Player* opponent = p2;

    display();
    std::cout << "Player 1 (" << p1->get_symbol() << ") move:\n";
    while (1) {
	if( board->has_legal_moves_remaining(current->get_symbol())) {
	    cant_move_counter = 0;
	    process_move(current, opponent);
	    display();
	} else {
	    std::cout << "Can't move\n";
	    if( cant_move_counter == 1 ) {
		// Both players can't move, game over                       
		break;
	    } else {
		cant_move_counter++;
	    }
	}
	toggle = (toggle + 1) % 2;
	if (toggle == 0) {
	    current = p1;
	    opponent = p2;
	    std::cout << "Player 1 (" << p1->get_symbol() << ") move:\n";
	} else {
	    current = p2;
	    opponent = p1;
	    std::cout << "Player 2 (" << p2->get_symbol() << ") move:\n";
	}
    }

    if ( board->count_score(p1->get_symbol()) == board->count_score(p2->get_symbol())) {
	std::cout << "Tie game" << std::endl;
    } else if ( board->count_score(p1->get_symbol()) > board->count_score(p2->get_symbol())) {
	std::cout << "Player 1 wins" << std::endl;
    } else {
	std::cout << "Player 2 wins" << std::endl;
    }
}

int main(int argc, char** argv) {
	if( argc != 3 ) {
		std::cout << "Usage: othello <player1 type> <player2 type>" << std::endl;
		exit(-1);
	}
	GameDriver* game = new GameDriver(argv[1],argv[2],4,4);
	game->run();
	return 0;
}
