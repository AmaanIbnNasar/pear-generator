import json
import shutil


def getPeople(team):
    with open(f"__pairfiles__/{team}/people.txt") as f:
        people = f.read().strip().split("\n")
        people = [
            person.strip()  # Strip leading/trailing spaces in a person's name
            for person in people
            if person.strip()  # Drop names that are accidental newlines
        ]
    return people


def getPreviousPairObjs(team):
    with open(f"__pairfiles__/{team}/previous_pears.json") as f:
        previousPairObjs = json.load(f)
    return previousPairObjs


def getMostRecentPairObj(team):
    pairObjs = getPreviousPairObjs(team)
    if len(pairObjs) != 0:
        return pairObjs[0]
    else:
        return []


def savePairings(team, name, pairings, excluded, unpaired, location, *, overwrite_most_recent=False):
    previousPairObjs = getPreviousPairObjs(team)
    if overwrite_most_recent:
        del previousPairObjs[0]
    previousPairObjs.insert(0, {
        "name": name,
        "pairings": pairings,
        "location": location,
        "excluded": excluded,
        "unpaired": unpaired
    })
    with open(f"__pairfiles__/{team}/previous_pears.json", 'w') as f:
        json.dump(previousPairObjs, f, indent=2)


def archiveTeam(team):
    shutil.move("./__pairfiles__/"+team, "./archivedTeams/"+team)
    print(team + " has been archived")
