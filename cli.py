#!/usr/bin/python3
"""cli.py

Description:
  Group GIT commits by user and show changes in a compact mode

Usage:
  cli.py [-b <name>] [-i <regex>] [-d <number>] [--since date] [--after date] <path>

Options:
  -h --help                     Show this screen.
  -b --branch <name>            GIT branch name [default: master]
  -i --issue <regex>            Regex pattern which correspond the issue ID. [default: ""]
  -d --deep <number>            change file deep [default: 1]
  --since <date>                Start date: format (%Y-%m-%d). Default is today -1
  --after <date>                End date: format (%Y-%m-%d). Default is today -2
  <path>                        GIT repository path.
"""
from datetime import datetime, timedelta
from git import Repo
from typing import List, Dict
from tabulate import tabulate
from docopt import docopt
import re


class Commit:
    def __init__(self, commit_hash, author, commit_datetime, msg, files=[]):
        self._commit_hash = commit_hash
        self._author = author
        self._datetime = commit_datetime
        self._files = files
        self._msg = msg

    def __str__(self):
        return f"{self._datetime} {self._commit_hash} {self._author}"

    @property
    def hash(self) -> str:
        return self._commit_hash

    @property
    def author(self) -> str:
        return self._author

    @property
    def datetime(self) -> str:
        return self._datetime

    @property
    def msg(self) -> str:
        return self._msg

    @property
    def files(self) -> List[str]:
        return self._files


class Summary:
    def __init__(self, pattern, deep):
        self._commits = []
        self._pattern = pattern
        self._deep = deep

    def add(self, commit):
        self._commits.append(commit)

    def show(self) -> str:
        _paths = set()
        for _c in self._commits:
            for _f in _c.files:
                count = _f.count('/')
                if count < 3:
                    _path = _f[0:_f.index('/')]
                else:
                    _path = '/'.join(_f.split("/", _deep)[0:_deep])
                _paths.add(_path)
        return '\n'.join(_paths)

    def msg(self) -> str:
        _messages = set()
        for _c in self._commits:
            match = self._pattern.search(_c.msg)
            if match:
                _short_msg = match.group(0)
            else:
                _short_msg = "NOT FOUND"
            _messages.add(_short_msg)
        return '\n'.join(_messages)

    def hashes(self) -> str:
        _hashes = set()
        for _c in self._commits:
            _hashes.add(_c.hash)
        return '\n'.join(_hashes)


class GitUtils:
    @staticmethod
    def get_commits_between(rep_path, branch, since, after) -> List[Commit]:
        _commits = []
        _repo = Repo(rep_path)
        for _c in _repo.iter_commits(branch, max_count=300, since=since, after=after):
            _commit = Commit(_c.hexsha, _c.author, _c.committed_datetime, _c.message, _c.stats.files)
            _commits.append(_commit)
        return _commits

    @staticmethod
    def group_by_user(commits, pattern, deep) -> Dict[str, Summary]:
        _summaries_by_user = {}
        for _commit in commits:
            if _commit.author in _summaries_by_user:
                _summary = _summaries_by_user[_commit.author]
                _summary.add(_commit)
                _summaries_by_user[_commit.author] = _summary
            else:
                _summary = Summary(pattern, deep)
                _summary.add(_commit)
                _summaries_by_user[_commit.author] = _summary
        return _summaries_by_user


def show(path, branch, pattern, deep, since, after):
    commits = GitUtils.get_commits_between(path, branch, since, after)
    changes_by_user = GitUtils.group_by_user(commits, pattern, deep)
    table = [
        [key, changes_by_user[key].show(), changes_by_user[key].msg(), changes_by_user[key].hashes()]
        for key in changes_by_user
    ]
    headers = ["Author", "Modules", "Issue", "GIT hash"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    _path = arguments['<path>']
    _branch = arguments['--branch']
    _issue_pattern = re.compile(arguments['--issue'])
    _deep = int(arguments['--deep'])
    _since = arguments['--since']
    _after = arguments['--after']
    if _since is None:
        _start_date = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d 00:00:00')
    else:
        _start_date = datetime.strptime(_since, '%Y-%m-%d')
    if _after is None:
        _end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        _end_date = datetime.strptime(_after, '%Y-%m-%d')
    show(_path, _branch, _issue_pattern, _deep, _start_date, _end_date)
