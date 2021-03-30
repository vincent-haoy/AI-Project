from search.datastructure import *
from search.util import print_board, print_slide, print_swing
def InitializeAGird(g):
  grid = [[] for i in range(9)]
  for i in range(9):
    grid[i] = [None]*9
    ran = range(-4, +4+1)
  for (r,q) in [(r,q) for r in ran for q in ran if -r-q in ran]:
    grid[r+4][q+4] = g
  return grid
  
def BFS(src, target, restraint,visited, pred, dist, board):

  queue = []
  dist[src.getx()][src.gety()] = 0
  queue.append(src)
  while (len(queue) != 0):
    u = queue[0]
    queue.pop(0)
    for i in range(len(u.surrounding)): 
      neighbours = u.surrounding[i]
      neighbours_cards_len = len(neighbours.cards)
      if(neighbours_cards_len>0):
        if(HasAlly(neighbours.cards)):
          all_neighbours = neighbours.surrounding
          neighbours_surrounding_len = len(all_neighbours)
          for g in range(neighbours_surrounding_len):    
            if (visited[all_neighbours[g].getx()][all_neighbours[g].gety()] == False):
              visited[all_neighbours[g].getx()][all_neighbours[g].gety()] = True
              if(all_neighbours[g].cards != [] and (all_neighbours[g].cards[0].side == "block" or all_neighbours[g].cards[0].role == restraint)):
                continue
              dist[all_neighbours[g].getx()][all_neighbours[g].gety()]= dist[u.getx()][u.gety()]  + 1
              pred[all_neighbours[g].getx()][all_neighbours[g].gety()] = u
              queue.append(all_neighbours[g])
              if (all_neighbours[g].cards != [] and all_neighbours[g].cards[0].role == target and HasEnemy(all_neighbours[g].cards)):
                return all_neighbours[g]
        elif(neighbours.cards[0].side == "block" or neighbours.cards[0].role == restraint):
          visited[neighbours.getx()][neighbours.gety()] = True
          continue        
      if (visited[neighbours.getx()][neighbours.gety()] == False):
        visited[neighbours.getx()][neighbours.gety()] = True
        dist[neighbours.getx()][neighbours.gety()] = dist[u.getx()][u.gety()]  + 1
        pred[neighbours.getx()][neighbours.gety()] = u
        queue.append(neighbours)
        if (neighbours.cards != [] and neighbours.cards[0].role == target and HasEnemy(neighbours.cards)):
          return neighbours
  return None

def RunDFSOnCards(src_card,board, turn):
    target = src_card.WantedOpponentRole()
    restraint = src_card.ResistanceOpponentRole()
    visited = InitializeAGird(False)
    distance_to_source = InitializeAGird(999)
    predecessor = InitializeAGird(None)
    
    src = board.grid[src_card.getx()][src_card.gety()]
    result = BFS(src, target,restraint, visited, predecessor, distance_to_source, board)
    if result is not None:
      nextpoint = findNextMove(predecessor, result, src).coordinate
      return nextpoint
    else:
      return None

def findNextMove(predecessor, dest, src):
  temp = dest
  while(predecessor[temp.getx()][temp.gety()] is not src):
    temp = predecessor[temp.getx()][temp.gety()]
  return temp


def printMove(turn,current_card, nextpoint):
  if (abs(nextpoint[0] - current_card.coordinate[0])<= 1)and(abs(nextpoint[1] - current_card.coordinate[1])<= 1):
    print_slide(turn,current_card.coordinate[0],current_card.coordinate[1],nextpoint[0],nextpoint[1])    
  else:
    print_swing(turn,current_card.coordinate[0],current_card.coordinate[1],nextpoint[0],nextpoint[1])

def settlement(coordinate,board,upper,lower,move_dic):
  upper_tokens = [x for x in board.grid[coordinate[0]+4][coordinate[1]+4].cards if x.getside() =="upper" ]
  lower_tokens = [x for x in board.grid[coordinate[0]+4][coordinate[1]+4].cards if x.getside() =="lower" ]
  hasp = False
  hass = False
  hasr = False
  for i in upper_tokens + lower_tokens:
    if i.role == 's':
      hass = True
    if i.role == 'p':
      hasp = True
    if i.role == 'r':
      hasr = True
  for g in upper_tokens:
    if((hasp and g.ResistanceOpponentRole()=='p') or (hass and g.ResistanceOpponentRole()=='s') or (hasr and g.ResistanceOpponentRole() == 'r')):
      move_dic.pop(g)
      upper.remove(g)
      board.deleOnboard(g)        
  for z in lower_tokens:
    if((hasp and z.ResistanceOpponentRole()=='p') or (hass and z.ResistanceOpponentRole()=='s') or (hasr and z.ResistanceOpponentRole() == 'r')):
      lower.remove(z)
      board.deleOnboard(z)

def HasAlly(cards):
  for card in cards:
    if card.side == "upper":
      return True
  return False

def HasEnemy(cards):
  for card in cards:
    if card.side == "lower":
      return True
  return False