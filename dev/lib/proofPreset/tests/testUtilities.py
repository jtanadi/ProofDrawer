"""
Testing utility functions
"""

from proofPreset import utils
from proofPreset.errors import XMLtagError
import unittest

class TestUtilities(unittest.TestCase):
    def test_baseGetTags(self):
        """
        Base case for utils.getTags()
        """
        testList = [
            "<group>",
            "UC, lc, numerals",
            "</group>",
            "<group>",
            "Combos",
            "</group>",
            "<group>",
            "Controls",
            "|H| HOHOHO",
            "</group>"
        ]

        actual = utils.getTags(testList, "group")
        expected = ["<group>", "</group>", "<group>",
                    "</group>", "<group>", "</group>"]
        self.assertEqual(actual, expected)

    def test_baseCleanList(self):
        """
        Base case for utils.cleanList()
        """
        dirtyList = ["item\n", "\n", "\nnext", "\n\n"]
        
        actual = utils.cleanList(dirtyList)
        expected = ["item", "next"]
        self.assertEqual(actual, expected)

    def test_cleanListDiscardBefore(self):
        """
        utils.cleanList(discardBefore="<group>")
        """
        dirtyList = ["stuf", "here", "<group>", "item\n", "\n", "\nnext", "\n\n"]
        
        actual = utils.cleanList(dirtyList, discardBefore="<group>")
        expected = ["<group>", "item", "next"]
        self.assertEqual(actual, expected)
    
    def test_cleanListDiscardAfter(self):
        """
        utils.cleanList(discardAfter="</group>")
        """
        dirtyList = ["item\n", "\n", "\nnext", "\n\n", "</group>", "more", "stuff"]
        
        actual = utils.cleanList(dirtyList, discardAfter="</group>")
        expected = ["item", "next", "</group>"]
        self.assertEqual(actual, expected)

    def test_cleanListDiscardBeforeAfter(self):
        """
        utils.cleanList(discardAfter="</group>")
        """
        dirtyList = ["stuf", "here", "<group>", "item\n", "\n",
                     "\nnext", "\n\n", "</group>", "more", "stuff"]
        
        actual = utils.cleanList(dirtyList, discardBefore="<group>", discardAfter="</group>")
        expected = ["<group>", "item", "next", "</group>"]
        self.assertEqual(actual, expected)

    def test_checkForTagsNoClose(self):
        """
        Fail utils.checkForTags(): no closing tags
        """
        inputList = ["<group>", "<group>", "<group>"]
        with self.assertRaises(XMLtagError):
            utils.checkForTags(inputList, "group")

    def test_checkSequenceNested(self):
        """
        Fail utils.checkXMLtagsSequence()
        if tags are nested (<tag><tag></tag></tag>).
        """
        inputList = ["<group>", "<group>", "</group>", "</group>"]
        with self.assertRaises(XMLtagError):
            utils.checkXMLtagsSequence(inputList, "group")

    def test_checkSequenceLessClose(self):
        """
        Fail utils.checkXMLtagsSequence()
        If 2 opens and 1 close
        """
        inputList = ["<group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            utils.checkXMLtagsSequence(inputList, "group")

    def test_checkSequenceLessOpen(self):
        """
        Fail utils.checkXMLtagsSequence()
        If 1 open and 2 closes
        """
        inputList = ["<group>", "</group>", "</group>"]
        with self.assertRaises(XMLtagError):
            utils.checkXMLtagsSequence(inputList, "group")

    def test_checkSequenceBadPairs(self):
        """
        Fail utils.checkXMLtagsSequence()
        If open/close/close/open
        """
        inputList = ["<group>", "</group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            utils.checkXMLtagsSequence(inputList, "group")

    def test_checkSequenceStartWithClose(self):
        """
        Fail utils.checkXMLtagsSequence()
        If close/open/close/open
        """
        inputList = ["</group>", "<group>", "</group>", "<group>"]
        with self.assertRaises(XMLtagError):
            utils.checkXMLtagsSequence(inputList, "group")
    

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)