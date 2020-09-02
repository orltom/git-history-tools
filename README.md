![](https://github.com/orltom/git-history-tools/workflows/Ansible%20Ubuntu%20Check/badge.svg)
[![MIT License](https://raw.githubusercontent.com/orltom/git-history-tools/master/.github/license.svg?sanitize=true)](https://github.com/orltom/git-history-tools/blob/master/LICENSE)

# git-history-tools
Command line tool to group commits by user for a specific time window.

```bash
>>./cli.py --help
cli.py

Description:
  Group GIT commits by user and show changes in a compact mode

Usage:
  cli.py <path> [-b <name>] [-i <regex>] [-d <number>]

Options:
  -h --help                     Show this screen.
  -b --branch <name>            GIT branch name [default: master]
  -i --issue <regex>            Regex pattern which correspond the issue ID. [default: ""]
  -d --deep <number>            change file deep [default: 1]
  <path>                        GIT repository path.
```