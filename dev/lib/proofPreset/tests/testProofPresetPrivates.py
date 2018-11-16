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
            "type size": "",
            "leading": "",
            "print": False,
            "contents": []
            }

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
