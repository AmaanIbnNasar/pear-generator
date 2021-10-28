import inquirer
import os

from pairModule.fileHandling import getPeople, getPreviousPairs, savePairings, getMostRecentPairs
from pairModule.peopleGraph import doFullPairing, printPairings


def pairTeamAndAskWhich():
    team_answers = inquirer.prompt([
        inquirer.List(
            'team',
            message="What team do you want to pear?",
            choices=os.listdir('./__pairfiles__')
        )
    ])
    pairTeam(team_answers["team"])


def pairAllTeams():
    for team in os.listdir('./__pairfiles__'):
        print(f'PAIRING TEAM: {team}\n')
        pairTeam(team)
    # TODO: print all pairings at the end


def pairTeam(team):
    people = getPeople(team)
    previousPairSets = getPreviousPairs(team)

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

    pairings = doFullPairing(people, previousPairSets, peopleLocation)

    unpaired = set(people)
    printPairings(pairings, [*unpaired, *exclusion_answers['excluded']])

    save_answers = inquirer.prompt([
        inquirer.Confirm(
            'save',
            message='Would you like to save this pairing in previous pairs?',
            default=True
        )
    ])
    if save_answers['save']:
        savePairings(team, pairings, unpaired)

def printAllPairings():
    for team in os.listdir('./__pairfiles__'):
        teamPairings = getMostRecentPairs(team)
        apples = getPeople(team)
        teamPairings = {
            p1: p2
            for p1, p2 in teamPairings.items()
            if p2!=0
        }
        for (p1, p2) in teamPairings.items():
            apples.remove(p1)
            apples.remove(p2)
        printPairings(teamPairings.items(), apples)

