import json


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
