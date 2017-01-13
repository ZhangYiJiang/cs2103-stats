import unittest
from parsers import ReadmeParser


class ReadmeParserTest(unittest.TestCase):
    def setUp(self):
        with open('readme.html', encoding='utf-8') as f:
            self.parser = ReadmeParser(f.read())

    def test_title(self):
        self.assertEqual(self.parser.title, 'PriorityQ')

    def test_codacy(self):
        self.assertEqual(self.parser.codacy_grade, 'A')

    def test_coveralls(self):
        self.assertEqual(self.parser.coveralls_grade, 83)

    def test_travis(self):
        self.assertEqual(self.parser.travis_status, 'passing')
