"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""
# haoyu: how to run this program
# python -m search search/ + "file name";
# eg :python -m search search/test1.json
import sys
import json

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing
from search.datastructure import *
from search.SearchingAlgorithm import *
def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).

    game = Board()
    Upper = []
    Lower = []
    Blocks = []
    for i in data['upper']:
        Upper.append((MyNode(i[0],"upper",tuple((i[1],i[2])),game)))   
    for i in data['lower']:
        Lower.append((MyNode(i[0],"lower",tuple((i[1],i[2])),game)))
    for i in data['block']: 
        Blocks.append((MyNode(i[0],"block",tuple((i[1],i[2])),game)))
    
    
    turn = 0
    while(Upper[0].coordinate != Lower[0].coordinate):
        RunDFSOnCards(Upper[0], Lower[0], game, turn)
        turn+=1
    
    """
    board_dict = {
        
    }
    Allcards = []
    Allcards = Allcards + Upper + Lower + Blocks
    for i in Allcards:
        board_dict[i.coordinate] = i.role 
    print_board(board_dict, "message goes here", ansi=False)
    """
