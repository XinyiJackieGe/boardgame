# boardgame
> This project creates a board game to test whether Minimax, Alpha-Beta Pruning, Cutting-Off Search and Q-Learning algorithms 
solve adversarial gamess with rewards not only at but also before ternimal.



## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Run code](#run-code)



## General info
This is a x*y board game.
For each step there will be a prompt to tell you what to input. 
If the input does not meet the requirements, then it will prompt again until they are satisfied. 
First, you will be asked to enter the size of board, number of rows and columns. 
Then, you will need to choose one of the four algorithms to run. 
For Q-learning, it will also ask you to enter the number of trials you want to train the algorithm. 
The steps after will be the same for all four scenarios. 
You will enter three numbers: the two coordinates of the piece you want to move one step forward and the direction (either straight or to the left or to the right)


## Technologies
* Python - version 3.7.

## Run code
python3 Game.py 
How many rows you want for the board game?4
How many columns?4
Which algorithm you would like to run this game?
1. Minimax 2. Alpha-beta 3. Cutting-off search. 4. QLearning
Please enter between 1 to 4: 1
0 OOOO 
1 ____ 
2 ____ 
3 XXXX 
  0123 

Please enter x coordinate you want to move:3 
Please enter y coordinate you want to move:3 
Please enter horizontal moves you want:0 

python3 Game.py
How many rows you want for the board game?4
How many columns?4
Which algorithm you would like to run this game?
1. Minimax 2. Alpha-beta 3. Cutting-off search. 4. QLearning
Please enter between 1 to 4: 4
How many training iterations?1000
Training 1000 iterations...
