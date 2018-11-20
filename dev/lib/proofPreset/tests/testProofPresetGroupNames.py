from proofPreset import ProofPreset, ProofPresetError
from collections import Counter
import unittest
import os.path

class TestGroupNames(unittest.TestCase):
    def setUp(self):
        self.proofPreset = ProofPreset("Test Proof Preset")
        currentDir = os.path.dirname(__file__)
        xmlDoc = os.path.join(currentDir, "resources", "proofDocForNamesTest.txt")

        with open(xmlDoc) as f:
            self.xmlProof = f.read()

    def test_importXMLWithSameNames(self):
        """
        Import from XML doc, where groups
        have the same name.

        3x "UC"
        2x "lc"
        1x "numerals"
        1x "UC & lc"
        3x "controls"

        At import, duplicate names should have
        a count appended
        """
        self.proofPreset.importFromXML(self.xmlProof)
        actual = Counter(self.proofPreset.getGroupNames())
        expected = Counter([
            "controls", "controls-1", "controls-2",
            "lc", "lc-1",
            "numerals",
            "UC", "UC-1", "UC-2",
            "UC & lc"
        ])

        self.assertEqual(actual, expected)

    def test_addGroupsWithSameNames(self):
        """
        Add group one by one, some with
        duplicate names.

        3x "UC"
        2x "lc"
        1x "numerals"
        1x "UC & lc"
        3x "controls"

        Duplicate names should have a count appended
        """
        ucGroup = {"name": "UC"}
        lcGroup = {"name": "lc"}
        numsGroup = {"name": "numerals"}
        ucLcGroup = {"name": "UC & lc"}
        controlsGroup = {"name": "controls"}

        self.proofPreset.addGroup(ucGroup)
        self.proofPreset.addGroup(lcGroup)
        self.proofPreset.addGroup(numsGroup)
        self.proofPreset.addGroup(ucLcGroup)
        self.proofPreset.addGroup(controlsGroup)
        self.proofPreset.addGroup(ucGroup)
        self.proofPreset.addGroup(lcGroup)
        self.proofPreset.addGroup(controlsGroup)
        self.proofPreset.addGroup(ucGroup)
        self.proofPreset.addGroup(controlsGroup)

        actual = Counter(self.proofPreset.getGroupNames())
        expected = Counter([
            "controls", "controls-1", "controls-2",
            "lc", "lc-1",
            "numerals",
            "UC", "UC-1", "UC-2",
            "UC & lc"
        ])

        self.assertEqual(actual, expected)

    def test_dontReturnNameCopies(self):
        """
        Import from XML doc, where groups
        have the same name.

        At import, duplicate names should have
        a count appended, but only return names
        without count.
        """
        self.proofPreset.importFromXML(self.xmlProof)
        actual = Counter(self.proofPreset.getGroupNames(returnCopies=False))
        expected = Counter(["controls", "lc", "numerals", "UC", "UC & lc"])

        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
        