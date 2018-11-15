"""
Test ProofPreset object
"""

from proofPreset import ProofPreset
import unittest
import os.path

class ProofPresetTest(unittest.TestCase):
    def setUp(self):
        fileDir = os.path.dirname(__file__)
        testFileDir = os.path.join(fileDir, "resources", "proofDocTest.txt")

        with open(testFileDir, "r") as testFile:
            testList = testFile.readlines()

        self.testPreset = ProofPreset("myPreset")
        self.testPreset.importFromXML(testList)

    def test_baseGetTags(self):
        """
        Base case for ProofPreset.getTags()
        """
        tagsList = self.testPreset._getTags()
        expected = ["<group>", "</group>", "<group>",
                    "</group>", "<group>", "</group>"]
        self.assertEqual(tagsList, expected)

    def test_baseCleanList(self):
        dirtyList = ["item\n", "\n", "\nnext", "\n\n"]
        cleanList = self.testPreset._cleanList(dirtyList)
        expected = ["item", "next"]
        self.assertEqual(cleanList, expected)

    def test_getName(self):
        actual = self.testPreset.getName()
        self.assertEqual(actual, "myPreset")

    def test_rename(self):
        newName = "funTimes"
        self.testPreset.renamePreset(newName)
        actual = self.testPreset.getName()

        self.assertEqual(newName, actual)

    def test_baseGetPreset(self):
        """
        Base case for ProofPreset.parseProofDoc()
        """
        testProof = self.testPreset.getPreset()
        expected = {
            "name": "myPreset",
            "groups": [
                {
                    "name": "UC, lc, numerals",
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
                    "name": "UC control",
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
                    "name": "lc control",
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

    def test_baseGetGroups(self):
        actual = self.testPreset.getGroups()
        expected = [
            {
                "name": "UC, lc, numerals",
                "contents": [
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    "abcdefghijklmnopqrstuvwxyz",
                    "0123456789"
                ]
            },
            {
                "name": "UC control",
                "contents": [
                    "|H| |O| HOHOHOHO",
                    "|A| HAHAHAOAOAOA",
                    "|B| HBHBHBOBOBOB",
                    "|C| HCHCHCOCOCOC"
                ]
            },
            {
                "name": "lc control",
                "contents": [
                    "|n| |o| nononono",
                    "|a| nananaoaoaoa",
                    "|b| nbnbnbobobob",
                    "|c| ncncncocococ"
                ]
            }
        ]

        self.assertEqual(actual, expected)

    def test_baseImportString(self):
        testString = "<group>\nUC\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n</group>"
        expected = {
            "name": "myPreset",
            "groups": [
                {
                    "name": "UC",
                    "order": 1,
                    "type size": "",
                    "leading": "",
                    "print": False,
                    "contents": [
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    ]
                }
            ]
        }
        strTestPreset = ProofPreset()
        strTestPreset.importFromXML(testString)
        actual = strTestPreset.getPreset()
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
