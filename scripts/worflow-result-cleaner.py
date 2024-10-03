#!/usr/bin/env python3
from github import Auth, Github
import argparse
import os

def check_env_vars():
    if not os.getenv('GITHUB_TOKEN'):
        raise ValueError('GITHUB_TOKEN is missing')

# Parse following arguments with argparse: -r repository -n keep_last_n -w workflow
def parse_args():
    parser = argparse.ArgumentParser(description='Clean up old workflow runs')
    parser.add_argument('-r', '--repository', required=True, help='Repository name')
    parser.add_argument('-n', '--keep_last_n', required=True, help='Keep last n workflow runs')
    parser.add_argument('-w', '--workflow', help='Workflow name')
    return parser.parse_args()

def main():
    check_env_vars()
    args = parse_args()
    auth = Auth.Token(os.getenv('GITHUB_TOKEN'))
    gh = Github(auth=auth)
    repo = gh.get_repo(args.repository)
    workflows = repo.get_workflows()
    for wf in workflows:
        print(f"Processing workflow {wf.name}")
        if args.workflow and wf.name != args.workflow:
            continue
        runs = wf.get_runs()
        runs = sorted(runs, key=lambda x: x.created_at, reverse=True)
        print(f"Found {len(runs)} runs")
        for run in runs[int(args.keep_last_n):]:
            run.delete()
            print(f"Deleted run {run.id}")
    
    #runs = workflow.get_runs()
    #runs = sorted(runs, key=lambda x: x.created_at, reverse=True)
    #for run in runs[int(args.keep_last_n):]:
    #    run.delete()
    #    print(f"Deleted run {run.id}")

if __name__ == '__main__':
    main()
    