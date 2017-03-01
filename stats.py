import arrow
from collections import OrderedDict, Counter, defaultdict
from pprint import pprint

from config import *
from github import Github
from project import Project, parse_project_id
from decorators import lazy_property
from operator import itemgetter


github = Github(GITHUB_USERNAME, GITHUB_TOKEN)


class Stats:
    def __init__(self, github: Github, projects):
        self.github = github
        self.projects = OrderedDict()

        for org in sorted(projects, key=parse_project_id):
            self.projects[org] = Project(github, org)

    @lazy_property
    def commits(self):
        # Sort the commits by commit time
        commits = []
        for project in self.projects.values():
            commits.extend(project.commits)
        commits.sort(key=lambda c: arrow.get(c['commit']['author']['date']))
        return commits

    def download_images(self):
        for name, project in self.projects.items():
            print('{} - {} image'.format(name, len(project.readme.images)))
            project.download_images()

    def analyze_dependencies(self):
        count = Counter()
        popularity = Counter()
        for name, project in self.projects.items():
            count[len(project.dependencies)] += 1
            for dep in project.dependencies:
                popularity[dep] += 1
        return count, popularity

    def analyze_commit_timing(self):
        counts = defaultdict(Counter)
        for project in self.projects.values():
            for commit in project.commits:
                counts[project.day][(commit.time.weekday(), commit.time.hour)] += 1

        # Reorder by hour
        for tutorial_day in counts.keys():
            commits_by_hour = {}
            for day in range(7):
                for hour in range(24):
                    key = (day, hour)
                    commits_by_hour[key] = counts[tutorial_day].get(key, 0)
            counts[tutorial_day] = commits_by_hour

        return counts

    def analyze_commit_week(self):
        count = Counter()
        for commit in self.commits:
            week = commit.time.week - PROJECT_START_WEEK
            if 0 < week <= PROJECT_LENGTH_WEEK:
                count[week] += 1
        return count

    def project_commits(self):
        count = defaultdict(list)
        for project in self.projects.values():
            count[len(project.members)].append(len(project.commits))
        return count

stats = Stats(github, GITHUB_ORGS)
