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
  
def BFS(src, dest, visited, pred, dist, board):
  queue = []
  dist[src.getx()][src.gety()] = 0
  queue.append(src)
  while (len(queue) != 0):
    u = queue[0]
    queue.pop(0)
    for i in range(len(u.surrounding)):
      neighbours = u.surrounding[i]
      if (visited[neighbours.getx()][neighbours.gety()] == False):
        visited[neighbours.getx()][neighbours.gety()] = True
        dist[neighbours.getx()][neighbours.gety()] = dist[u.getx()][u.gety()]  + 1
        pred[neighbours.getx()][neighbours.gety()] = u
        queue.append(neighbours)
        if (neighbours == dest):
          return neighbours
  return None

def RunDFSOnCards(src_card, dest_card, board, turn):
    visited = InitializeAGird(False)
    distance_to_source = InitializeAGird(999)
    predecessor = InitializeAGird(None)
    
    src = board.grid[src_card.getx()][src_card.gety()]
    dest = board.grid[dest_card.getx()][dest_card.gety()]
    result = BFS(src, dest, visited, predecessor, distance_to_source, board)
    if result is not None:
      nextpoint = findNextMove(predecessor, dest, src).coordinate
      print_slide(turn,src_card.coordinate[0],src_card.coordinate[1],nextpoint[0],nextpoint[1])
      src_card.Move(nextpoint,board)

def findNextMove(predecessor, dest, src):
  temp = dest
  while(predecessor[temp.getx()][temp.gety()] is not src):
    temp = predecessor[temp.getx()][temp.gety()]
  return temp