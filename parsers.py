import re
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List


class GradleParser:
    """
    This is an extremely simple and dumb Gradle build file parser.
    It does not actually understands the semantics of the Gradle file, but
    rather treats it as a simple text file and extracts out parts of it using
    some simple regexps.

    Currently only parses dependencies.
    """
    def __init__(self, content: str):
        self.content = content
        self._parse_dependencies(self.content)

    def _parse_dependencies(self, content):
        lines = content.lower().split('\n')
        self.dependencies = []

        for l in lines:
            l = l.lstrip()
            # Search for lines with 'compile' or 'testCompile'
            # See: https://docs.gradle.org/current/userguide/artifact_dependencies_tutorial.html
            if l.startswith('compile') or l.startswith('testcompile'):
                package = re.findall(r"['\"]([^'\"]+)['\"]", l)

                if len(package) > 1:
                    # Long format - eg:
                    # compile group: 'org.ocpsoft.prettytime', name: 'prettytime-nlp', version: '4.0.0.Final'
                    name = package[1]
                else:
                    # Short format - eg:
                    # compile "com.fasterxml.jackson.core:jackson-databind:$jacksonVersion"
                    try:
                        name = package[0].split(':')[1]
                    except IndexError:
                        continue
                self.dependencies.append(name)


class ReadmeParser:
    codacy_prefix = 'https://api.codacy.com/project/badge/'
    travis_prefix = 'https://travis-ci.org/'
    coveralls_prefix = 'https://coveralls.io/repos/github/'
    src_attr = 'data-canonical-src'

    def __init__(self, content: str):
        self.content = content
        self.soup = BeautifulSoup(content, "html.parser")

    def img_tags(self, prefix=None) -> List[Tag]:
        tags = self.soup.select('img[{}]'.format(self.src_attr))
        if prefix:
            return [t for t in tags if t[self.src_attr].startswith(prefix)]
        return tags

    @property
    def images(self):
        img = self.soup.find_all(src=re.compile(r'\.(png|jpe?g|gif)$'))
        return [i['src'] for i in img]

    @property
    def codacy_grade(self):
        for img in self.img_tags(self.codacy_prefix):
            r = requests.get(img[self.src_attr])
            soup = BeautifulSoup(r.text, 'html.parser')
            for text in soup.find_all('text'):
                if len(text.text.strip()) == 1:
                    return text.text.strip()

    @property
    def coveralls_grade(self):
        for img in self.img_tags(self.coveralls_prefix):
            # Coveralls URL are in the form of
            # https://s3.amazonaws.com/assets.coveralls.io/badges/coveralls_83.svg
            # We need to parse out the '83' here
            r = requests.get(img[self.src_attr])
            return int(re.search(r'(\d{1,2})\.svg', r.url).group(1))

    @property
    def travis_status(self):
        for img in self.img_tags(self.travis_prefix):
            r = requests.get(img[self.src_attr])
            soup = BeautifulSoup(r.text, 'html.parser')
            for text in soup.find_all('text'):
                if text.text.strip() != 'build':
                    return text.text.strip()

    @property
    def title(self):
        h1 = self.soup.find('h1')
        if h1:
            return h1.text.strip()
        return ''
