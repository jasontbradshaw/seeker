import util

class Seeker(object):
    """
    A class that returns shortest paths using the A* algorithm.
    """

    def __init__(self, successors_func, heuristic_func = None):
        """
        Sets up the seeker with successor ane heuristic functions that are
        used in the search method.  If the user doesn't provide a heuristic
        function, the null heuristic (always returns 0) is used instead.
        """

        # initialize internal functions to those provided by user
        self.successors = successors_func

        # override default null heuristic if user supplied one
        if heuristic_func is not None:
            self.heuristic = heuristic_func

    def heuristic(self, state, goal):
        """
        Evaluates a state and returns an approximation of its distance to
        the goal.  Numbers closer to zero are better, and further from
        zero are worse.  Must return a number greater than or equal to
        zero.  If the search is to be guaranteed complete, the heuristic
        must be admissible, ie. it should never overestimate the cost to
        get to the goal from the current state.
        """

        # null heuristic be default, should be overridden by the user
        return 0

    def successors(self, state):
        """
        Given a state, return all its possible (successor, action, cost)
        tuples.
        """

        raise NotImplementedError("User must supply a successor function.")

    def search(self, start, goal):
        """
        Calculate the shortest path from the given start state to the given
        goal state.  Returns a list of actions representing that path, or
        'None' if no path was found.
        """

        # priorty queue keeps items in form (priority, data)
        frontier = util.PriorityQueue()

        # paths from start to a given node, list of (action, total_cost)
        paths = {}
        paths[start] = [(None, 0)] # start node always has an empty path from 'start'

        # already expored nodes
        explored = set([])

        # put the starting node into the frontier along with an 'f' value
        # of zero.  'f' doesn't matter initially since start node is always
        # the only one in the queue to begin with and is immediately popped
        frontier.put(start, 0)

        # loop until we've found a solution, or are out of nodes to check
        while not frontier.empty():

            # expand the 'best looking' node (originally the start node)
            node = frontier.get()

            # return the solution if we found it
            if node == goal:
                # return only the actions, not the costs in the path
                final_path = map(lambda n: n[0], paths[node])

                # remove the initial 'None' action that gets us to 'start'
                final_path = final_path[1:]

                return final_path

            # add node to set of explored nodes to prevent loops
            explored.add(node)

            # add this node's children to the frontier
            for child, action, cost in self.successors(node):
                # don't re-add an already explored node
                if child not in explored and child not in frontier:
                    # update path to get to this child from start state by
                    # appending 'action' to path to get to the parent node
                    child_path = list(paths[node]) # make a copy

                    # keep a running total of path cost for the children;
                    # cost is a tally and latest is in last item of path
                    g = cost + paths[node][-1][1]

                    child_path.append( (action, g) )
                    paths[child] = child_path

                    # add the child with its 'f' value
                    f = g + self.heuristic(child, goal)
                    frontier.put(child, f)

        # couldn't find a solution
        return None
