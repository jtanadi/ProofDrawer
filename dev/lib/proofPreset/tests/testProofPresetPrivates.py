"""
Test ProofPreset private methods
"""

from proofPreset import ProofPreset
from proofPreset.errors import ProofPresetError, XMLtagError
import unittest
import os.path

class ProofPresetTest(unittest.TestCase):
    def setUp(self):
        self.testPreset = ProofPreset("myPreset")

    def test_removeUnnecessaryKeys(self):
        newGroup = {"name": "tester", "boinger": False}
        actual = self.testPreset._removeUnneededKeysInGroup(newGroup)
        expected = {"name": "tester"}

        self.assertEqual(actual, expected)

    def test_addMissingKeys(self):
        newGroup = {"name": "tester"}
        actual = self.testPreset._addMissingKeysToGroup(newGroup)
        expected = {
            "name": "tester",
            "typeSize": "",
            "leading": "",
            "print": False,
            "contents": []
            }

        self.assertEqual(actual, expected)

    def test_countGroupNames(self):
        """
        This only works if _checkForCopy is False,
        because otherwise the names will have their
        counts appended.
        """
        # 4 group1s, 2 group2s, 3 group3s, 1 group4, 1 group5
        groupsToAdd = [
            {"name": "group1"},
            {"name": "group1"},
            {"name": "group1"},
            {"name": "group2"},
            {"name": "group3"},
            {"name": "group3"},
            {"name": "group4"},
            {"name": "group5"},
            {"name": "group3"},
            {"name": "group2"},
            {"name": "group1"}
        ]

        for group in groupsToAdd:
            self.testPreset.addGroup(group, _checkForCopy=False)

        self.testPreset._countGroupNames()

        actual = self.testPreset.groupNameCount
        expected = {"group1": 4, "group2": 2, "group3": 3, "group4": 1, "group5": 1}

        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
