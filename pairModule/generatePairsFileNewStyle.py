import json

from pairModule.fileHandling import getPreviousPairObjs


def generatePairsFileNewStyle(team):
    # Load old pairs file
    previousPairSetsOldStyle = getPreviousPairObjs(team)

    # Convert format
    previousPairSetsNewStyle = [
        {
            "name": "< Unnamed >",
            "pairings": {
                p1: p2
                for p1, p2 in previousPairSet.items()
                if p2 != 0
            },
            "location": {},
            "excluded": [
                p1
                for p1, p2 in previousPairSet.items()
                if p2 == 0
            ],
            "unpaired": []
        }
        for previousPairSet in previousPairSetsOldStyle
    ]

    with open(f'./__pairfiles__/{team}/previous_pairs_NEW.json', 'w') as f:
        json.dump(previousPairSetsNewStyle, f, indent=2)
