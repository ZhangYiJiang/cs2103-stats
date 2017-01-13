import unittest
from parsers import GradleParser


class GradleParserTest(unittest.TestCase):
    def _create_parser(self, content):
        return GradleParser(content)

    def _read_file(self, name):
        with open(name, encoding='utf-8') as f:
            content = f.read()
        return content

    def test_parse_dependencies(self):
        parser = self._create_parser(self._read_file('build.gradle'))
        self.assertEqual(14, len(parser.dependencies))
