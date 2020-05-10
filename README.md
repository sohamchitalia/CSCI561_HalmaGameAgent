# CSCI561_HalmaGameAgent

An agent to play the 'Halma' game. 

## About Halma

![Halma board](https://i.brainking.com/rules/halma/01.gif)

Halma is a strategy board game invented in 1883 or 1884 by George Howard Monks, a US thoracic surgeon at Harvard Medical School. His inspiration was the English game Hoppity which was devised in 1854.
The game is played by two or four players seated at opposing corners of the board. The game is won by being first to transfer all of one's pieces from one's own camp into the camp in the opposing corner. For four-player games played in teams, the winner is the first team to race both sets of pieces into opposing camps. On each turn, a player either moves a single piece to an adjacent open square, or jumps over one or more pieces in sequence.

## About The Agent

This game playing agent is designed to play a 2 player Halma game. The main goal is to have all of its pieces in the opposition camp.
The agent takes the current state of the board as input and outputs the best possible move.
In order to predict the best move, minimax algorithm is used. A tree with depth = 3 is created and then alpha beta pruning is used to prune this tree in order to increase the search efficiency. 
By evaluating the values at various nodes, the move resulting in the best utility value is chosen. 



