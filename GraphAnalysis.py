# author: Jacob Schlaerth
# date: 26 July 2020
# course: CS 325 Analysis of Algorithms
# Homework 4

class Wrestler:
    def __init__(self, id):
        self.id = id
        self.team = None

    def __repr__(self):
        return str(self.id)

def ret_by_id(id):
    for w in wrestler_list:
        if w.id == id:
            return w


wrestler_list = []
graph = dict()
user_file = input("Please enter the filename you wish to analyze (include filetype)  >")

with open(user_file, 'r') as infile:
    # iterate through each line
    for line in infile:
        wrestler_list.append(line.strip().split(" "))

    # first entry is number of wrestlers
    number_of_wrestlers = int(wrestler_list[0][0])
    del wrestler_list[0]
    # split the data.txt into the wrestlers and the rivalry pairs
    rivalries = wrestler_list[number_of_wrestlers+1:]
    wrestler_list = [Wrestler(x[0]) for x in wrestler_list[:number_of_wrestlers]]

    # format graph
    # init each dict value as empty set
    for wrestler in wrestler_list:
        graph[wrestler] = set()

    # for each rivalry, add the rival to that wrestler's set
    # since rivalries go both ways, add add each rival to each value
    for riv in rivalries:
        graph[ret_by_id(riv[0])].add(ret_by_id(riv[1]))
        graph[ret_by_id(riv[1])].add(ret_by_id(riv[0]))


def rivals_algo(graph):
    """
    determines whether teams such that each rival is on the opposite team
    :param graph: dictionary containing each wrestler's rivals
    :return: False if impossible, team lists if possible
    """
    bag = set()
    wrestlers = graph.keys()
    team_babyface = set()
    team_heel = set()

    done = False
    while not done: # while there are unclassified nodes / wrestlers without a team
        unclassified = [w for w in wrestlers if w.team is None]
        if len(unclassified) != 0:
            arb_wrestler = next(iter(unclassified))
            arb_wrestler.team = "Babyface"
            for adj in graph[arb_wrestler]:
                if adj.team is None:
                    bag.add(adj)
        if len(unclassified) == 0:
            done = True
            break

    # while bag is not empty
        while len(bag) != 0:
            current = bag.pop()
            current_rivals = graph[current]
            rivalBB, rivalHeel = False, False
            for rival in current_rivals:
                if rival.team == "Babyface":
                    rivalBB = True
                if rival.team == "Heel":
                    rivalHeel = True
            if rivalBB and rivalHeel: # if current has a rival on each team, this is impossible
                print("Impossible")
                return

            if rivalBB:
                current.team = "Heel"
            if rivalHeel:
                current.team = "Babyface"
            # add all unclassified nodes adjacent to current to bag
            for r in current_rivals:
                if r.team is None:
                    bag.add(r)

    # if we are here, all nodes are classified
    for w in wrestlers:
        if w.team == "Babyface":
            team_babyface.add(w)
        if w.team == "Heel":
            team_heel.add(w)
    print("Yes Possible")
    print("Team Babyface:", team_babyface)
    print("Team Heel:", team_heel)
    return


rivals_algo(graph)