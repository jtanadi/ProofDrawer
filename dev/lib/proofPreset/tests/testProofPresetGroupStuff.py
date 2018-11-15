from proofPreset import ProofPreset
import unittest

class TestImportExport(unittest.TestCase):
    def setUp(self):
        self.testPreset = ProofPreset("testPreset")

    def test_baseAddGroup(self):
        """
        Add complete group (group has all info filled out)
        """
        groupToAdd = {
            "name": "UC, lc",
            "order": 3,
            "type size": 12,
            "leading": 14,
            "print": True,
            "contents": [
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "abcdefghijklmnopqrstuvwxyz"
            ]
        }
        expectedPreset = {
            "name": "testPreset",
            "groups": [groupToAdd]
        }
        self.testPreset.addGroup(groupToAdd)
        actual = self.testPreset.getPreset()
        self.assertDictEqual(expectedPreset, actual)

    def test_addIncompleteGroup(self):
        """
        Add incomplete group
        """
        groupToAdd = {"name": "new test", "contents": ["abcde"]}
        expectedPreset = {
            "name": "testPreset",
            "groups": [
                {
                    "name": "new test",
                    "order": "",
                    "type size": "",
                    "leading": "",
                    "print": False,
                    "contents": ["abcde"]
                }
            ]
        }
        self.testPreset.addGroup(groupToAdd)
        actual = self.testPreset.getPreset()
        self.assertDictEqual(expectedPreset, actual)
        
    def test_overwriteGroup(self):
        """
        Add one group and then overwrite with anoter
        """
        firstGroup = {"name": "new group", "type size": 2}
        self.testPreset.addGroup(firstGroup)

        secondGroup = {"name": "new group", "type size": 8, "leading": 10}
        self.testPreset.addGroup(secondGroup, overwrite=True)

        actual = self.testPreset.getPreset()
        expected = {
            "name": "testPreset",
            "groups": [
                {
                    "name": "new group",
                    "order": "",
                    "type size": 8,
                    "leading": 10,
                    "print": False,
                    "contents": []
                }
            ]
        }

        self.assertDictEqual(actual, expected)

    def test_addTwoGroupsOfSameName(self):
        """
        Add one group and then another with the same name
        (no overwrite)
        """
        firstGroup = {"name": "new group", "type size": 2, "contents": ["abcde"]}
        self.testPreset.addGroup(firstGroup)

        secondGroup = {"name": "new group", "type size": 8, "leading": 10, "print": True}
        self.testPreset.addGroup(secondGroup)

        actual = self.testPreset.getPreset()
        expected = {
            "name": "testPreset",
            "groups": [
                {
                    "name": "new group",
                    "order": "",
                    "type size": 2,
                    "leading": "",
                    "print": False,
                    "contents": ["abcde"]
                },
                {
                    "name": "new group",
                    "order": "",
                    "type size": 8,
                    "leading": 10,
                    "print": True,
                    "contents": []
                }
            ]
        }

        self.assertDictEqual(actual, expected)

    def test_addAndRemoveGroups(self):
        newGroup = {"name": "new group", "type size": 2, "contents": ["abcde"]}
        self.testPreset.addGroup(newGroup)
        self.testPreset.removeGroup("new group")

        actual = self.testPreset.getPreset()
        expected = {
            "name": "testPreset",
            "groups": []
        }

        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
