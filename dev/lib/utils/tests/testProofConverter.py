from lib.utils.proofConverter import ProofConverter, XMLtagError
import unittest
import os.path

class ProofConverterTest(unittest.TestCase):
    def setUp(self):
        fileDir = os.path.dirname(__file__)
        testFileDir = os.path.join(fileDir, "resources", "proofDocTest.txt")

        testFile = open(testFileDir, "r")
        testList = testFile.readlines()
        testFile.close()

        self.testPreset = ProofConverter(testList, "group")

    def test_baseGetTags(self):
        """
        Base case for ProofConverter.getTags()
        """
        tagsList = self.testPreset.getTags()
        expected = ["<group>", "</group>", "<group>",
                    "</group>", "<group>", "</group>"]
        self.assertEqual(tagsList, expected)

    def test_baseReturnAllButTags(self):
        """
        Base case for ProofConverter.returnAllButTags()
        """
        pass

    def test_baseParseProofDoc(self):
        """
        Base case for ProofConverter.parseProofDoc()
        """
        testProof = self.testPreset.parseProofDoc()
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
                    "|A| HAHAHAOAOAOA",
                    "|B| HBHBHBOBOBOB",
                    "|C| HCHCHCOCOCOC"
                ]
            },
            {
                "group": "lc control",
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
        Fail ProofConverter._checkForTags(): no closing tags
        """
        inputList = ["<group>", "<group>", "<group>"]
        with self.assertRaises(XMLtagError):
            testProof = ProofConverter(inputList, "group")

    def test_checkSequenceNested(self):
        """
        Fail ProofConverter._checkXMLtagsSequence()
        if tags are nested (<tag><tag></tag></tag>).
        """
        inputList = ["<group>", "<group>", "</group>", "</group>"]
        with self.assertRaises(XMLtagError):
            testProof = ProofConverter(inputList, "group")
    
    def test_checkSequenceLessClose(self):
        """
        Fail ProofConverter._checkXMLtagsSequence()
        If 2 opens and 1 close
        """
        inputList = ["<group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            testProof = ProofConverter(inputList, "group")

    def test_checkSequenceLessOpen(self):
        """
        Fail ProofConverter._checkXMLtagsSequence()
        If 1 open and 2 closes
        """
        inputList = ["<group>", "</group>", "</group>"]
        with self.assertRaises(XMLtagError):
            testProof = ProofConverter(inputList, "group")

    def test_checkSequenceBadPairs(self):
        """
        Fail ProofConverter._checkXMLtagsSequence()
        If open/close/close/open
        """
        inputList = ["<group>", "</group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            testProof = ProofConverter(inputList, "group")            

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
