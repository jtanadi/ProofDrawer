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

    def test_getName(self):
        actual = self.testPreset.getPresetName()
        self.assertEqual(actual, "myPreset")

    def test_rename(self):
        newName = "funTimes"
        self.testPreset.renamePreset(newName)
        actual = self.testPreset.getPresetName()

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

    def test_baseGetGroupsNotVerbose(self):
        actual = self.testPreset.getGroups(verbose=False)
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

    def test_baseGetGroups(self):
        actual = self.testPreset.getGroups(verbose=True)
        expected = [
            {
                "name": "UC, lc, numerals",
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

        self.assertEqual(actual, expected)

    def test_baseImportString(self):
        testString = "<group>\nUC\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n</group>"
        expected = {
            "name": "myPreset",
            "groups": [
                {
                    "name": "UC",
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
