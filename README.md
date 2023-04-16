# GitLab Issue Migrator

Migrate issues from GitLab to GitHub. Migrated issues will look like this:

----
{Original text from GitLab here}

### This issue was automatically migrated from GitLab

[issue #{ID}]()

|Author|Created At (UTC)|Assignee|
|-|-|-|
|{Author} ({Author Username})|{Created At (UTC)}|{Assignee} ({Assignee Username})|"""

---- 

# USAGE
```txt
$ ./migrate.py --help
GitLab to GitHub issue migrator
USAGE:
  migrate.py -r <repo> -o <owner> -t <token> <file>
  
  -r | --repo   <repo>    repository name
  -o | --owner  <owner>   account owner of repo
  -t | --token  <token>   github token
  <file>                  csv file name

The <file> argument is the filename of the csv file
Downloaded from GitLab. See https://github.com/settings/tokens
for token generation.
```

## steps
- Download issues from GitLab repo as CSV
- Create a token on github: [github.com/settings/tokens](https://github.com/settings/tokens)
- Edit the CSV file to include the wanted issues
- Run the script to migrate issues