#!/bin/bash

# function diffCheck() {
#     theDiff = diff test1.txt test2.txt
#     if [[ "$theDiff" == "" ]];
#     then
#         echo "WE OKAY"
#     else
#         echo "PROBLEM"
#     fi
# }

#BFS
echo "BFS Tests"
python reference.py start1.txt goal1.txt bfs test1.txt
python copy.py start1.txt goal1.txt bfs test2.txt

# diffCheck

python reference.py start2.txt goal2.txt bfs test1.txt
python copy.py start2.txt goal2.txt bfs test2.txt

python reference.py start3.txt goal3.txt bfs test1.txt
python copy.py start3.txt goal3.txt bfs test2.txt

#DFS
echo "DFS Tests"
python reference.py start1.txt goal1.txt dfs test1.txt
python copy.py start1.txt goal1.txt dfs test2.txt

python reference.py start2.txt goal2.txt dfs test1.txt
python copy.py start2.txt goal2.txt dfs test2.txt

python reference.py start3.txt goal3.txt dfs test1.txt
python copy.py start3.txt goal3.txt dfs test2.txt

#IDDFS
echo "IDDFS Tests"
python reference.py start1.txt goal1.txt iddfs test1.txt
python copy.py start1.txt goal1.txt iddfs test2.txt

python reference.py start2.txt goal2.txt iddfs test1.txt
python copy.py start2.txt goal2.txt iddfs test2.txt

python reference.py start3.txt goal3.txt iddfs test1.txt
python copy.py start3.txt goal3.txt iddfs test2.txt

#A*
echo "A* Tests"
python reference.py start1.txt goal1.txt a* test1.txt
python copy.py start1.txt goal1.txt a* test2.txt

python reference.py start2.txt goal2.txt a* test1.txt
python copy.py start2.txt goal2.txt a* test2.txt

python reference.py start3.txt goal3.txt a* test1.txt
python copy.py start3.txt goal3.txt a* test2.txt
