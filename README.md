Artificial intelligence The fox and the hunters:

Implementation of a game called "The Fox and the Hunters" with AI and using the Pygame library in Python. The game consists of a grid board where a fox (represented by an image) must try to avoid being captured by hunters (also represented by images) moving around the board. The fox's goal is to reach the top of the board, while the hunters try to block its path.

![image](https://github.com/YakoViTo/FoxAndHounds/assets/135473233/1b89adae-bde4-46ee-b2d1-ee1f34b09c9c)

The game allows players to alternate turns between the fox and the hunters. The fox can move diagonally up or down the board, while the hunters only move diagonally down. The fox can evade the hunters by moving strategically and taking advantage of opportunities to advance to the top.

The program uses the Minimax algorithm to make automatic decisions for hunter moves. The algorithm evaluates the possible moves and selects the best option based on an evaluation function that considers several factors, such as the position of the fox, the distance between the pieces and the chance of winning.

In general, the program implements the logic of the game "The Fox and the Hunters" and provides a graphical interface through the Pygame library for players to interact with the game and play both against the computer (hunters controlled by the Minimax algorithm) and against each other.
