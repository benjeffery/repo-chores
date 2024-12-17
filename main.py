import click
from pathlib import Path
import subprocess

from config import Config
from github_utils import GithubHelper
from workflow_utils import process_workflows

@click.command()
@click.option('--config', default='config.yaml', help='Path to config file')
def main(config):
    cfg = Config.from_file(config)
    work_dir = Path(cfg.work_dir)
    work_dir.mkdir(exist_ok=True)
    
    github = GithubHelper(cfg)
    org = github.gh.get_organization(cfg.source_org)
    
    for repo in org.get_repos():
        if click.confirm(f"\nProcess {repo.name}?"):
            process_repo(github, repo, work_dir, cfg)

def process_repo(github, repo, work_dir, config):
    print(f"Processing {repo.name}")
    fork = github.ensure_fork_exists(repo)
    
    repo_dir = work_dir / repo.name
    if not repo_dir.exists():
        subprocess.run(['git', 'clone', repo.ssh_url, str(repo_dir)], check=True)
        
    subprocess.run(['git', 'checkout', '-b', config.branch_name], cwd=repo_dir, check=True)
    
    if changes := process_workflows(repo_dir, config):
        print("\nProposed changes:")
        for workflow_name, diff in changes:
            print(f"\n{click.style(workflow_name, bold=True)}:")
            print(diff)
            
        if click.confirm("Create PR with these changes?"):
            subprocess.run(['git', 'add', '.'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'commit', '-m', config.pr_title], 
                         cwd=repo_dir, check=True)
            subprocess.run(['git', 'push', '-u', fork.ssh_url, config.branch_name],
                         cwd=repo_dir, check=True)
            
            github.create_pr(repo, config.branch_name, changes)

if __name__ == '__main__':
    main()