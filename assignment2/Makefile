CXX = g++
CXXFLAGS = -std=c++0x
SRCS = Board.cpp OthelloBoard.cpp Player.cpp HumanPlayer.cpp GameDriver.cpp MinimaxPlayer.cpp
HEADERS = Board.h OthelloBoard.h Player.h HumanPlayer.h GameDriver.h MinimaxPlayer.h 
OBJS = Board.o OthelloBoard.o Player.o HumanPlayer.o GameDriver.o MinimaxPlayer.o 

all: ${SRCS} ${HEADERS}
	${CXX} ${CXXFLAGS} ${SRCS} -o othello

${OBJS}: ${SRCS}
	${CXX} -c $(@:.o=.cpp)

clean:
	rm -f *.o othello