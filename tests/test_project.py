from project import Project
from github import Github
import unittest

from config import *


class ProjectTest(unittest.TestCase):
    def setUp(self):
        self.github = Github(GITHUB_USERNAME)
        self.project = Project(self.github, 'CS2103AUG2016-W10-C4', 'main')

    def test_download_image(self):
        self.project.download_images()
