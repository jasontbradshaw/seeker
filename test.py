#!/usr/bin/env python2

import seeker

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

    # do actual searching
    s = seeker.Seeker(succ, heur)

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
    # profile code
    import cProfile
    import pstats

    pname = "search_prof"

    # get statistics
    cProfile.run("main()", pname)
    p = pstats.Stats(pname)

    p = p.strip_dirs()
    p.sort_stats("calls").print_stats()
