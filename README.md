# Pairing Generator

## Setup

To install the dependencies to the project please run `pip install -r requirements.txt`

Run `python main.py` to start

If you'd like to add a new team:

- Add a directory of the team name into **pair**files
- Add a people.json file and a previous_pears.JSON file

THE FILE MUST BE PEARS NOT PAIRS

Or you can run `python generateNewTeam.py`

## How the algorithm works

A team is represented as a fully connected graph.
This means each person is a node and all people have links between them.
Imagine there are three people (A, B, C), this would look like so:

```
A -------- B
  \       /
   \     /
    \   /
      C
```

Each edge has a `weight`, representing how good the connection is, for instance:

```
    100
A -------- B
  \       /
25 \     / 250
    \   /
      C
```

In this diagram, the connection between B and C is the best. The algorithm will try to find the optimal matching. The optimal matching always matches the maximum number of people possible, and maximizes the total sum weight of all the matches. In the example network above, the algorithm would output the pairing `{(B, C)}`.

This weight is calculated according to the following process:

1. All weights start at 100

2. The `previousPairings` are iterated over, and if person `p1` and `p2` have been in a pair on `previousPairing i` (where `i=0` is the most recent previous pairing and `i=1` is the pairing the week before, etc...) then the weight of the connection between the two people is multiplied by `0.5 - 0.5**(i+1)`

   - This means that if `p1` and `p2` were paired the previous week then the `weight` goes to 0 for that connection

   - The sequence `0.5 - 0.5**(i+1)` has values `0, 0.25, 0.375, 0.4375, ...`. In this way a previous pairing becomes less and less penalized as time goes on. As `i` goes to infinity this sequence goes to `0.5`, people who have never been paired

   - The penalty is applied multiple times if people have been paired multiple times, if `p1` and `p2` were paired on pairings `i=1` and `i=2`, their final weight at the end of this step is `100 * 0.25 * 0.375`.

   - The motivation of this step is to penalize connections between those who have been paired previously; to penalize more recent pairings more than older pairings; and to penalize a pair more and more each additional time that they are paired. In this way people are paired with those whom they have never worked with less and less recently.

3. If someone was unpaired in any pairing because the algorithm couldn't match them (not because they were excluded) then the algorithm will add `+15` to all their connections for each time they were unpaired.

   - The motivation of this is to prioritize pairing people who were left unpaired in previous rounds.

4. Finally, `+150` is added to all connections where the two people on the connection are in the same location.

   - The motivation of this is to make sure that people are preferentially matched to others working in the same location, above any other criteria.

   - For example, if only two people were working from home, the algorithm would match them two together repeatedly even if there were people at the office with whom they'd never worked.
