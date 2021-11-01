from unittest import TestCase
from unittest.mock import patch

from pairModule.pairingProcesses import pairTeam


class TestPairTeam(TestCase):
    @patch('pairModule.pairingProcesses.printPairings')
    @patch('pairModule.pairingProcesses.doFullPairing')
    @patch('pairModule.pairingProcesses.savePairings')
    @patch('pairModule.pairingProcesses.getPreviousPairObjs')
    @patch('pairModule.pairingProcesses.getPeople')
    @patch('pairModule.pairingProcesses.print')
    @patch('inquirer.prompt')
    def test_no_previous_pairs_basic_path(self, inquirerPrompt, printInFunc, getPeople, getPreviousPairObjs, savePairings, doFullPairing, printPairings):
        # Set internal function returns
        getPeople.return_value = list('abcd')
        getPreviousPairObjs.return_value = []
        doFullPairing.return_value = ({'a': 'b', 'c': 'd'}, [])

        # Set responses to inquirer questions
        inquirerPrompt.side_effect = [
            {'homeworkers': []},
            {'excluded': []},
            {'save': False}
        ]

        # Run pairing process
        pairTeam('fakeee')

        # Step by step what we expect to have happened in the function
        # 1) says no previous pairings are found
        self.assertIn('No previous pairings found.',
                      str(printInFunc.call_args_list))
        # 2) asks wfh with all people and nobody preselected
        self.assertEqual(
            list('abcd'),
            inquirerPrompt \
            # 0th call
            .call_args_list[0] \
            # 0th argument (the list of questions) 0th question
            .args[0][0] \
            .choices
        )
        self.assertEqual(
            [], inquirerPrompt.call_args_list[0].args[0][0].default)
        # 3) asks who is excluded
        self.assertEqual(
            list('abcd'),
            inquirerPrompt.call_args_list[1].args[0][0].choices
        )
        self.assertEqual(
            [],
            inquirerPrompt.call_args_list[1].args[0][0].default
        )
        # 4) does full pairing
        doFullPairing.assert_called_with(
            list('abcd'), [],
            {'a': 'office', 'b': 'office', 'c': 'office', 'd': 'office'}
        )
        # 5) asks about saving
        # 6) doesn't save
        savePairings.assert_not_called()

        self.assertEqual(3, len(inquirerPrompt.call_args_list))

    @patch('pairModule.pairingProcesses.printPairings')
    @patch('pairModule.pairingProcesses.doFullPairing')
    @patch('pairModule.pairingProcesses.savePairings')
    @patch('pairModule.pairingProcesses.getPreviousPairObjs')
    @patch('pairModule.pairingProcesses.getPeople')
    @patch('pairModule.pairingProcesses.print')
    @patch('inquirer.prompt')
    def test_has_previous_pairs_basic_path(self, inquirerPrompt, printInFunc, getPeople, getPreviousPairObjs, savePairings, doFullPairing, printPairings):
        # Set internal function returns
        getPeople.return_value = list('abcdef')
        getPreviousPairObjs.return_value = [
            {
                "name": "prevPairName",
                "pairings": {
                    "a": "b",
                    "c": "d"
                },
                "excluded": ["e"],
                "unpaired": ["f"],
                "location": {
                    "d": "home"
                }
            }
        ]
        doFullPairing.return_value = ({'a': 'b', 'c': 'd'}, [])

        # Set responses to inquirer questions
        inquirerPrompt.side_effect = [
            {'redo': False},
            {'homeworkers': ["b"]},
            {'excluded': ["c"]},
            {'save': False}
        ]

        # Run pairing process
        pairTeam('fakeee')

        # Step by step what we expect to have happened in the function
        # 1) displays previous pairing
        self.assertIn('prevPairName',
                      str(printInFunc.call_args_list))
        # 1.5) asks to redo last pairing
        # 2) asks wfh with all people and 'd' preselected
        self.assertEqual(
            list('dabcef'),
            inquirerPrompt.call_args_list[1].args[0][0].choices
        )
        self.assertEqual(
            ['d'], inquirerPrompt.call_args_list[1].args[0][0].default)
        # 3) asks who is excluded
        self.assertEqual(
            list('eabcdf'),
            inquirerPrompt.call_args_list[2].args[0][0].choices
        )
        self.assertEqual(
            ['e'],
            inquirerPrompt.call_args_list[2].args[0][0].default
        )
        # 4) does full pairing
        doFullPairing.assert_called_with(
            list('abdef'),
            getPreviousPairObjs.return_value,
            {
                **{
                    letter: 'office'
                    for letter in 'acdef'
                },
                'b': 'home'
            }
        )
        # 5) asks about saving
        # 6) doesn't save
        savePairings.assert_not_called()

        self.assertEqual(4, len(inquirerPrompt.call_args_list))

    @patch('pairModule.pairingProcesses.printPairings')
    @patch('pairModule.pairingProcesses.doFullPairing')
    @patch('pairModule.pairingProcesses.savePairings')
    @patch('pairModule.pairingProcesses.getPreviousPairObjs')
    @patch('pairModule.pairingProcesses.getPeople')
    @patch('pairModule.pairingProcesses.print')
    @patch('inquirer.prompt')
    def test_has_previous_pairs_rerun_overwrite_path(self, inquirerPrompt, printInFunc, getPeople, getPreviousPairObjs, savePairings, doFullPairing, printPairings):
        # Set internal function returns
        getPeople.return_value = list('abcdef')
        getPreviousPairObjs.return_value = [
            {
                "name": "prevPairName",
                "pairings": {
                    "a": "b",
                    "c": "d"
                },
                "excluded": ["e"],
                "unpaired": ["f"],
                "location": {
                    "d": "home"
                }
            }
        ]
        doFullPairing.return_value = ({'a': 'b', 'c': 'd'}, [])

        # Set responses to inquirer questions
        inquirerPrompt.side_effect = [
            {'redo': True},
            {'homeworkers': ["b"]},
            {'excluded': ["c"]},
            {'save': True},
            {'overwrite': True}
        ]

        # Run pairing process
        pairTeam('fakeee')

        # Step by step what we expect to have happened in the function
        # 1) displays previous pairing
        # 1.5) asks to redo last pairing
        # 2) asks wfh with all people and 'd' preselected
        # 3) asks who is excluded
        # 4) does full pairing
        doFullPairing.assert_called_with(
            list('abdef'),
            [],
            {
                **{
                    letter: 'office'
                    for letter in 'acdef'
                },
                'b': 'home'
            }
        )
        # 5) asks about saving
        # 6) saves and overwrites
        self.assertEqual(
            True,
            savePairings.call_args.kwargs['overwrite_most_recent']
        )

        self.assertEqual(5, len(inquirerPrompt.call_args_list))
