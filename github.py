import base64
import hashlib
import json
import re
import time
import os
from urllib.parse import urljoin, urlparse

import arrow
import requests
from requests.auth import HTTPBasicAuth

from config import *
from decorators import lazy_property


def strip_params(url: str):
    return re.sub(r'{/[^}]+}', '', url)


class ProxyObject:
    def __init__(self, proxy, github: 'Github'):
        self.raw = proxy
        self.github = github

    def __getitem__(self, item):
        return self.raw[item]

    def __contains__(self, item):
        return item in self.raw


class Commit(ProxyObject):
    @property
    def contributor(self):
        # Some commits are done using email addresses not associated with a Github account
        if self['author']:
            return self['author']['login']
        elif self['committer']:
            return self['committer']['login']
        return None

    @lazy_property
    def time(self):
        if self['commit']['author']:
            return arrow.get(self['commit']['author']['date']).to('Asia/Singapore')
        elif self['commit']['committer']:
            return arrow.get(self['commit']['committer']['date']).to('Asia/Singapore')
        raise Exception('Date not found on commit')


class Repo(ProxyObject):
    """
    A git repository on Github. This class proxies a Github repo API JSON object.
    See https://developer.github.com/v3/repos/#get for all properties available
    """
    gradle = 'build.gradle'

    def get_readme(self):
        return self.github.get_readme(self['full_name'])

    def get_file(self, path):
        return self.github.get_content(self['full_name'], path)

    def get_commits(self, **kwargs):
        commit_url = strip_params(self['commits_url'])

        commits = []
        for commit in self.github.get_all(commit_url, params=kwargs):
            c = Commit(commit, self.github)
            if c.contributor not in PARENT_CONTRIBUTORS:
                commits.append(c)

        return commits


class Github:
    base_url = 'https://api.github.com'

    def __init__(self, username, token=None):
        self.username = username
        self.token = token

    def _headers(self, **kwargs):
        additional_headers = {}
        if 'headers' in kwargs:
            additional_headers = kwargs['headers']

        headers = {
            **additional_headers,
            # User agent is required - see: https://developer.github.com/v3/#user-agent-required
            'user-agent': self.username,
        }

        return headers

    def _auth(self):
        if not self.token:
            return None
        return HTTPBasicAuth(self.username, self.token)

    def _cache_path(self, url: str):
        hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        return CACHE_PATH + '/' + hash

    def _read_cache(self, url: str):
        try:
            with open(self._cache_path(url), encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None

    def _write_cache(self, url: str, content):
        with open(self._cache_path(url), encoding='utf-8', mode='w') as f:
            f.write(content)

    def normalize(self, url):
        # Ensure the endpoint is an absolute URL (ie. starts with the api.github.com base URL)
        if not url.startswith(self.base_url):
            return urljoin(self.base_url, url)
        else:
            return url

    def get(self, endpoint, params: dict=None, **kwargs):
        if params is None:
            params = {}

        url = self.normalize(endpoint)

        # Try getting the file from cache
        content = self._read_cache(url)
        if content:
            content = json.loads(content)
        else:
            r = requests.get(url, params=params, headers=self._headers(**kwargs), auth=self._auth())

            # Wait and retry if we run foul of the rate limiter
            # TODO: Use time provided in the response header instead of system time
            if r.status_code == 403 and int(r.headers['X-RateLimit-Remaining']) == 0:
                reset = int(r.headers['X-RateLimit-Reset'])
                wait = time.time() - reset + 3
                print('! Hit rate limit, waiting {} seconds'.format(wait))
                time.sleep(wait)
                return self.get(endpoint)

            # Die here if the request failed so we don't get further weirdness down the line
            r.raise_for_status()

            if 'raw' in kwargs and kwargs['raw']:
                content = r.text
            else:
                content = r.json()

                # Handle paginated endpoints
                if isinstance(content, list):
                    content = {
                        'pagination': r.links,
                        'content': content,
                    }

            # Cache the result
            self._write_cache(url, json.dumps(content))

        return content

    def get_all(self, endpoint, params: dict=None):
        if params is None:
            params = {}

        params['per_page'] = 100

        r = self.get(endpoint, params)
        content = r['content']
        while 'next' in r['pagination']:
            endpoint = r['pagination']['next']['url']
            r = self.get(endpoint)
            content.extend(r['content'])

        return content

    def _decode_content(self, json):
        if json['encoding'] == 'base64':
            bytes = base64.b64decode(json['content'])
            return bytes.decode('utf-8')
        else:
            raise Exception('Encoding not recognized')

    def get_repo(self, user, name):
        return Repo(self.get('repos/{}/{}'.format(user, name)), self)

    def get_readme(self, repo):
        return self.get('repos/{}/readme'.format(repo), raw=True, headers={
            'accept': 'application/vnd.github.v3.html',
        })

    def download_file(self, repo, path, download_path, overwrite=False):
        if not overwrite and os.path.exists(download_path):
            return

        # Don't use Github API if the path is absolute
        if urlparse(path).scheme:
            r = requests.get(path, stream=True)
        else:
            url = self.normalize('repos/{}/contents/{}'.format(repo, path))
            headers = self._headers(headers={
                'accept': 'application/vnd.github.v3.raw'
            })
            r = requests.get(url, stream=True, headers=headers, auth=self._auth())

        r.raise_for_status()

        with open(download_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

    def get_content(self, repo, path):
        r = self.get('repos/{}/contents/{}'.format(repo, path))
        return self._decode_content(r)
