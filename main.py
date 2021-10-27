import networkx as nx
import json
import os
import itertools
import inquirer

from pairModule.teamNetwork import convertPeopleToGraph, convertPreviousPairsToGraphWeights, weightHomeWorkers
from pairModule.fileHandling import getPeople, getPreviousPairs


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


if __name__ == "__main__":
    main()
