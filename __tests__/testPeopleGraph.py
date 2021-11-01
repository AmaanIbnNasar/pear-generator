from unittest import TestCase

from pairModule.peopleGraph import applyPreviousPairWeightDiscount, applySameLocationBoost, applyUnpairedWeightBoost, convertPeopleToGraph, doFullPairing


class TestConvertPeopleToGraph(TestCase):
    def test_creates_all_edges(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3, 4])
        self.assertEqual(list(peopleGraph.edges()),
                         [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])

    def test_gives_correct_initial_weight(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3])
        self.assertEqual(list(peopleGraph.edges.data("weight")),
                         [(1, 2, 100), (1, 3, 100), (2, 3, 100)])


class TestPreviousPairWeightDiscount(TestCase):
    def test_no_pairings_does_not_alter_weights(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3])
        applyPreviousPairWeightDiscount(peopleGraph, [])
        self.assertEqual(list(peopleGraph.edges.data("weight")),
                         [(1, 2, 100), (1, 3, 100), (2, 3, 100)])
        applyPreviousPairWeightDiscount(peopleGraph, [{"pairings": {}}])
        self.assertEqual(list(peopleGraph.edges.data("weight")),
                         [(1, 2, 100), (1, 3, 100), (2, 3, 100)])

    def test_paired_last_time_discount(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3])
        applyPreviousPairWeightDiscount(peopleGraph, [{"pairings": {1: 2}}])
        self.assertEqual(0, peopleGraph.edges[1, 2]["weight"])

    def test_pair_discounts_into_past(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3, 4, 5])
        applyPreviousPairWeightDiscount(
            peopleGraph, [{"pairings": {1: 2}}, {"pairings": {1: 3}}, {"pairings": {1: 4}}, {"pairings": {1: 5}}])
        self.assertEqual(0, peopleGraph.edges[1, 2]["weight"])
        self.assertEqual(25, peopleGraph.edges[1, 3]["weight"])
        self.assertEqual(25 + 25/2, peopleGraph.edges[1, 4]["weight"])
        self.assertEqual(25 + 25/2 + 25/4, peopleGraph.edges[1, 5]["weight"])

    def test_discounts_repeatedly_for_paired_repeatedly(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3])
        applyPreviousPairWeightDiscount(
            peopleGraph, [
                {"pairings": {}},
                {"pairings": {1: 2}},
                {"pairings": {1: 2}}
            ]
        )
        self.assertEqual(100*0.25*0.375, peopleGraph.edges[1, 2]["weight"])

    def test_handles_multiple_discounts(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3, 4])
        applyPreviousPairWeightDiscount(
            peopleGraph, [
                {"pairings": {1: 2, 3: 4}},
                {"pairings": {1: 3, 2: 4}}
            ]
        )
        self.assertEqual(
            [(1, 2, 0.0), (1, 3, 25.0), (1, 4, 100),
             (2, 3, 100), (2, 4, 25.0), (3, 4, 0.0)],
            list(peopleGraph.edges.data("weight"))
        )


class TestUnpairedWeightBoost(TestCase):
    def test_no_pairings_does_not_alter_weights(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3])
        applyUnpairedWeightBoost(peopleGraph, [])
        self.assertEqual(list(peopleGraph.edges.data("weight")),
                         [(1, 2, 100), (1, 3, 100), (2, 3, 100)])
        applyUnpairedWeightBoost(peopleGraph, [{"unpaired": []}])
        self.assertEqual(list(peopleGraph.edges.data("weight")),
                         [(1, 2, 100), (1, 3, 100), (2, 3, 100)])

    def test_applies_boost_single_time_single_person(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3])
        applyUnpairedWeightBoost(peopleGraph, [{"unpaired": [2]}])
        self.assertEqual(list(peopleGraph.edges.data("weight")),
                         [(1, 2, 115), (1, 3, 100), (2, 3, 115)])

    def test_applies_boost_multiple_times_single_person(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3])
        applyUnpairedWeightBoost(
            peopleGraph, [{"unpaired": [2]}, {"unpaired": [2]}])
        self.assertEqual(list(peopleGraph.edges.data("weight")),
                         [(1, 2, 130), (1, 3, 100), (2, 3, 130)])

    def test_applies_boost_multiple_times_multiple_people(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3, 4])
        applyUnpairedWeightBoost(
            peopleGraph, [{"unpaired": [3, 4]}, {"unpaired": [3]}])
        self.assertEqual(
            list(peopleGraph.edges.data("weight")),
            [(1, 2, 100), (1, 3, 130), (1, 4, 115),
             (2, 3, 130), (2, 4, 115), (3, 4, 145)])
        # It is potentially undesirable behaviour that 3 & 4 have such a high weight.
        # It is not a good outcome that two people that have been unpaired are incentivised
        # by the algorithm to be paired above other potential pairings


class TestSameLocationBoost(TestCase):
    def test_no_location_does_not_alter_weights(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3])
        applySameLocationBoost(peopleGraph, {})
        self.assertEqual(list(peopleGraph.edges.data("weight")),
                         [(1, 2, 100), (1, 3, 100), (2, 3, 100)])

    def test_two_people_same_location(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3])
        applySameLocationBoost(peopleGraph, {1: 'office', 2: 'office'})
        self.assertEqual(250, peopleGraph.edges[1, 2]["weight"])
        self.assertEqual(100, peopleGraph.edges[1, 3]["weight"])

    def test_four_people_two_locations(self):
        peopleGraph = convertPeopleToGraph([1, 2, 3, 4])
        applySameLocationBoost(
            peopleGraph, {1: 'office', 2: 'office', 3: 'home', 4: 'home'})
        self.assertEqual(
            [(1, 2, 250), (1, 3, 100), (1, 4, 100),
             (2, 3, 100), (2, 4, 100), (3, 4, 250)],
            list(peopleGraph.edges.data("weight"))
        )


class TestDoFullPairing(TestCase):
    def test_everyone_gets_a_go(self):
        # Run 5 pairings with 5 people
        # Each person should be excluded once under our scheme
        previousPairObjs = []
        for i in range(5):
            pairings, unpaired = doFullPairing(
                [1, 2, 3, 4, 5], previousPairObjs, {})
            previousPairObjs.append({
                "pairings": pairings,
                "unpaired": unpaired
            })
        unpairedChoices = [
            pairObj["unpaired"][0]
            for pairObj in previousPairObjs
        ]
        self.assertTrue(all(i in unpairedChoices for i in [1, 2, 3, 4, 5]))

    def test_homeworkers_get_paired_forever(self):
        # Run a lot of pairings with 6 people, 2 homeworkers, rest office
        # The homeworkers should be paired every single round under our scheme
        previousPairObjs = []
        for i in range(100):
            pairings, unpaired = doFullPairing(
                [1, 2, 3, 4, 5, 6], previousPairObjs, {1: 'office', 2: 'home', 3: 'home', 4: 'office', 5: 'office', 6: 'office'})
            previousPairObjs.append({
                "pairings": pairings,
                "unpaired": unpaired
            })
        self.assertTrue(
            all(
                pairObj["pairings"].get(2, None) == 3 or
                pairObj["pairings"].get(3, None) == 2
                for pairObj in previousPairObjs
            )
        )
