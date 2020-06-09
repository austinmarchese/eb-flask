import unittest

from src.main.tag_identifier import TagIdentifier

class TestTagIdentifier(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        super(TestTagIdentifier, self).setUpClass()
        self.tag_identifier = TagIdentifier()
