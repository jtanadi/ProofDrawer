"""
THIS IS OLD, before functions consolidated into class
"""

from lib.utils.convertProofToPreset import parseProofDoc
import os.path
import unittest

class TestParseProofDoc(unittest.TestCase):
    def test_baseAsFile(self):
        """
        Base case. The file content looks like this:
        <group>
        UC, lc, numerals
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        abcdefghijklmnopqrstuvwxyz
        0123456789
        </group>
        <group>
        UC control
        |H| |O| HOHOHOHO
        |A| HAHAHAOAOAOA
        </group>
        """
        currentFile = os.path.dirname(__file__)
        proofDoc = os.path.join(currentFile, "resources", "proofDocTest.txt")
        expected = [
            {
                "group": "UC, lc, numerals",
                "contents": [
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    "abcdefghijklmnopqrstuvwxyz",
                    "0123456789"
                ]
            },
            {
                "group": "UC control",
                "contents": [
                    "|H| |O| HOHOHOHO",
                    "|A| HAHAHAOAOAOA"
                ]
            }
        ]
        self.assertEqual(parseProofDoc(proofDoc, "group"), expected)
    
    def test_baseAsList(self):
        """
        Base case, using list instead of file
        """
        proofList = [
            "<group>",
            "UC, lc, numerals",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "abcdefghijklmnopqrstuvwxyz",
            "0123456789",
            "</group>",
            "<group>",
            "UC control",
            "|H| |O| HOHOHOHO",
            "|A| HAHAHAOAOAOA",
            "</group>"
            ]
        expected = [
            {
                "group": "UC, lc, numerals",
                "contents": [
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    "abcdefghijklmnopqrstuvwxyz",
                    "0123456789"
                ]
            },
            {
                "group": "UC control",
                "contents": [
                    "|H| |O| HOHOHOHO",
                    "|A| HAHAHAOAOAOA"
                ]
            }
        ]
        self.assertEqual(parseProofDoc(proofList, "group"), expected)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
