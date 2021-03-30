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
import time
import random
def main():
    start = time.time()
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
    Lower = [] 
    board_dict ={

    }

    for i in data['upper']:
        board_dict[tuple((i[1],i[2]))] = i[0]
        Upper.append((MyNode(i[0],"upper",tuple((i[1],i[2])),game)))   
    for i in data['lower']:
        board_dict[tuple((i[1],i[2]))] = i[0]
        Lower.append((MyNode(i[0],"lower",tuple((i[1],i[2])),game)))         
    for i in data['block']: 
        board_dict[tuple((i[1],i[2]))] = 'b'
        Blocks.append((MyNode("b","block",tuple((i[1],i[2])),game)))
    #move dict for the next move:
    move_dic = {

    }
    no_targets = []
    turn = 1
    #print_board(board_dict)
    while(len(Lower)>0):
        p = 0
        s = 0
        r = 0
        for lower_token in Lower:
            if(lower_token.role == 'p'):
                s+=1
            elif(lower_token.role == 'r'):
                p+=1
            elif(lower_token.role == 's'):
                r+=1

        for current_card in Upper:
            nextpoint = RunDFSOnCards(current_card, game, turn)
            if nextpoint is not None:
                move_dic[current_card] = nextpoint
            else:
                if current_card in move_dic.keys():
                    move_dic.pop(current_card)
                no_targets.append(current_card)
                continue
        
        #if two tokens are move to the same location, we run random for either of them:

        move_key = [key for key in move_dic.keys()]
        move_value = [move_dic[key] for key in move_key]
        same_spot = []
        original_surrounding = []
        for i in range(len(move_key)):
            for j in range(i,len(move_key)):
                if  (i != j ) and move_dic[move_key[i]] == move_dic[move_key[j]] and (move_key[i].role != move_key[j].role):
                    same_spot.append(move_key[i])
                    same_spot.append(move_key[j])            
        for spot in same_spot:
            available = []
            for near in game.grid[spot.getx()][spot.gety()].surrounding:
                if(len(near.cards) > 0):
                    if(near.cards[0].side == 'block'):
                        continue
                    if(HasEnemy(near.cards) and spot.ResistanceOpponentRole() == near.cards[0].role):
                        continue 
                    available.append(near.coordinate)
                else:
                    available.append(near.coordinate)
            original_surrounding.append(available)
        possible_combination = []
        if(len(same_spot) == 2):
            possible_combination = [(a,b) for a in original_surrounding[0] for b in original_surrounding[1] if a !=b]
        elif(len(same_spot) ==3):
            possible_combination = [(a,b,c) for a in original_surrounding[0] for b in original_surrounding[1] for c in original_surrounding[2] if (a !=b and b!= c and c != a)]
        comibination_len = len(possible_combination)
        if(comibination_len > 0):
            randn = random.randint(0,comibination_len-1)
            move_dic[same_spot[0]] = possible_combination[randn][0]
            move_dic[same_spot[1]] = possible_combination[randn][1]
            if(len(same_spot)==3):
                move_dic[same_spot[2]]= possible_combination[randn][2]
        #if BFS cant find a target, move randomly
        for no_target in no_targets:
            # random move
            acceptable_list = []
            existing_key = [key for key in move_dic.keys()]
            existing_value =[move_dic[key] for key in existing_key]
            suicide_list = []
            for spot in game.grid[no_target.getx()][no_target.gety()].surrounding:
                if(len(spot.cards) > 0):
                    if(spot.cards[0].role == 'block'):
                        continue
                    if(HasEnemy(spot.cards) and no_target.ResistanceOpponentRole() == spot.cards[0].role):
                        suicide_list.append(spot.coordinate)
                        continue            
                else:
                    acceptable_list.append(spot.coordinate)
            
            if((len(suicide_list) > 0) and ((no_target.role == 'p' and p == 0) or (no_target.role == 's' and s ==0) or (no_target.role == 'r' and r == 0))):
                move_dic[no_target] = suicide_list [0]
                no_targets.remove(no_target)
                continue
            
            chooseable = list(set(acceptable_list) - set(existing_value))            
            if len(chooseable) > 0:
                n = random.randint(0,len(chooseable)-1)
                move_dic[no_target] = chooseable[n]
                no_targets.remove(no_target)
                continue
            else:
                g = random.randint(0,len(acceptable_list)-1)
                move_dic[no_target] = acceptable_list[g]
                no_targets.remove(no_target)
                continue

        for key in move_dic.keys():
            printMove(turn,key,move_dic[key])
            key.Move(move_dic[key],game)
        
        for key in list(move_dic.keys()):   
            settlement(move_dic[key],game,Upper,Lower,move_dic)
        turn+=1
    
#python -m search search/1v2.json