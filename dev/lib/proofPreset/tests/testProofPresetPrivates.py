"""
Fail ProofPreset private methods & make sure
XMLtagError is raised everytime
"""

from proofPreset.proofPreset import ProofPreset, XMLtagError
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
            self.testPreset.importProof(inputList, "group")

    def test_checkSequenceNested(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        if tags are nested (<tag><tag></tag></tag>).
        """
        inputList = ["<group>", "<group>", "</group>", "</group>"]
        with self.assertRaises(XMLtagError):
            self.testPreset.importProof(inputList, "group")
    
    def test_checkSequenceLessClose(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If 2 opens and 1 close
        """
        inputList = ["<group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            self.testPreset.importProof(inputList, "group")

    def test_checkSequenceLessOpen(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If 1 open and 2 closes
        """
        inputList = ["<group>", "</group>", "</group>"]
        with self.assertRaises(XMLtagError):
            self.testPreset.importProof(inputList, "group")

    def test_checkSequenceBadPairs(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If open/close/close/open
        """
        inputList = ["<group>", "</group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            self.testPreset.importProof(inputList, "group")

    def test_checkSequenceStartWithClose(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If close/open/close/open
        """
        inputList = ["</group>", "<group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            self.testPreset.importProof(inputList, "group")

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
