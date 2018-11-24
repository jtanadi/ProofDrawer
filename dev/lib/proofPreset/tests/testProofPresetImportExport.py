from proofPreset import ProofPreset, ProofPresetError
import unittest
import os.path

fileDir = os.path.dirname(__file__)

class TestBase(unittest.TestCase):
    def setUp(self):
        self.preset = ProofPreset("myPreset")

class TestImport(TestBase):
    def setUp(self):
        super().setUp()
        self.jsonPath = os.path.join(fileDir, "resources", "proofPresetTest.json")
        self.xmlPath = os.path.join(fileDir, "resources", "xmlProofTest.xml")
        self.txtPath = os.path.join(fileDir, "resources", "proofDocTest.txt")

    def test_importXMLFromFile(self):
        """
        Base case: importing from xml file
        """
        self.preset.importFromXML(self.xmlPath)

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
        self.preset.importFromXML(self.txtPath)
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
        self.preset.importFromJSON(self.jsonPath)

        actual = self.preset.preset
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
            self.preset.importFromXML(self.jsonPath)

    def test_importJSONWrongFile(self):
        """
        Test import wrong extension
        (expect JSON, actual XML)
        """
        with self.assertRaises(ProofPresetError):
            self.preset.importFromXML(self.jsonPath)


class TestExport(TestBase):
    def setUp(self):
        super().setUp()
        self.jsonPath = os.path.join(fileDir, "resources", "jsonExportTest.json")
        self.xmlPath = os.path.join(fileDir, "resources", "xmlExportTest.xml")
        self.txtPath = os.path.join(fileDir, "resources", "jsonExportTest.txt")

        presetGroups = [
            {
                "name": "UC", 
                "typeSize": 10,
                "leading": 12,
                "print": True,
                "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
            },
            {
                "name": "lc", 
                "typeSize": 10,
                "leading": 12,
                "print": False,
                "contents": ["abcdefghijklmnopqrstuvwxyz"]
            },
            {
                "name": "numerals", 
                "typeSize": 10,
                "leading": 12,
                "print": True,
                "contents": ["0123456789"]
            }
        ]

        for group in presetGroups:
            self.preset.addGroup(group)

    def test_exportJSONFile(self):
        self.preset.exportToJSON(self.jsonPath)
    
    def test_exportXMLFile(self):
        self.preset.exportToXML(self.xmlPath)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
