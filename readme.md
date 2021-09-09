[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
# Cluedo game solver
## Project Goal
[Cluedo](https://en.wikipedia.org/wiki/Cluedo) is a popular board game. The
object of the game is to determine who murdered the game's victim, where and
which weapon was used. Each player attempts to deduce the correct answer by
strategically moving around a game board and collecting clues about the
circumstances of the murder from the other players.

The aim of the project is to create the perfect Cluedo player, who extracts all
the possible information from the ongoing game, delivering the solution as soon
as it is logically possible.

The initial idea is to realize an algorithm which can be fed up with the events
of the game in the simplest way possible, making its way towards the solution.

Python-wise, this project is a way for me to explore the object-oriented
programming which I rarely use while performing data analysis.

# Usage
## How to run the code
To run the code you should download the entire content of the repository in a folder. Then you can run the following command from the command line:
```console
python Cluedo.py
```
The idea is that a player should register what happens in a real game with this script. The program will then eventually tell the player what is the solution of the game.

## Required packages
No external library is required to run this code.

# Ideas for future improvements
Some ideas for improvements are:
- Creation of a GUI
- Implementation of a log/save/load mechanism