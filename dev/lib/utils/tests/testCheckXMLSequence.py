from lib.utils.convertProofToPreset import checkXMLtagsSequence, XMLtagError
import unittest

class TestCheckXMLtagsSequence(unittest.TestCase):
    def test_base(self):
        """
        Base case: check open tag is closed
        """
        tagsList = ["<group>", "</group>", "<group>", "</group>", "<group>", "</group>"]
        self.assertTrue(checkXMLtagsSequence(tagsList))

    def test_wrongClose(self):
        """
        Raise exception if open and close tags have different names
        """
        tagsList = ["<open>", "</close>"]
        with self.assertRaises(XMLtagError):
            checkXMLtagsSequence(tagsList)

    def test_nestedTags(self):
        """
        Raise exception if tags are nested (currently not supported)
        <tag1><tag2></tag2></tag1> shouldn't work
        """
        tagsList = ["<tag1>", "<tag2>", "</tag2>", "</tag1>"]
        with self.assertRaises(XMLtagError):
            checkXMLtagsSequence(tagsList)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
