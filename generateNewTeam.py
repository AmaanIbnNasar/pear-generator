import os, inquirer

def main():
    team_answers = inquirer.prompt([
        inquirer.Text(
            'team',
            message='What team name do you want to add?'
        )
    ])

    os.mkdir(f"./__pairfiles__/{team_answers['team']}")
    with open (f"./__pairfiles__/{team_answers['team']}/people.txt", "w") as f:
        f.write("")
    with open (f"./__pairfiles__/{team_answers['team']}/previous_pears.JSON", "w") as f:
        f.write("[]")


if __name__ == "__main__":
    main()