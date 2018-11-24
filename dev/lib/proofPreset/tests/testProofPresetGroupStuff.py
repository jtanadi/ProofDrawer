from proofPreset import ProofPreset, ProofPresetError
import unittest

class TestGroupStuff(unittest.TestCase):
    def setUp(self):
        self.testPreset = ProofPreset("testPreset")

    def test_baseAddGroup(self):
        """
        Add complete group (group has all info filled out)
        """
        groupToAdd = {
            "name": "UC, lc",
            "order": 3, # This should be ignored because it's not something we care about
            "typeSize": 12,
            "leading": 14,
            "print": True,
            "contents": [
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "abcdefghijklmnopqrstuvwxyz"
            ]
        }
        expectedPreset = {
            "name": "testPreset",
            "groups": [
                {
                    "name": "UC, lc",
                    "typeSize": 12,
                    "leading": 14,
                    "print": True,
                    "contents": [
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                        "abcdefghijklmnopqrstuvwxyz"
                    ]
                }
            ]
        }
        self.testPreset.addGroup(groupToAdd)
        actual = self.testPreset.preset
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
                    "typeSize": "",
                    "leading": "",
                    "print": False,
                    "contents": ["abcde"]
                }
            ]
        }
        self.testPreset.addGroup(groupToAdd)
        actual = self.testPreset.preset
        self.assertDictEqual(expectedPreset, actual)

    def test_overwriteGroup(self):
        """
        Add one group and then overwrite with anoter
        """
        firstGroup = {"name": "new group", "typeSize": 2}
        self.testPreset.addGroup(firstGroup)

        secondGroup = {"name": "new group", "typeSize": 8, "leading": 10}
        self.testPreset.addGroup(secondGroup, overwrite=True)

        actual = self.testPreset.preset
        expected = {
            "name": "testPreset",
            "groups": [
                {
                    "name": "new group",
                    "typeSize": 8,
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
        firstGroup = {"name": "new group", "typeSize": 2, "contents": ["abcde"]}
        self.testPreset.addGroup(firstGroup)

        secondGroup = {"name": "new group", "typeSize": 8, "leading": 10, "boing": True}
        self.testPreset.addGroup(secondGroup)

        thirdGroup = {"name": "new group", "print": True, "contents": ["fghij"]}
        self.testPreset.addGroup(thirdGroup)

        actual = self.testPreset.preset

        expected = {
            "name": "testPreset",
            "groups": [
                {
                    "name": "new group",
                    "typeSize": 2,
                    "leading": "",
                    "print": False,
                    "contents": ["abcde"]
                },
                {
                    "name": "new group-1",
                    "typeSize": 8,
                    "leading": 10,
                    "print": False,
                    "contents": []
                },
                {
                    "name": "new group-2",
                    "typeSize": "",
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
        newGroup = {"typeSize": 6}
        with self.assertRaises(ProofPresetError):
            self.testPreset.addGroup(newGroup)

    def test_addGroupsSameNames(self):
        """
        Add a few groups, some with the same name
        """
        from collections import Counter

        # 4 group1s, 2 group2s, 3 group3s, 1 group4, 1 group5
        groupsToAdd = [
            {"name": "group1"},
            {"name": "group1"},
            {"name": "group1"},
            {"name": "group2"},
            {"name": "group3"},
            {"name": "group3"},
            {"name": "group4"},
            {"name": "group5"},
            {"name": "group3"},
            {"name": "group2"},
            {"name": "group1"}
        ]

        for group in groupsToAdd:
            self.testPreset.addGroup(group)

        actual = Counter(self.testPreset.groupNames)
        expected = Counter([
            "group1", "group1-1", "group1-2", "group1-3",
            "group2", "group2-1",
            "group3", "group3-1", "group3-2",
            "group4", "group5"
        ])

        self.assertEqual(actual, expected)

    def test_addAndRemoveGroup(self):
        """
        Base case removing a group
        """
        newGroup = {"name": "new group", "typeSize": 2, "contents": ["abcde"]}
        self.testPreset.addGroup(newGroup)
        self.testPreset.removeGroup("new group")

        actual = self.testPreset.preset
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
        newGroup = {"name": "new group", "typeSize": 2, "contents": ["abcde"]}
        newGroup1 = {"name": "new group", "typeSize": 8}
        newGroup2 = {"name": "new group", "leading": 3}
        self.testPreset.addGroup(newGroup)
        self.testPreset.addGroup(newGroup1)
        self.testPreset.addGroup(newGroup2)

        self.testPreset.removeGroup("new group")

        actual = self.testPreset.preset
        expected = {
            "name": "testPreset",
            "groups": [
                {
                    "name": "new group-1",
                    "typeSize": 8,
                    "leading": "",
                    "print": False,
                    "contents": []
                },
                {
                    "name": "new group-2",
                    "typeSize": "",
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
        with self.assertRaises(KeyError):
            self.testPreset.removeGroup("new group")

    def test_editGroup(self):
        newGroup = {
            "name": "New Group",
            "typeSize": 12,
            "leading": 14,
            "print": True,
            "contents": []
        }
        self.testPreset.addGroup(newGroup)
        self.testPreset.editGroup(0, name="Even newer",
                                  typeSize=10, leading=12,
                                  print=False, bleep=12)

        actual = self.testPreset.groups
        expected = [
            {
                "name": "Even newer",
                "typeSize": 10,
                "leading": 12,
                "print": False,
                "contents": []
            }
        ]

        self.assertEqual(actual, expected)

    def test_editGroupSameName(self):
        newGroup = {
            "name": "New Group",
            "typeSize": 12,
            "leading": 14,
            "print": True,
            "contents": []
        }
        self.testPreset.addGroup(newGroup)

        with self.assertRaises(ValueError):
            self.testPreset.editGroup(0, name="New Group",
                                      typeSize=10, leading=12,
                                      print=False, bleep=12)

    def test_moveGroupUp(self):
        group1 = {"name": "group1", "contents": ["abcde"]}
        group2 = {"name": "group2", "contents": ["fghij"]}
        group3 = {"name": "group3", "contents": ["klmno"]}
        self.testPreset.addGroup(group1)
        self.testPreset.addGroup(group2)
        self.testPreset.addGroup(group3)

        self.testPreset.moveGroup(2, 1)
        actual = self.testPreset.shortGroups

        expected = [
            {"name": "group1", "contents": ["abcde"]},
            {"name": "group3", "contents": ["klmno"]},
            {"name": "group2", "contents": ["fghij"]},
        ]

        self.assertEqual(actual, expected)

    def test_moveGroupDown(self):
        group1 = {"name": "group1", "contents": ["abcde"]}
        group2 = {"name": "group2", "contents": ["fghij"]}
        group3 = {"name": "group3", "contents": ["klmno"]}
        self.testPreset.addGroup(group1)
        self.testPreset.addGroup(group2)
        self.testPreset.addGroup(group3)

        self.testPreset.moveGroup(0, 2)
        actual = self.testPreset.shortGroups

        expected = [
            {"name": "group2", "contents": ["fghij"]},
            {"name": "group3", "contents": ["klmno"]},
            {"name": "group1", "contents": ["abcde"]},
        ]

        self.assertEqual(actual, expected)

    def test_moveGroupRandom1(self):
        group1 = {"name": "group1", "contents": ["abcde"]}
        group2 = {"name": "group2", "contents": ["fghij"]}
        group3 = {"name": "group3", "contents": ["klmno"]}
        self.testPreset.addGroup(group1)
        self.testPreset.addGroup(group2)
        self.testPreset.addGroup(group3)

        self.testPreset.moveGroup(-1, 1)
        actual = self.testPreset.shortGroups

        expected = [
            {"name": "group1", "contents": ["abcde"]},
            {"name": "group3", "contents": ["klmno"]},
            {"name": "group2", "contents": ["fghij"]},
        ]

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
