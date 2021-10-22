import networkx, json

def getPeople():
    with open("./__pairfiles__/people.json") as f:
        people = json.load(f)
    return people

def getPreviousPairs():
    with open("./__pairfiles__/previous_pears.JSON") as f:
        previousPairs = json.load(f)
    return previousPairs

def main():
    people = getPeople()
    previousPairs = getPreviousPairs()
    


if __name__=="__main__":
    main()