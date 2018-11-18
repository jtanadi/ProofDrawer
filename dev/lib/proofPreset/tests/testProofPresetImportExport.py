from proofPreset import ProofPreset, ProofPresetError
import unittest
import os.path

fileDir = os.path.dirname(__file__)
jsonPath = os.path.join(fileDir, "resources", "proofPresetTest.json")
xmlPath = os.path.join(fileDir, "resources", "xmlProofTest.xml")
txtPath = os.path.join(fileDir, "resources", "proofDocTest.txt")

class TestImportExport(unittest.TestCase):
    def setUp(self):
        self.preset = ProofPreset("myPreset")

    def test_importXMLFromFile(self):
        """
        Base case: importing from xml file
        """
        self.preset.importFromXML(xmlPath)

        actual = self.preset.getGroups(verbose=False)
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

        self.assertEqual(expected, actual)

    def test_importTXTFromFile(self):
        """
        Base case: import txt
        """
        self.preset.importFromXML(txtPath)
        actual = self.preset.getGroups(verbose=False)
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

    def test_importJSONFromFile(self):
        """
        Base case: importing from JSON file
        """
        self.preset.importFromJSON(jsonPath)

        actual = self.preset.getPreset()
        expected = {
            "name": "proofPreset1",
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

        self.assertEqual(expected, actual)

    def test_importXMLWrongFile(self):
        """
        Test import wrong extension
        (expect XML, actual JSON)
        """
        with self.assertRaises(ProofPresetError):
            self.preset.importFromXML(jsonPath)

    def test_importJSONWrongFile(self):
        """
        Test import wrong extension
        (expect JSON, actual XML)
        """
        with self.assertRaises(ProofPresetError):
            self.preset.importFromXML(jsonPath)
        

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
