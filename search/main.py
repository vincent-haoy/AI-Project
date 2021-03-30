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
    #stage1
    Upper = []
    Blocks = []
    #stage2    
    Upper_p = []
    Upper_s = []
    Upper_r = []
    #stage3
    Lower_p = []
    Lower_s = []
    Lower_r = []
    Lower = [] 
    board_dict ={

    }

    for i in data['upper']:
        board_dict[tuple((i[1],i[2]))] = i[0]
        Upper.append((MyNode(i[0],"upper",tuple((i[1],i[2])),game)))   
    for i in data['lower']:
        board_dict[tuple((i[1],i[2]))] = i[0]
        Lower.append((MyNode(i[0],"lower",tuple((i[1],i[2])),game)))
        """
        if(i[0] == "p"):
            Lower_p.append((MyNode(i[0],"lower",tuple((i[1],i[2])),game)))
        elif(i[0] == "s"):
            Lower_s.append((MyNode(i[0],"lower",tuple((i[1],i[2])),game)))
        elif(i[0] == "r"):
            Lower_r.append((MyNode(i[0],"lower",tuple((i[1],i[2])),game)))
        """            
    for i in data['block']: 
        board_dict[tuple((i[1],i[2]))] = 'b'
        Blocks.append((MyNode("b","block",tuple((i[1],i[2])),game)))
    #move dict for the next move:
    move_dic = {

    }
    turn = 1
    print_board(board_dict)
    while(len(Lower)>0):

        for current_card in Upper:
            nextpoint = RunDFSOnCards(current_card, game, turn)
            if nextpoint is not None:
                move_dic[current_card] = nextpoint
            else:
                print("didnt find")
                continue

        for key in move_dic.keys():
            printMove(turn,key,move_dic[key])
            key.Move(move_dic[key],game)
        
        for key in list(move_dic.keys()):   
            settlement(move_dic[key],game,Upper,Lower,move_dic)
        turn+=1
#python -m search search/1v2.json