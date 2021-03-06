import os
import inquirer

from pairModule.fileHandling import archiveTeam

def generateTeam():
    team_answers = inquirer.prompt([
        inquirer.Text(
            'team',
            message='What team name do you want to add?'
        )
    ])

    os.mkdir(f"./__pairfiles__/{team_answers['team']}")
    with open(f"./__pairfiles__/{team_answers['team']}/people.txt", "w") as f:
        f.write("")
    with open(f"./__pairfiles__/{team_answers['team']}/previous_pears.json", "w") as f:
        f.write("[]")

    print('\nYour new team has been prepared!\n\n'
          f'You will need to set up the /__pairfiles/{team_answers["team"]}/people.txt file '
          "with the list of people on the team, refer to README.md on how to do this.")

def archiveTeamAndAskWhich():
    team_answers = inquirer.prompt([
        inquirer.List(
            'team',
            message="What team do you want to archive?",
            choices=os.listdir('./__pairfiles__')
        )
    ])
    archiveTeam(team_answers["team"])
