import requests
import requests.exceptions
import os

from config import *
from github import Github
from parsers import GradleParser, ReadmeParser
from decorators import lazy_property


def parse_project_id(project_id: str):
    # Parse out project IDs (ie. org names) like 'CS2103AUG2016-W10-C4'
    # into machine readable components

    # The 15th character is the day of week of the tutorials
    d = project_id[14]
    # W = Wednesday, T = Thursday, F = Friday
    if d == 'W':
        day = 2
    elif d == 'T':
        day = 3
    elif d == 'F':
        day = 4
    else:
        raise Exception('Day not found in ' + project_id)

    # Tutorial number (9-15)
    tutorial = int(project_id[15:17])

    # Group number (1-4)
    group = int(project_id[19])

    return day, tutorial, group


class Project:
    image_dir = 'projects'

    """
    Represents a single CS2103/T project.
    """
    def __init__(self, github: Github, org: str, repo_name: str=REPO_NAME):
        self.org = org
        self.repo_name = repo_name
        self.github = github
        self.repo = self.github.get_repo(self.org, self.repo_name)

    @property
    def day(self):
        return self.order[0]

    @property
    def tutorial_number(self):
        return self.order[1]

    @property
    def group_number(self):
        return self.order[2]

    @property
    def order(self):
        return parse_project_id(self.org)

    @property
    def is_forked(self):
        return self.repo['fork']

    @property
    def title(self):
        return OVERRIDE['TITLE'].get(self.org, self.readme.title)

    @property
    def images(self):
        return list(filter(lambda f: f.startswith(self.org), os.listdir(self.image_dir)))

    @lazy_property
    def _gradle(self):
        file = OVERRIDE['GRADLE_LOCATION'].get(self.org, self.repo.gradle)
        gradle_file = self.repo.get_file(file)
        return GradleParser(gradle_file)

    @lazy_property
    def readme(self):
        readme_file = self.repo.get_readme()
        return ReadmeParser(readme_file)

    @lazy_property
    def dependencies(self):
        try:
            dependencies = set(self._gradle.dependencies)
            return dependencies - set(PARENT_DEPENDENCIES)
        except requests.exceptions.HTTPError:
            print('Cannot find build.gradle')
            return set()

    @lazy_property
    def commits(self):
        return self.repo.get_commits(since=COMMITS_SINCE)

    @lazy_property
    def members(self):
        contributors = {}
        for commit in self.commits:
            # Some commits are done using email addresses not associated with a Github account
            # In that case both author and committer are not available. We'll ignore these cases.
            if not commit.contributor:
                continue

            if commit.contributor not in contributors:
                contributors[commit.contributor] = commit['author']

        # Remove all contributors from the parent project
        return {k: v for k, v in contributors.items() if k not in PARENT_CONTRIBUTORS}

    def download_images(self):
        base = '{}/{}'.format(self.image_dir, self.org)
        for i, img in enumerate(self.readme.images):
            name, ext = os.path.splitext(img)
            download_path = '{}_{}{}'.format(base, i, ext)
            try:
                self.github.download_file(self.repo['full_name'], img, download_path)
            except requests.exceptions.HTTPError as e:
                print(e)
