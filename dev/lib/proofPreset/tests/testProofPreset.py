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
        actual = self.testPreset.name
        self.assertEqual(actual, "myPreset")

    def test_rename(self):
        newName = "funTimes"
        self.testPreset.name = newName
        actual = self.testPreset.name

        self.assertEqual(newName, actual)

    def test_baseGetPreset(self):
        """
        Base case for ProofPreset.parseProofDoc()
        """
        testProof = self.testPreset.preset
        expected = {
            "name": "myPreset",
            "groups": [
                {
                    "name": "UC, lc, numerals",
                    "typeSize": "",
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
                    "typeSize": "",
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
                    "typeSize": "",
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
        actual = self.testPreset.groups
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
        actual = self.testPreset.groups
        expected = [
            {
                "name": "UC, lc, numerals",
                "typeSize": "",
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
                "typeSize": "",
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
                "typeSize": "",
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

    def test_baseGetXMLGroups(self):
        actual = self.testPreset.xmlGroups
        expected = "<group>\nUC, lc, numerals\nABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz\n0123456789\n</group>\n\n"
        expected += "<group>\nUC control\n|H| |O| HOHOHOHO\n|A| HAHAHAOAOAOA\n|B| HBHBHBOBOBOB\n|C| HCHCHCOCOCOC\n</group>\n\n"
        expected += "<group>\nlc control\n|n| |o| nononono\n|a| nananaoaoaoa\n|b| nbnbnbobobob\n|c| ncncncocococ\n</group>"

        self.assertEqual(actual, expected)

    def test_baseImportString(self):
        testString = "<group>\nUC\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n</group>"
        expected = {
            "name": "myPreset",
            "groups": [
                {
                    "name": "UC",
                    "typeSize": "",
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
        actual = strTestPreset.preset
        self.assertEqual(actual, expected)

    def test_duplicatePreset(self):
        """
        Test duplication
        """
        newPreset = self.testPreset.duplicatePreset('new')

        oldGroups = self.testPreset.groups
        newGroups = newPreset.getGroups()

        # Make sure groups are the same, but presets aren't
        # actually pointing to the same object in memory
        self.assertEqual(oldGroups, newGroups)
        self.assertNotEqual(newPreset, self.testPreset)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
