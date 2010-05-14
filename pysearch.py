import Queue

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
        frontier = Queue.PriorityQueue()
        
        # paths from start to a given node, list of (action, total_cost)
        paths = {}
        paths[start] = [(None, 0)] # start node always has an empty path from 'start'
        
        # already expored nodes
        explored_set = set([])
        
        # set of nodes in the frontier (memory inefficient, but faster)
        frontier_set = set([])
        
        # put the starting node into the frontier along with an 'f' value
        # of zero.  'f' doesn't matter initially since start node is always
        # the only one in the queue to begin with and is immediately popped
        frontier.put( (0, start) )
        
        # loop until we've found a solution, or are out of nodes to check
        while not frontier.empty():
            
            # expand the 'best looking' node (originally the start node)
            node = frontier.get_nowait()[1]
            
            # return the solution if we found it
            if node == goal:
                # return only the actions, not the costs in the path
                final_path = map(lambda n: n[0], paths[node])
                
                # remove the initial 'None' action that gets us to 'start'
                final_path = final_path[1:]
                
                return final_path
            
            # add node to set of explored nodes to prevent loops
            explored_set.add(node)
            
            # add this node's children to the frontier
            for child, action, cost in self.successors(node):
                # don't re-add an already explored node
                if child not in explored_set and child not in frontier_set:
                    # update path to get to this child from start state by
                    # appending 'action' to path to get to the parent node
                    child_path = list(paths[node]) # make a copy
                    
                    # keep a running total of path cost for the children
                    # (cost of last item in path)
                    g = cost + paths[node][-1][1]
                    
                    child_path.append( (action, g) )
                    paths[child] = child_path
                    
                    # add the child with its 'f' value
                    f = g + self.heuristic(child, goal)
                    frontier.put( (f, child) )

                    frontier_set.add(child)
                
        # couldn't find a solution
        return None

def main():
    def succ(state):
        """
        'state' is the all-lowercase 3-letter prefix of the city name.
        """
        
        romania = {}
        
        # connected cities by name
        romania["ora"] = [ ("zer", "zer", 71), ("sib", "sib", 151) ]
        romania["zer"] = [ ("ora", "ora", 71), ("ara", "ara", 75) ]
        romania["ara"] = [ ("zer", "zer", 75), ("sib", "sib", 140),
                           ("tim", "tim", 118) ]
        romania["tim"] = [ ("ara", "ara", 118), ("lug", "lug", 111) ]
        romania["lug"] = [ ("tim", "tim", 111), ("meh", "meh", 70) ]
        romania["meh"] = [ ("lug", "lug", 70), ("dro", "dro", 75) ]
        romania["dro"] = [ ("meh", "meh", 75), ("cra", "cra", 120) ]
        romania["sib"] = [ ("ora", "ora", 151), ("ara", "ara", 140),
                           ("fag", "fag", 99), ("rim", "rim", 80) ]
        romania["rim"] = [ ("sib", "sib", 80), ("cra", "cra", 146),
                           ("pit", "pit", 97) ]
        romania["cra"] = [ ("dro", "dro", 120), ("rim", "rim", 146),
                           ("pit", "pit", 138) ]
        romania["fag"] = [ ("sib", "sib", 99), ("buc", "buc", 211) ]
        romania["pit"] = [ ("rim", "rim", 97), ("cra", "cra", 138),
                           ("buc", "buc", 101) ]
        romania["giu"] = [ ("buc", "buc", 90) ]
        romania["buc"] = [ ("giu", "giu", 90), ("pit", "pit", 101),
                           ("fag", "fag", 211), ("urz", "urz", 85) ]
        romania["urz"] = [ ("buc", "buc", 85), ("vas", "vas", 142),
                           ("hir", "hir", 98) ]
        romania["hir"] = [ ("urz", "urz", 98), ("efo", "efo", 86) ]
        romania["efo"] = [ ("hir", "hir", 86) ]
        romania["vas"] = [ ("urz", "urz", 142), ("ias", "ias", 92) ]
        romania["ias"] = [ ("vas", "vas", 92), ("nea", "nea", 87) ]
        romania["nea"] = [ ("ias", "ias", 87) ]
        
        return romania[state]
    
    def heur(state, goal):
        """
        Smaller distance between cities, 10% times number of in-between
        cities
        """
        
        return 0
    
    s = Seeker(succ, heur)
    
    import itertools

    romania = [ "ora", "zer", "ara", "tim", "lug", "meh", "dro", "sib", "rim",
                "cra", "fag", "pit", "giu", "buc", "urz", "hir", "efo", "vas",
                "ias", "nea" ]
    
    perms = []
    for pair in itertools.permutations(romania, 2):
        perms.append(pair)
        
    # unique_perms = []
    # for pair in perms:
    #     if pair[0] > pair[1]:
    #         pair = pair[1], pair[0]
    #     if pair not in unique_perms:
    #         unique_perms.append(pair)
            
    for city in perms:
        s.search(city[0], city[1])

if __name__ == "__main__":
    #main()
    
    # profile code
    import cProfile
    import pstats
    
    pname = "search_prof"
    
    # get statistics
    cProfile.run("main()", pname)
    p = pstats.Stats(pname)
    
    p = p.strip_dirs()
    p.sort_stats("calls").print_stats()
