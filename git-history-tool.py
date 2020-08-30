#!/usr/bin/python3
"""git-history-tool.py

Description:
  Group GIT commits by user and show changed folders

Usage:
  git-history-tool.py <path>

Options:
  -h --help         Show this screen.
  <path>            GIT repository path
"""
from datetime import datetime, timedelta
from git import Repo
from typing import List, Dict
from tabulate import tabulate
from docopt import docopt


class Commit:
    def __init__(self, commit_hash, author, commit_datetime, files=[]):
        self._commit_hash = commit_hash
        self._author = author
        self._datetime = commit_datetime
        self._files = files

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
    def files(self) -> List[str]:
        return self._files


class Summary:
    def __init__(self):
        self._commits = []

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
                    _path = '/'.join(_f.split("/", 3)[0:3])
                _paths.add(_path)
        return '\n'.join(_paths)

    def hashes(self) -> str:
        _hashes = set()
        for _c in self._commits:
            _hashes.add(_c.hash)
        return '\n'.join(_hashes)


class GitUtils:
    @staticmethod
    def get_commits_from_yesterday(rep_path) -> List[Commit]:
        start_date = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d 23:59:59')
        end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        return GitUtils.get_commits_between(rep_path, start_date, end_date)

    @staticmethod
    def get_commits_between(rep_path, since, after) -> List[Commit]:
        _commits = []
        _repo = Repo(rep_path)
        for _c in _repo.iter_commits('master', max_count=300, since=since, after=after):
            _commit = Commit(_c.hexsha, _c.author, _c.committed_datetime, _c.stats.files)
            _commits.append(_commit)
        return _commits

    @staticmethod
    def group_by_user(commits) -> Dict[str, Summary]:
        _summaries_by_user = {}
        for _commit in commits:
            if _commit.author in _summaries_by_user:
                _summary = _summaries_by_user[_commit.author]
                _summary.add(_commit)
                _summaries_by_user[_commit.author] = _summary
            else:
                _summary = Summary()
                _summary.add(_commit)
                _summaries_by_user[_commit.author] = _summary
        return _summaries_by_user


def show_changes_from_yesterday(_path):
    commits = GitUtils.get_commits_from_yesterday(_path)
    changes_by_user = GitUtils.group_by_user(commits)
    table = [[key, changes_by_user[key].show(), changes_by_user[key].hashes()] for key in changes_by_user]
    headers = ["Autor", "Modules", "GIT hash"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    path = arguments['<path>']
    show_changes_from_yesterday(path)
