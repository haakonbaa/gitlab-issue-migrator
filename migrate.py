#!/bin/python

import sys
import requests
import pandas as pd


USAGE = """GitLab to GitHub issue migrator
USAGE:
  migrate.py -r <repo> -o <owner> -t <token> <file>
  
  -r | --repo   <repo>    repository name
  -o | --owner  <owner>   account owner of repo
  -t | --token  <token>   github token
  <file>                  csv file name

The <file> argument is the filename of the csv file
Downloaded from GitLab. See https://github.com/settings/tokens
for token generation."""

GITLABINFO = """
### This issue was automatically migrated from GitLab

[issue #{Issue ID}]({URL})

|Author|Created At (UTC)|Assignee|
|-|-|-|
|{Author} ({Author Username})|{Created At (UTC)}|{Assignee} ({Assignee Username})|"""


def main():
    # parse arguments

    repo, owner, token, file = None, None, None, None

    args = sys.argv[1:]
    while len(args) != 0:
        match args[0:2]:
            case ['-r' | '--repo', arg_repo]:
                repo = arg_repo
                args = args[2:]
            case ['-o' | '--owner', arg_owner]:
                owner = arg_owner
                args = args[2:]
            case ['-t' | '--token', arg_token]:
                token = arg_token
                args = args[2:]
            case ['-h' | '--help' | 'help']:
                print(USAGE, file=sys.stdout)
                exit(0)
            case [arg_file]:
                file = arg_file
                args = args[1:]
            case _:
                print(USAGE, file=sys.stderr)
                exit(1)

    # make sure arguments are valid

    for var in [repo, owner, token, file]:
        if var is None:
            print(f'Missing argument\n', file=sys.stderr)
            print(USAGE, file=sys.stderr)
            exit(1)

    # parse csv file

    try:
        csv_data = pd.read_csv(file, dtype=str, na_filter=False)
    except FileNotFoundError as err:
        print(err, file=sys.stderr)
        exit(1)

    # iterate through rows and update issues

    for row in csv_data.iterrows():
        data = row[1]

        issue = {
            'title': '',
            'body': '',
            'assignees': [],
            'labels': []
        }

        # migrating the assignees only succeeds if the GitLab
        # username happens to correspond to the GitHub username.
        # Therefore, don't bother adding assignees :(

        title = data['Title']
        if title != '':
            issue['title'] = title

        desc = data['Description']
        if desc != '':
            issue['body'] = desc

        labels = data['Labels']
        if labels != '':
            labels = labels.split(',')
            issue['labels'] = labels

        issue['body'] += GITLABINFO.format(**data)

        # upload to GitHub
        res = requests.post(
            f'https://api.github.com/repos/{owner}/{repo}/issues',
            headers={
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {token}',
                'X-GitHub-Api-Version': '2022-11-28'
            },
            json=issue)

        if str(res.status_code)[0] != '2':
            print(
                f'Error uploading issue ({res.status_code}):\n {res.text}', file=sys.stderr)
            print(f'On issue: {issue["title"]}', file=sys.stderr)
            exit(1)
        else:
            print(f'uploaded: {issue["title"]}')


if __name__ == '__main__':
    main()
