from github import Github
import re
import requests

def get_latest_version(action_ref, token):
    owner, repo = action_ref.split('/')
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/repos/{owner}/{repo}/releases'
    
    response = requests.get(url, headers=headers)
    if not response.ok:
        print(f"Failed to fetch releases for {action_ref}: {response.status_code}")
        return None
        
    releases = response.json()
    if not isinstance(releases, list) or not releases:
        return None
        
    return releases[0]['tag_name']

class GithubHelper:
    def __init__(self, config):
        self.gh = Github(config.github_token)
        self.config = config
        
    def ensure_fork_exists(self, repo):
        try:
            return self.gh.get_repo(f"{self.config.fork_org}/{repo.name}")
        except:
            return repo.create_fork()
            
    def create_pr(self, source_repo, branch, changes):
        title = self.config.pr_title
        body = ""
        
        return source_repo.create_pull(
            title=title,
            body=body,
            head=f"{self.config.fork_org}:{branch}",
            base="main"
        )