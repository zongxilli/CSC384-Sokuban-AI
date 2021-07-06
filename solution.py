#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import math
import os #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems

def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    
    total_distance = 0;
    
    for box in state.boxes :
      min_distance = 999999999999999999;
      
      for storage in state.storage :
        curr_distance = abs(box[0] - storage[0]) + abs(box[1] - storage[1])
        
        if curr_distance < min_distance :
          min_distance = curr_distance
        
      total_distance += min_distance
    
    return total_distance  
      
          
#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

#---------------------------------------------------------------------------------------------------------------------------------
#                                                       Helper functions

#! Check if the input coordinates is wall or obstacles -> invalid
def is_walls_or_obstacles (state, coordinates) :
  
  if coordinates[0] < 0 or coordinates[0] >= state.width : 
    return True;
  
  if coordinates[1] < 0 or coordinates[1] >= state.height :
    return True;
  
  if coordinates in state.obstacles :
    return True;
  
  return False;

#------------------------------------------------------------------------
#                           Subhelper functions

def is_box_or_obstacles_or_walls(state, coordinates) :
  return (coordinates in state.boxes) or is_walls_or_obstacles(state, coordinates)

def top_left_topLeft_haveBoxOrObstaclesOrWalls(state, box) :
  return ((is_box_or_obstacles_or_walls(state, (box[0], box[1] + 1))) 
      and (is_box_or_obstacles_or_walls(state, (box[0] - 1, box[1]))) 
      and (is_box_or_obstacles_or_walls(state, (box[0] - 1, box[1] + 1))))
  
def top_right_topRight_haveBoxOrObstaclesOrWalls(state, box) :
  return ((is_box_or_obstacles_or_walls(state, (box[0], box[1] + 1))) 
      and (is_box_or_obstacles_or_walls(state, (box[0] + 1, box[1]))) 
      and (is_box_or_obstacles_or_walls(state, (box[0] + 1, box[1] + 1))))
  
def bot_left_botLeft_haveBoxOrObstaclesOrWalls(state, box) :
  return ((is_box_or_obstacles_or_walls(state, (box[0], box[1] - 1))) 
      and (is_box_or_obstacles_or_walls(state, (box[0] - 1, box[1]))) 
      and (is_box_or_obstacles_or_walls(state, (box[0] - 1, box[1] - 1))))

def bot_right_botRight_haveBoxOrObstaclesOrWalls(state, box) :
  return ((is_box_or_obstacles_or_walls(state, (box[0], box[1] - 1))) 
      and (is_box_or_obstacles_or_walls(state, (box[0] + 1, box[1]))) 
      and (is_box_or_obstacles_or_walls(state, (box[0] + 1, box[1] - 1))))

#! Four locked  
def is_four_locked(state, box) :
  return ((top_left_topLeft_haveBoxOrObstaclesOrWalls(state, box))
        or(top_right_topRight_haveBoxOrObstaclesOrWalls(state, box))
        or(bot_left_botLeft_haveBoxOrObstaclesOrWalls(state, box))
        or(bot_right_botRight_haveBoxOrObstaclesOrWalls(state, box)))





def top_right_topLeft_haveBoxOrObstaclesOrWalls(state, box) :
  return ((is_box_or_obstacles_or_walls(state, (box[0], box[1] + 1))) 
      and (is_walls_or_obstacles(state, (box[0] + 1, box[1]))) 
      and (is_walls_or_obstacles(state, (box[0] - 1, box[1] + 1))))
  
def top_left_topRight_haveBoxOrObstaclesOrWalls(state, box) :
  return ((is_box_or_obstacles_or_walls(state, (box[0], box[1] + 1))) 
      and (is_walls_or_obstacles(state, (box[0] - 1, box[1]))) 
      and (is_walls_or_obstacles(state, (box[0] + 1, box[1] + 1))))

def bot_right_botLeft_haveBoxOrObstaclesOrWalls(state, box) :
  return ((is_box_or_obstacles_or_walls(state, (box[0], box[1] - 1))) 
      and (is_walls_or_obstacles(state, (box[0] + 1, box[1]))) 
      and (is_walls_or_obstacles(state, (box[0] - 1, box[1] - 1))))
 
def bot_left_botRight_haveBoxOrObstaclesOrWalls(state, box) :
  return ((is_box_or_obstacles_or_walls(state, (box[0], box[1] - 1))) 
      and (is_walls_or_obstacles(state, (box[0] - 1, box[1]))) 
      and (is_walls_or_obstacles(state, (box[0] + 1, box[1] - 1)))) 

#! Z locked
def is_Z_locked(state, box) :
  return ((top_right_topLeft_haveBoxOrObstaclesOrWalls(state, box))
        or(top_left_topRight_haveBoxOrObstaclesOrWalls(state, box))
        or(bot_right_botLeft_haveBoxOrObstaclesOrWalls(state, box))
        or(bot_left_botRight_haveBoxOrObstaclesOrWalls(state, box)))

   
# Check if the input box is dead
def dead (state, box) :

  left_is_invalid  = is_walls_or_obstacles(state, (box[0] - 1, box[1]))
  right_is_invalid = is_walls_or_obstacles(state, (box[0] + 1, box[1]))
  top_is_invalid   = is_walls_or_obstacles(state, (box[0], box[1] + 1))
  bot_is_invalid   = is_walls_or_obstacles(state, (box[0], box[1] - 1))

  #-------------------------------------------------------------------------------
  #     #        #                       #               #       #         #
  #     $#      #$      #$       $#      $#     #$#     #$      #$#       #$#
  #                      #       #       #       #       #                 # 
  #-------------------------------------------------------------------------------
  # Check if it is one situation of above
  
  if (left_is_invalid or right_is_invalid) and (top_is_invalid or bot_is_invalid) :
    return True;
  
  #-------------------------------------------------------------------------------
  #                               #########################
  #                               #           $           #
  #                               #       .               #
  #-------------------------------------------------------------------------------
  # Check if the box is close to wall and there is no storage along the wall
  
  storages_x_coordinates = [storage[0] for storage in state.storage]
  storages_y_coordinates = [storage[1] for storage in state.storage]
  
  
  #-------------------------------------------------------------------------------
  #                               #########################
  #                               #     .   #   $         #
  #                               #                       #
  #-------------------------------------------------------------------------------
  # Check if the box is close to wall and there is a storage along the wall
  # but there is a obstacles between the box and the storage
  
  
  # Left and right walls
  if ((box[0] == 0) or (box[0] == state.width - 1)) :
    if box[0] not in storages_x_coordinates : 
      return True;
    else :
      for obstacle in state.obstacles :
        for storage in state.storage :
          if (box[0] == storage[0]) and (box[0] == obstacle[0]) :
            if (obstacle[1] >= box[1] and obstacle[1] <= storage[1]) :
              return True
            elif (obstacle[1] <= box[1] and obstacle[1] >= storage[1]) :
              return True
            
      
   
  # Top and bottom walls
  if ((box[1] == 0) or (box[1] == state.height - 1)) :
    if box[1] not in storages_y_coordinates :
      return True
    else :
      for obstacle in state.obstacles :
        for storage in state.storage :
          if (box[1] == storage[1]) and (box[1] == obstacle[1]) :
            if (obstacle[0] >= box[0] and obstacle[0] <= storage[0]) :
              return True
            elif (obstacle[0] <= box[0] and obstacle[0] >= storage[0]) :
              return True
  
  #-------------------------------------------------------------------------------
  #   #########################     #########################    #########################
  #   #                       #     #                       #    #            $$         #
  #   #          #$           #     #           $$          #    #                       #
  #   #          #$           #     #           $$          #    #                       #
  #-------------------------------------------------------------------------------
  # Check if there are four boxes or obstacles or mixed together
  
  if (is_four_locked(state, box)) :
    return True;
  
  #-------------------------------------------------------------------------------
  #   #########################     #########################  
  #   #                       #     #                       #    
  #   #          #$           #     #           ##          #    
  #   #           $#          #     #            $#         #    
  #-------------------------------------------------------------------------------
  # Check if there are a Z shape locked
  
  if (is_Z_locked(state, box)) :
    return True;
  
  
  return False;

#------------------------------------------------------------------------

def any_box_in_state_is_dead(state) :
  boxes_need_move = list(state.boxes - state.storage)
  for box in boxes_need_move :
    if dead(state, box) :
      return True;
  
  return False;

#---------------------------------------------------------------------------------------------------------------------------------






def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    
    if any_box_in_state_is_dead(state) :
      return 999999999999999999;
    
    boxes_need_move = list(state.boxes - state.storage)
    storages_are_empty = list(state.storage - state.boxes)
    
    # Distance 
    heuristic_distance = 0;
    # list to store abs distances
    count = []
    
    for box in boxes_need_move:
      
      # Boxes   <=>   Storages
      for storage in storages_are_empty:
        
        count.append(abs(box[0] - storage[0]) + abs(box[1] - storage[1]))
      
      heuristic_distance += min(count)
      count = []
      
      # Boxes   <=>   Robots
      for robot in state.robots :
        
        count.append(abs(box[0] - robot[0]) + abs(box[1] - robot[1]))
      
      heuristic_distance += min(count)
      count = []
        
    return heuristic_distance
        

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.
    Use this function stub to encode the standard form of weighted A* (i.e. g + w*h)

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval

def fval_function_XUP(sN, weight):
#IMPLEMENT
    """
    Another custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.
    Use this function stub to encode the XUP form of weighted A* 

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    part1 = 1/(2*weight)
    part2 = sN.gval + sN.hval
    part3 = (sN.gval+sN.hval)**2
    part4 = 4*weight*(weight-1)*sN.hval**2
    
    result = part1 * (part2 + math.sqrt(part3 + part4 ))
    
    return result
  

def fval_function_XDP(sN, weight):
#IMPLEMENT
    """
    A third custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.
    Use this function stub to encode the XDP form of weighted A* 

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    part1 = 1/(2*weight)
    part2 = sN.gval
    part3 = (2*weight-1)*sN.hval
    part4 = (sN.gval-sN.hval)**2
    part5 = 4*weight*sN.gval*sN.hval
    
    result =  part1 * (part2 + part3 + math.sqrt(part4 + part5))
    
    return result
  
def compare_weighted_astars():
#IMPLEMENT
    '''Compares various different implementations of A* that use different f-value functions'''
    '''INPUT: None'''
    '''OUTPUT: None'''
    """
    This function should generate a CSV file (comparison.csv) that contains statistics from
    4 varieties of A* search on 3 practice problems.  The four varieties of A* are as follows:
    Standard A* (Variant #1), Weighted A*  (Variant #2),  Weighted A* XUP (Variant #3) and Weighted A* XDP  (Variant #4).  
    Format each line in your your output CSV file as follows:

    A,B,C,D,E,F

    where
    A is the number of the problem being solved (0,1 or 2)
    B is the A* variant being used (1,2,3 or 4)
    C is the weight being used (2,3,4 or 5)
    D is the number of paths extracted from the Frontier (or expanded) during the search
    E is the number of paths generated by the successor function during the search
    F is the overall solution cost    

    Note that you will submit your CSV file (comparison.csv) with your code
    """

    for i in range(0,3):
        problem = PROBLEMS[i] 
        for weight in [2,3,4,5]:
          #you can write code in here if you like
          pass

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  
  
  find_result = False
  find_better_result = False
  stats = None
  
  # initial cost bound
  cost_bound = (float("inf"), float("inf"), float("inf"))
  # initial time
  initial_time = os.times()[0]
  time_last = timebound
  
  # Run searchEngine
  se = SearchEngine('custom', 'full')
  se.init_search(initial_state, 
                 sokoban_goal_state, 
                 heur_fn, 
                 lambda sN: fval_function(sN, weight))
  find_result, stats = se.search(time_last, cost_bound)
  
  # use to reset the cost_bound
  cost_count = float("inf")
  
  # make sure not exceeding the time
  time_last = timebound - (os.times()[0] - initial_time)
  
  # if find result
  if find_result : 
    cost_count = find_result.gval + heur_fn(find_result)
    cost_bound = (float("inf"),float("inf"),cost_count)
    
  # didnt find result     
  else:
    return False
  
  # initialize the best result we have found so far  
  best_result_found = find_result

  # Rerun searchEngin if frontier is not empty and also we still have time 
  while not se.open.empty() and time_last > 0 :
      find_better_result, stats = se.search(time_last, cost_bound)
      time_last = timebound - (os.times()[0] + initial_time)
      
      # if find better result
      if find_better_result :
          cost_count = find_better_result.gval + heur_fn(find_better_result)
          
          # Renew the best result we have found so far
          best_result_found = find_better_result
               
      # didnt find better result
      else:
        
        # change the weight and try to rerun it
        # I dont want my weight goes under 1
        weight *= 0.8
  
  return best_result_found

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of anytime greedy best-first search'''
  
  find_result = False
  find_better_result = False
  
  # initial time
  initial_time = os.times()[0]
  time_last = timebound
  
  # Run searchEngine
  se = SearchEngine('best_first', 'default')
  se.init_search(initial_state, 
                 sokoban_goal_state, 
                 heur_fn)

  # use to reset the cost_bound
  cost_count = float("inf")
  
  # initial cost bound
  cost_bound = (float("inf"), float("inf"), float("inf"))
  find_result, stats = se.search(time_last, cost_bound)
  time_last = timebound - (os.times()[0] - initial_time)
  
  # if find result
  if find_result : 
    cost_count = find_result.gval
    cost_bound = (cost_count,float("inf"),float("inf"))
  
  # didnt find result
  else :
    return False
  
  # initialize the best result we have found so far  
  best_result_found = find_result
      
  # Rerun searchEngin if frontier is not empty and also we still have time 
  while not se.open.empty() and time_last > 0 :
      find_better_result, stats = se.search(time_last, cost_bound)
      time_last = timebound - (os.times()[0] + initial_time)
      
      # if find better result
      if find_better_result :
          cost_count = find_better_result.gval
          
          # Renew the best result we have found so far
          best_result_found = find_better_result
          
      # didnt find better result
      else :
        continue
        
  return best_result_found


