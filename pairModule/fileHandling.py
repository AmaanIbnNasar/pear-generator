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


def getPreviousPairs(team):
    with open(f"__pairfiles__/{team}/previous_pears.json") as f:
        previousPairSets = json.load(f)
    return previousPairSets

def getMostRecentPairs(team):
    pairs = getPreviousPairs(team)
    if len(pairs) != 0:
        return pairs[0]
    else:
        return []


def savePairings(team, pairings, unpaired):
    with open(f"__pairfiles__/{team}/previous_pears.json") as f:
        previousPairSets = json.load(f)
    previousPairSets.insert(0, {
        **{
            p1: p2
            for p1, p2 in pairings
        },
        **{
            person: 0
            for person in unpaired
        }
    })
    with open(f"__pairfiles__/{team}/previous_pears.json", 'w') as f:
        json.dump(previousPairSets, f, indent=2)

def archiveTeam(team):
    shutil.move("./__pairfiles__/"+team, "./archivedTeams/"+team)
    print(team + " has been archived")