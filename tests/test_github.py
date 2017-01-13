import unittest
from github import Github, strip_params
from .config import *


class StripParamTest(unittest.TestCase):
    def test_strip(self):
        self.assertEqual(
            'https://api.github.com/users/ZhangYiJiang/gists',
            strip_params('https://api.github.com/users/ZhangYiJiang/gists{/gist_id}')
        )

    def test_multiple(self):
        self.assertEqual(
            'https://api.github.com/users/ZhangYiJiang/starred',
            strip_params('https://api.github.com/users/ZhangYiJiang/starred{/owner}{/repo}')
        )

    def test_none(self):
        self.assertEqual(
            'https://api.github.com/users/ZhangYiJiang',
            strip_params('https://api.github.com/users/ZhangYiJiang')
        )


class GithubTest(unittest.TestCase):
    def setUp(self):
        self.github = Github(GITHUB_USERNAME)

    def test_get_repo(self):
        repo = self.github.get_repo('CS2103AUG2016-W10-C4', 'main')
        self.assertTrue(repo['fork'])
        self.assertEqual('main', repo['name'])


class RepoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.github = Github(GITHUB_USERNAME)
        cls.repo = cls.github.get_repo('CS2103AUG2016-W10-C4', 'main')

    def test_get_readme(self):
        readme = self.repo.get_readme()
        self.assertTrue(readme)

    def test_get_gradle(self):
        gradle = self.repo.get_file(self.repo.gradle)
        self.assertTrue(gradle)

    def test_get_commits(self):
        # https://github.com/ZhangYiJiang/addressbook-level1
        repo = self.github.get_repo('ZhangYiJiang', 'addressbook-level1')
        commits = repo.get_commits()
        self.assertEqual(len(commits), 48)
