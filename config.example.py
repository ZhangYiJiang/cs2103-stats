import datetime

# Using a personal Github Oauth token, we can lift the restrictive
# unauthenticated rate limit on requests to Github's API
# See: https://github.com/settings/tokens and
#   https://developer.github.com/v3/#rate-limiting
GITHUB_TOKEN = 'YOUR TOKEN HERE'


# Your Github username, which is required to be embedded as part of the user
# agent string and for authentication
# See: https://developer.github.com/v3/#user-agent-required
GITHUB_USERNAME = 'YOUR USERNAME HERE'


# A list of project orgs to scrape from. They have the common format of
# CS2103AUG2016-W10 [(module)(semester)-(tutorial code)-(group code)]
GITHUB_ORGS = [
    "CS2103AUG2016-T10-C4",
    "CS2103AUG2016-T14-C4",
    "CS2103AUG2016-T16-C3",
    "CS2103AUG2016-F09-C1",
    "CS2103AUG2016-F09-C2",
    "CS2103AUG2016-F09-C3",
    "CS2103AUG2016-F09-C4",
    "CS2103AUG2016-F10-C1",
    "CS2103AUG2016-F10-C2",
    "CS2103AUG2016-F10-C3",
    "CS2103AUG2016-F10-C4",
    "CS2103AUG2016-F11-C1",
    "CS2103AUG2016-F11-C2",
    "CS2103AUG2016-F11-C3",
    "CS2103AUG2016-F11-C4",
    "CS2103AUG2016-T09-C1",
    "CS2103AUG2016-T09-C2",
    "CS2103AUG2016-T09-C3",
    "CS2103AUG2016-T09-C4",
    "CS2103AUG2016-T10-C1",
    "CS2103AUG2016-T10-C2",
    "CS2103AUG2016-T10-C3",
    "CS2103AUG2016-T11-C1",
    "CS2103AUG2016-T11-C2",
    "CS2103AUG2016-T11-C3",
    "CS2103AUG2016-T11-C4",
    "CS2103AUG2016-T13-C1",
    "CS2103AUG2016-T13-C2",
    "CS2103AUG2016-T13-C3",
    "CS2103AUG2016-T13-C4",
    "CS2103AUG2016-T14-C1",
    "CS2103AUG2016-T14-C2",
    "CS2103AUG2016-T14-C3",
    "CS2103AUG2016-T15-C1",
    "CS2103AUG2016-T15-C2",
    "CS2103AUG2016-T15-C3",
    "CS2103AUG2016-T15-C4",
    "CS2103AUG2016-T16-C1",
    "CS2103AUG2016-T16-C2",
    "CS2103AUG2016-T16-C4",
    "CS2103AUG2016-T17-C1",
    "CS2103AUG2016-T17-C2",
    "CS2103AUG2016-T17-C3",
    "CS2103AUG2016-W09-C1",
    "CS2103AUG2016-W09-C2",
    "CS2103AUG2016-W09-C3",
    "CS2103AUG2016-W09-C4",
    "CS2103AUG2016-W10-C1",
    "CS2103AUG2016-W10-C2",
    "CS2103AUG2016-W10-C3",
    "CS2103AUG2016-W10-C4",
    "CS2103AUG2016-W11-C2",
    "CS2103AUG2016-W11-C3",
    "CS2103AUG2016-W11-C4",
    "CS2103AUG2016-W13-C1",
    "CS2103AUG2016-W13-C2",
    "CS2103AUG2016-W13-C3",
    "CS2103AUG2016-W13-C4",
    "CS2103AUG2016-W14-C1",
    "CS2103AUG2016-W14-C2",
    "CS2103AUG2016-W14-C3",
    "CS2103AUG2016-W14-C4",
    "CS2103AUG2016-W15-C2",
    "CS2103AUG2016-W15-C3",
    "CS2103AUG2016-W15-C4",
]

# All project repository share the same name
REPO_NAME = 'main'

# Since projects are forked from the original repo, we only count commits
# from the project's start date
COMMITS_SINCE = datetime.datetime(2016, 9, 30, 0, 0, 0).isoformat()

# Contributors to the original repo, which are used to exclude
PARENT_CONTRIBUTORS = [
    "damithc",
    "m133225",
    "yl-coder",
    "pyokagan",
    "lejolly",
    "ndt93",
    "YijinL",
    "okkhoy",
    "edmundmok",
    "zzzzwen",
    "MightyCupcakes",
    "chao1995",
    "jia1",
    "mauris",
]

CACHE_PATH = 'cache'

# Week number of the week before start of the project and length of project in weeks
PROJECT_START_WEEK = 38
PROJECT_LENGTH_WEEK = 7
