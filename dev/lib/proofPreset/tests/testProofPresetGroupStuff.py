from proofPreset import ProofPreset, ProofPresetError
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

    def test_addGroupsOfSameName(self):
        """
        Add more than one group of the same name
        (no overwrite)
        """
        firstGroup = {"name": "new group", "type size": 2, "contents": ["abcde"]}
        self.testPreset.addGroup(firstGroup)

        secondGroup = {"name": "new group", "type size": 8, "leading": 10, "print": True}
        self.testPreset.addGroup(secondGroup)

        secondGroup = {"name": "new group", "print": True, "contents": ["fghij"]}
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
                    "name": "new group-1",
                    "order": "",
                    "type size": 8,
                    "leading": 10,
                    "print": True,
                    "contents": []
                },
                {
                    "name": "new group-2",
                    "order": "",
                    "type size": "",
                    "leading": "",
                    "print": True,
                    "contents": ["fghij"]
                }
            ]
        }

        self.assertDictEqual(actual, expected)

    def test_addGroupNoName(self):
        """
        Fail addGroup if no name specified
        """
        newGroup = {"type size": 6}
        with self.assertRaises(ProofPresetError):
            self.testPreset.addGroup(newGroup)

    def test_addAndRemoveGroup(self):
        """
        Base case removing a group
        """
        newGroup = {"name": "new group", "type size": 2, "contents": ["abcde"]}
        self.testPreset.addGroup(newGroup)
        self.testPreset.removeGroup("new group")

        actual = self.testPreset.getPreset()
        expected = {
            "name": "testPreset",
            "groups": []
        }

        self.assertEqual(actual, expected)

    def test_addAndRemoveGroup2(self):
        """
        Add more than 1 group with the same name
        and remove one group
        """
        newGroup = {"name": "new group", "type size": 2, "contents": ["abcde"]}
        newGroup1 = {"name": "new group", "type size": 8}
        newGroup2 = {"name": "new group", "leading": 3}
        self.testPreset.addGroup(newGroup)
        self.testPreset.addGroup(newGroup1)
        self.testPreset.addGroup(newGroup2)
        
        self.testPreset.removeGroup("new group")

        actual = self.testPreset.getPreset()
        expected = {
            "name": "testPreset",
            "groups": [
                {
                    "name": "new group-1",
                    "order": "",
                    "type size": 8,
                    "leading": "",
                    "print": False,
                    "contents": []
                },
                {
                    "name": "new group-2",
                    "order": "",
                    "type size": "",
                    "leading": 3,
                    "print": False,
                    "contents": []
                }
            ]
        }

        self.assertEqual(actual, expected)

    def test_failRemoveGroup(self):
        """
        Raise error when trying to remove group
        that doesn't exist
        """
        with self.assertRaises(ProofPresetError):
            self.testPreset.removeGroup("new group")


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
