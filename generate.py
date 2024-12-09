import argparse
import os
from datetime import datetime
from datetime import timedelta
from subprocess import Popen
import sys

# Predefined commit data: date (as string) -> number of commits
commit_dates = {
    "2024-05-11": 1,
    "2024-05-16": 3,
    "2024-05-29": 4,
    "2024-06-05": 2,
    "2024-06-06": 5,
    "2024-06-12": 1,
    "2024-06-15": 2,
    "2024-06-17": 3,
    "2024-06-19": 1,
    "2024-06-20": 1,
    "2024-07-08": 4,
    "2024-07-17": 1,
    "2024-07-18": 1,
    "2024-07-22": 1,
    "2024-07-23": 1,
    "2024-07-29": 1,
    "2024-07-30": 1,
    "2024-07-31": 4,
    "2024-08-01": 1,
    "2024-08-05": 2,
    "2024-08-09": 2,
    "2024-08-12": 5,
    "2024-08-13": 1,
    "2024-08-16": 1,
    "2024-08-26": 1,
    "2024-08-27": 7,
    "2024-08-29": 1,
    "2024-09-02": 1,
    "2024-09-03": 3,
    "2024-09-04": 1,
    "2024-09-11": 4,
    "2024-09-12": 1,
    "2024-09-17": 1,
    "2024-09-19": 6,
    "2024-09-23": 1,
    "2024-09-26": 1,
    "2024-10-04": 3,
    "2024-10-07": 5,
    "2024-10-08": 3,
    "2024-10-09": 5,
    "2024-10-10": 2,
    "2024-10-19": 4,
    "2024-10-21": 5,
    "2024-10-22": 1,
    "2024-10-25": 7,
    "2024-10-28": 2,
    "2024-10-29": 1,
    "2024-10-30": 5,
    "2024-10-31": 2,
    "2024-11-01": 3,
    "2024-11-05": 4,
    "2024-11-06": 3,
    "2024-11-07": 2,
    "2024-11-09": 3,
    "2024-11-12": 3,
    "2024-11-13": 1,
    "2024-11-18": 1,
    "2024-11-19": 4,
    "2024-11-20": 1,
}

def main(def_args=sys.argv[1:]):
    args = arguments(def_args)
    curr_date = datetime.now()
    directory = 'repository-' + curr_date.strftime('%Y-%m-%d-%H-%M-%S')
    repository = args.repository
    user_name = args.user_name
    user_email = args.user_email
    if repository is not None:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        directory = repository[start:end]
    os.mkdir(directory)
    os.chdir(directory)
    run(['git', 'init', '-b', 'main'])

    if user_name is not None:
        run(['git', 'config', 'user.name', user_name])

    if user_email is not None:
        run(['git', 'config', 'user.email', user_email])

    for date_str, num_commits in commit_dates.items():
        commit_date = datetime.strptime(date_str, '%Y-%m-%d')
        for commit_time in (commit_date + timedelta(minutes=m) for m in range(num_commits)):
            contribute(commit_time)

    if repository is not None:
        run(['git', 'remote', 'add', 'origin', repository])
        run(['git', 'branch', '-M', 'main'])
        run(['git', 'push', '-u', 'origin', 'main'])

    print('\nRepository generation ' +
          '\x1b[6;30;42mcompleted successfully\x1b[0m!')

def contribute(date):
    with open(os.path.join(os.getcwd(), 'README.md'), 'a') as file:
        file.write(message(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '"%s"' % message(date),
         '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])

def run(commands):
    Popen(commands).wait()

def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M')

def arguments(argsval):
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repository', type=str, required=False,
                        help="""A link on an empty non-initialized remote git
                        repository. If specified, the script pushes the changes
                        to the repository. The link is accepted in SSH or HTTPS
                        format. For example: git@github.com:user/repo.git or
                        https://github.com/user/repo.git""")
    parser.add_argument('-un', '--user_name', type=str, required=False,
                        help="""Overrides user.name git config.
                        If not specified, the global config is used.""")
    parser.add_argument('-ue', '--user_email', type=str, required=False,
                        help="""Overrides user.email git config.
                        If not specified, the global config is used.""")
    return parser.parse_args(argsval)

if __name__ == "__main__":
    main()
