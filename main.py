import networkx as nx, json, os, itertools
import inquirer

def getPeople(team):
    with open(f"__pairfiles__/{team}/people.json") as f:
        people = json.load(f)
    return people["people"]

def getPreviousPairs(team):
    with open(f"__pairfiles__/{team}/previous_pears.JSON") as f:
        previousPairWeeks = json.load(f)
    return previousPairWeeks

def savePairings(team, pairings, unpaired):
    with open(f"__pairfiles__/{team}/previous_pears.JSON") as f:
        previousPairWeeks = json.load(f)
    previousPairWeeks.insert(0, {
        **{
            p1: p2
            for p1, p2 in pairings
        },
        **{
            person: 0
            for person in unpaired
        }
    })
    with open(f"__pairfiles__/{team}/previous_pears.JSON", 'w') as f:
        json.dump(previousPairWeeks, f)

def convertPeopleToGraph(people):
    peopleGraph = nx.Graph()
    peopleEdges = itertools.combinations(people, 2)
    peopleGraph.add_edges_from(peopleEdges, weight=100)
    return peopleGraph

def convertPreviousPairsToGraphWeights(peopleGraph, previousPairWeeks):
    unmatchedPeople = []  # can include repeats
    # First apply the penalties for being matched previously
    for i, previousPairWeek in enumerate(previousPairWeeks):
        for p1, p2 in previousPairWeek.items():
            if p1 in peopleGraph.nodes and p2 == 0:
                unmatchedPeople.append(p1)
                continue
            if p1 not in peopleGraph.nodes or p2 not in peopleGraph.nodes:
                continue
            peopleGraph.edges[p1, p2]["weight"] *= 0.5 - 0.5**(i+1)
    
    # Then add the boost for being unpaired
    for unmatchedPerson in unmatchedPeople:
        for neighbor in peopleGraph.neighbors(unmatchedPerson):
            peopleGraph.edges[unmatchedPerson, neighbor]["weight"] += 15


def weightHomeWorkers(peopleGraph, people, peopleLocation):
    for p1, p2 in itertools.combinations(people, 2):
        if peopleLocation[p1] == peopleLocation[p2]:
            peopleGraph.edges[p1, p2]["weight"] += 150


def plotGraph(graph):
    import matplotlib.pyplot as plt
    pos = nx.drawing.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos, width=[edge[2]/100 for edge in graph.edges.data("weight")])
    nx.draw_networkx_labels(graph, pos)
    plt.show()

def main():
    team_answers = inquirer.prompt([
        inquirer.List(
            'team',
            message="What team do you want to pear?",
            choices=os.listdir('./__pairfiles__') + ["Get all teams"]
        )
    ])
    if team_answers["team"] == "Get all teams":
        for team in os.listdir("./__pairfiles__"):
            print(f"Processing team: {team}")
            processTeam(team)
    else:
        processTeam(team_answers["team"])


def processTeam(team):
    people = getPeople(team)
    previousPairWeeks = getPreviousPairs(team)

    wfh_answers = inquirer.prompt([
        inquirer.Checkbox(
            'homeworkers',
            message='Who is working from home?',
            choices=people
        )
    ])
    peopleLocation = {
        person: 'home' if person in wfh_answers['homeworkers'] else 'office'
        for person in people
    }

    exclusion_answers = inquirer.prompt([
        inquirer.Checkbox(
            'excluded',
            message='Who do you want to exclude from pairing?',
            choices=people
        )
    ])
    people = [
        person
        for person in people
        if person not in exclusion_answers['excluded']
    ]

    peopleGraph = convertPeopleToGraph(people)
    convertPreviousPairsToGraphWeights(peopleGraph, previousPairWeeks)
    weightHomeWorkers(peopleGraph, people, peopleLocation)

    # for neigh in peopleGraph.neighbors('Amaan Ibn-Nasar'):
    #     print(neigh, peopleGraph.edges['Amaan Ibn-Nasar', neigh]['weight'])

    pairings = nx.max_weight_matching(peopleGraph, maxcardinality=True)

    unpaired = set(people)
    for (p1, p2) in pairings:
        unpaired.remove(p1)
        unpaired.remove(p2)
        print(f":pear: {p1} :pear: {p2} :pear:")
    for person in unpaired:
        print(f":apple: {person} :apple:")
    for person in exclusion_answers['excluded']:
        print(f":apple: {person} :apple:")

    # plotGraph(peopleGraph)

    print()

    save_answers = inquirer.prompt([
        inquirer.Confirm(
            'save',
            message='Would you like to save this pairing in previous pairs?',
            default=True
        )
    ])
    if save_answers['save']:
        savePairings(team, pairings, unpaired)


if __name__=="__main__":
    main()