#!/usr/bin/env python3

import game, queue


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
