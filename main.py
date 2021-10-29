import inquirer

from pairModule.fileProcesses import generateTeam, archiveTeamAndAskWhich
from pairModule.pairingProcesses import pairAllTeams, pairTeamAndAskWhich, printAllPairings


def main():
    main_answers = inquirer.prompt([
        inquirer.List(
            'main',
            message="Which of the following would you like to do?",
            choices=[
                ('Pair a single team', 'pair_team'),
                ('Pair all teams in __pairfiles__', 'pair_all_teams'),
                ('Print the most recent pairing of all teams in a big combined message', 'big_message'),
                ('Generate a new team', 'generate_team'),
                ('Archive a current team', 'archive_team')
            ]
        )
    ])
    print()

    if main_answers['main'] == 'pair_team':
        pairTeamAndAskWhich()
    elif main_answers['main'] == 'pair_all_teams':
        pairAllTeams()
    elif main_answers['main'] == 'big_message':
        printAllPairings()  
    elif main_answers['main'] == 'generate_team':
        generateTeam()
    elif main_answers['main'] == 'archive_team':
        archiveTeamAndAskWhich()


if __name__ == "__main__":
    main()
