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

        with open(testFileDir, "r") as testFile:
            testList = testFile.readlines()

        self.testPreset = ProofPreset("myPreset")
        self.testPreset.importProof(testList, "group")

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
        expected = {
            "name": "myPreset",
            "groups": [
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
        }
        self.assertEqual(testProof, expected) 


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
