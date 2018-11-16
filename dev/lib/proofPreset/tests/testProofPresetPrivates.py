"""
Test ProofPreset private methods
"""

from proofPreset import ProofPreset, XMLtagError
import unittest
import os.path

class ProofPresetTest(unittest.TestCase):
    def setUp(self):
        self.testPreset = ProofPreset("myPreset")

    def test_checkForTagsNoClose(self):
        """
        Fail ProofPreset._checkForTags(): no closing tags
        """
        inputList = ["<group>", "<group>", "<group>"]
        with self.assertRaises(XMLtagError):
            self.testPreset.importFromXML(inputList)

    def test_checkSequenceNested(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        if tags are nested (<tag><tag></tag></tag>).
        """
        inputList = ["<group>", "<group>", "</group>", "</group>"]
        with self.assertRaises(XMLtagError):
            self.testPreset.importFromXML(inputList)
    
    def test_checkSequenceLessClose(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If 2 opens and 1 close
        """
        inputList = ["<group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            self.testPreset.importFromXML(inputList)

    def test_checkSequenceLessOpen(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If 1 open and 2 closes
        """
        inputList = ["<group>", "</group>", "</group>"]
        with self.assertRaises(XMLtagError):
            self.testPreset.importFromXML(inputList)

    def test_checkSequenceBadPairs(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If open/close/close/open
        """
        inputList = ["<group>", "</group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            self.testPreset.importFromXML(inputList)

    def test_checkSequenceStartWithClose(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If close/open/close/open
        """
        inputList = ["</group>", "<group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            self.testPreset.importFromXML(inputList)

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
