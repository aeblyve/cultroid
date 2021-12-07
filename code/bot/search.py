#!/usr/bin/env python3

import game, queue, heapq


# class SearchNode:
#     def __init__(self, state, cost, path):
#         self.state = state
#         self.cost = cost
#         self.path = path


def breadth_first_search(game):

    frontier = queue.SimpleQueue()
    explored = set()

    start_node = (game.get_start_state(), 0, [])

    frontier.put(start_node)

    while not frontier.empty():
        current_state, current_cost, current_path = frontier.get()
        explored.add(current_state)
        print(current_state)
        if game.is_goal(current_state):
            return current_path

        for new_state, new_action, action_cost in game.get_successors(current_state):
            new_node = (
                new_state,
                current_cost + action_cost,
                current_path + [new_action],
            )

            if new_state not in explored:
                frontier.put(new_node)

    # no path found
    return []

def Astar_search(game, heurisitic):

    frontier = PriorityQueue()
    explored = set()

    start_node = (game.get_start_state(), 0, [])

    frontier.push(start_node, 0)
    #counter = 0

    while not frontier.empty():
        #counter = counter + 1
        current_state, current_cost, current_path = frontier.pop()

        #explored.add((current_state.piece, current_state.grid))
        explored.add(current_state)
        #if counter % 100 == 0:
        #    print(str(explored))
        #print(str(current_state))
        if game.is_goal(current_state):
            return current_path

        for new_state, new_action, action_cost in game.get_successors(current_state):
            new_node = (
                new_state,
                current_cost + action_cost,
                current_path + [new_action],
            )

            if new_state not in explored:
                frontier.update(new_node, new_node[1] + heurisitic(new_node[0]))

    # no path found
    return []

#code from CS188 Berkeley for PriorityQueue with update function modified
class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def empty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i[0] == item[0]:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

from game import CheeseGame
Astar_search(CheeseGame(), lambda a: 0)