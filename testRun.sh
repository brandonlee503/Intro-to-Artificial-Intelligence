#!/bin/bash

#BFS
echo "BFS Tests"
python assignment1.py start1.txt goal1.txt bfs output.txt
python assignment1.py start2.txt goal2.txt bfs output.txt
python assignment1.py start3.txt goal3.txt bfs output.txt


#DFS
echo "DFS Tests"
python assignment1.py start1.txt goal1.txt dfs output.txt
python assignment1.py start2.txt goal2.txt dfs output.txt
python assignment1.py start3.txt goal3.txt dfs output.txt

#IDDFS
echo "IDDFS Tests"
python assignment1.py start1.txt goal1.txt iddfs output.txt
python assignment1.py start2.txt goal2.txt iddfs output.txt
python assignment1.py start3.txt goal3.txt iddfs output.txt

#A*
echo "A* Tests"
python assignment1.py start1.txt goal1.txt a* output.txt
python assignment1.py start2.txt goal2.txt a* output.txt
python assignment1.py start3.txt goal3.txt a* output.txt
