import inquirer
import os
from datetime import datetime

from pairModule.fileHandling import getPeople, getPreviousPairObjs, savePairings, getMostRecentPairObj
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
    previousPairObjs = getPreviousPairObjs(team)

    lastPairing = previousPairObjs[0] if len(previousPairObjs) else None

    if lastPairing:
        print(f'Last pairing name: "{lastPairing["name"]}"\n')
        printPairings(lastPairing["pairings"],
                      [*lastPairing["unpaired"], *lastPairing["excluded"]])

        redo_answer = inquirer.prompt([
            inquirer.Confirm(
                'redo',
                message='Would you like to ignore and redo the last pairing (displayed above)?',
                default=False
            )
        ])['redo']

        print(
            "\nThe last pairing will be used to set defaults for the upcoming questions.\n")
    else:
        redo_answer = False
        print("No previous pairings found.\n")

    if lastPairing:
        preselected_wfh_people = []
        unpreselected_wfh_people = []
        for person in people:
            if lastPairing["location"].get(person, None) == "home":
                preselected_wfh_people.append(person)
            else:
                unpreselected_wfh_people.append(person)
    else:
        preselected_wfh_people = []
        unpreselected_wfh_people = people

    wfh_answer = inquirer.prompt([
        inquirer.Checkbox(
            'homeworkers',
            message='Who is working from home?',
            choices=preselected_wfh_people + unpreselected_wfh_people,
            default=preselected_wfh_people
        )
    ])['homeworkers']
    peopleLocation = {
        person: 'home' if person in wfh_answer else 'office'
        for person in people
    }

    if lastPairing:
        preselected_excluded_people = lastPairing["excluded"]
        unpreselected_excluded_people = [
            person
            for person in people
            if person not in preselected_excluded_people
        ]
    else:
        preselected_excluded_people = []
        unpreselected_excluded_people = people

    exclusion_answer = inquirer.prompt([
        inquirer.Checkbox(
            'excluded',
            message='Who do you want to exclude from pairing?',
            choices=preselected_excluded_people + unpreselected_excluded_people,
            default=preselected_excluded_people
        )
    ])['excluded']
    people = [
        person
        for person in people
        if person not in exclusion_answer
    ]

    pairObjsToGive = previousPairObjs[1:] if redo_answer else previousPairObjs
    pairings, unpaired = doFullPairing(
        people, pairObjsToGive, peopleLocation)

    print("GENERATED PAIRING\n"
          "-----------------\n")

    printPairings(pairings, [*unpaired, *exclusion_answer])

    save_answer = inquirer.prompt([
        inquirer.Confirm(
            'save',
            message='Would you like to save this pairing in previous pairs?',
            default=True
        )
    ])['save']
    if save_answer:
        if redo_answer:
            overwrite_answer = inquirer.prompt([
                inquirer.Confirm(
                    'overwrite',
                    message="Do you want to overwrite the last pairing?",
                    default=True
                )
            ])['overwrite']
        else:
            overwrite_answer = False
        pairObjName = datetime.now().strftime("%c")
        print(f'This pairing will have name "{pairObjName}"')
        savePairings(team, pairObjName, pairings,
                     exclusion_answer, unpaired, peopleLocation, overwrite_most_recent=overwrite_answer)


def printAllPairings():
    for team in os.listdir('./__pairfiles__'):
        teamPairingObj = getMostRecentPairObj(team)
        printPairings(teamPairingObj["pairings"], [
                      *teamPairingObj["unpaired"], *teamPairingObj["excluded"]])
