"""
Test ProofPreset private methods
"""

from proofPreset import ProofGroup
from proofPreset.errors import ProofPresetError, XMLtagError
import unittest
import os.path

class ProofPresetTest(unittest.TestCase):
    def setUp(self):
        self.testGroup = ProofGroup({"name": "test"})

    def test_removeUnnecessaryKeys(self):
        newGroup = {"name": "tester", "boinger": False}
        actual = self.testGroup._removeUnneededKeysInGroup(newGroup)
        expected = {"name": "tester"}

        self.assertEqual(actual, expected)

    def test_addMissingKeys(self):
        newGroup = {"name": "tester"}
        actual = self.testGroup._addMissingKeysToGroup(newGroup)
        expected = {
            "name": "tester",
            "typeSize": "",
            "leading": "",
            "print": False,
            "contents": []
            }

        self.assertEqual(actual, expected)

    def test_editGroup(self):
        self.testGroup.name = "new name"
        self.testGroup.typeSize = 12
        self.testGroup.leading = 10
        self.testGroup.contents = ["hey", "how", "are", "you"]

        actual = self.testGroup
        expected = {
            "name": "new name",
            "typeSize": 12,
            "leading": 10,
            "print": False,
            "contents": ["hey", "how", "are", "you"]
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
