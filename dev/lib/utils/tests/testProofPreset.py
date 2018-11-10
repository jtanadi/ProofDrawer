"""
Test ProofPreset object
"""

from utils.proofPreset import ProofPreset, XMLtagError
import unittest
import os.path

class ProofPresetTest(unittest.TestCase):
    def setUp(self):
        fileDir = os.path.dirname(__file__)
        testFileDir = os.path.join(fileDir, "resources", "proofDocTest.txt")

        testFile = open(testFileDir, "r")
        testList = testFile.readlines()
        testFile.close()

        self.testPreset = ProofPreset(testList, "group")

    def test_baseGetTags(self):
        """
        Base case for ProofPreset.getTags()
        """
        tagsList = self.testPreset.getTags()
        expected = ["<group>", "</group>", "<group>",
                    "</group>", "<group>", "</group>"]
        self.assertEqual(tagsList, expected)

    def test_baseReturnAllButTags(self):
        """
        Base case for ProofPreset.returnAllButTags()
        """
        pass

    def test_baseCleanList(self):
        dirtyList = ["item\n", "\n", "\nnext", "\n\n"]
        cleanList = self.testPreset._cleanList(dirtyList)
        expected = ["item", "next"]
        self.assertEqual(cleanList, expected)

    def test_baseParseProofDoc(self):
        """
        Base case for ProofPreset.parseProofDoc()
        """
        testProof = self.testPreset.getPreset()
        expected = [
            {
                "group": "UC, lc, numerals",
                "order": 1,
                "type size": "",
                "leading": "",
                "print": False,
                "contents": [
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    "abcdefghijklmnopqrstuvwxyz",
                    "0123456789"
                ]
            },
            {
                "group": "UC control",
                "order": 2,
                "type size": "",
                "leading": "",
                "print": False,
                "contents": [
                    "|H| |O| HOHOHOHO",
                    "|A| HAHAHAOAOAOA",
                    "|B| HBHBHBOBOBOB",
                    "|C| HCHCHCOCOCOC"
                ]
            },
            {
                "group": "lc control",
                "order": 3,
                "type size": "",
                "leading": "",
                "print": False,
                "contents": [
                    "|n| |o| nononono",
                    "|a| nananaoaoaoa",
                    "|b| nbnbnbobobob",
                    "|c| ncncncocococ"
                ]
            }
        ]
        self.assertEqual(testProof, expected)

    def test_checkForTagsNoClose(self):
        """
        Fail ProofPreset._checkForTags(): no closing tags
        """
        inputList = ["<group>", "<group>", "<group>"]
        with self.assertRaises(XMLtagError):
            testProof = ProofPreset(inputList, "group")

    def test_checkSequenceNested(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        if tags are nested (<tag><tag></tag></tag>).
        """
        inputList = ["<group>", "<group>", "</group>", "</group>"]
        with self.assertRaises(XMLtagError):
            testProof = ProofPreset(inputList, "group")
    
    def test_checkSequenceLessClose(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If 2 opens and 1 close
        """
        inputList = ["<group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            testProof = ProofPreset(inputList, "group")

    def test_checkSequenceLessOpen(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If 1 open and 2 closes
        """
        inputList = ["<group>", "</group>", "</group>"]
        with self.assertRaises(XMLtagError):
            testProof = ProofPreset(inputList, "group")

    def test_checkSequenceBadPairs(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If open/close/close/open
        """
        inputList = ["<group>", "</group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            testProof = ProofPreset(inputList, "group")    

    def test_checkSequenceStartWithClose(self):
        """
        Fail ProofPreset._checkXMLtagsSequence()
        If close/open/close/open
        """
        inputList = ["</group>", "<group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            testProof = ProofPreset(inputList, "group")    


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
