from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class Config:
    github_token: str
    source_org: str
    fork_org: str
    branch_name: str
    pr_title: str
    tool: str
    work_dir: str = './work'

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            return cls(**yaml.safe_load(f))