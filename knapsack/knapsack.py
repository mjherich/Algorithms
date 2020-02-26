#!/usr/bin/python

import sys, pdb
from collections import namedtuple

Item = namedtuple('Item', ['index', 'size', 'value'])

class Knapsack:
  # Invoking Knapsack without arguments should create an empty Knapsack of cost and value 0
  def __init__(self, items=[], value=0, cost=0):
    self.items = items
    self.value = value
    self.cost = cost


def knapsack_solver(items, capacity):
  """
  Uses dynamic programming to iteratively builds a grid of smaller subproblems.
     1, 2, 3, 4, 5, 6, 7   <- COST  
  [ [*, *, *, *, *, *, *], 👇 ITEMS 
    [*, *, *, *, *, *, *],
    [*, *, *, *, *, *, *],
    [*, *, *, *, *, *, *] ]

  Returns the Item indicies to select, the total value and total cost
  ex: Items to select: 2, 8, 10
      Total cost: 98
      Total value: 117
  """
  # === Create dynamic grid ===
  # Each grid element represents a Knapsack that maximizes the value for the given cost.
  # n: Number of items to choose from (rows)
  n = len(items)
  # m: Item cost breakpoints, continuous integer breakpoints from 1 to max capacity (columns)
  m = capacity
  # Initilize subproblem grid with empty Knapsacks (subproblems[item_idx][knapsack_capacity])
  subproblems = [[Knapsack()] * m] * n

  # Update first row with first item solution
  first_item = items[0]
  first_item_value = first_item.value
  first_item_cost = first_item.size
  for knapsack_capacity in range(1, m):
    if first_item_cost <= knapsack_capacity:
      subproblems[0][knapsack_capacity] = Knapsack([first_item], first_item_value, first_item_cost)

  # === Start building subproblems grid with solutions ===
  # Loop over each subsequent subproblem and find max value given the cost (m)
  for item_idx in range(1, n):
    cur_item = items[item_idx]
    cur_item_cost = cur_item.size
    cur_item_value = cur_item.value
    for knapsack_capacity in range(1, m):
      knapsack_items = []
      knapsack_value = 0
      knapsack_cost = 0
      # Check if the item is small enough to fit in the knapsack
      if cur_item_cost <= knapsack_capacity:
        knapsack_items += [cur_item]
        knapsack_value += cur_item_value
        knapsack_cost += cur_item_cost
        left_over_cost = knapsack_capacity - knapsack_cost
        # If there is left over cost...
        if left_over_cost > 0:
          # what item(s) can fit in the left over space that maximizes the value
          left_over_knapsack_maxed = subproblems[item_idx-1][left_over_cost] # Returns instance of Knapsack
          # Update knapsack value to include the left_over_knapsack value
          knapsack_value += left_over_knapsack_maxed.value
          # Add left_over_knapsack items to knapsack_items
          knapsack_items.extend(left_over_knapsack_maxed.items)
          # Update cost
          knapsack_cost += left_over_knapsack_maxed.cost

        # Save new Knapsack to subproblems grid
        subproblems[item_idx][knapsack_capacity] = Knapsack(knapsack_items, knapsack_value, knapsack_cost)
      else:
        # Item doesn't fit in this subproblem, use previously found max solution
        subproblems[item_idx][knapsack_capacity] = subproblems[item_idx-1][knapsack_capacity]

  ret = {
    "Value": sum([item.value for item in subproblems[-1][-1].items]),
    "Chosen": [item.index for item in subproblems[-1][-1].items]
  }
  return ret
  

if __name__ == '__main__':
  if len(sys.argv) > 1:
    capacity = int(sys.argv[2])
    file_location = sys.argv[1].strip()
    file_contents = open(file_location, 'r')
    items = []

    for line in file_contents.readlines():
      data = line.rstrip().split()
      items.append(Item(int(data[0]), int(data[1]), int(data[2])))
    
    file_contents.close()

    # print(items[0].index, items[0].size, items[0].value)
    print(knapsack_solver(items, capacity))
  else:
    print('Usage: knapsack.py [filename] [capacity]')