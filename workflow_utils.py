from github_utils import get_latest_version
from ruamel.yaml import YAML
from pathlib import Path
import difflib
import click
from config import Config
from tools import TOOLS

def process_workflows(repo_path, config):
    tool = TOOLS[config.tool]
    changes = []
    
    for workflow in tool.get_workflow_files(repo_path):
        with workflow.open() as f:
            content = f.read()
        
        if replacements := tool.find_replacements(content, config):
            updated = content
            for old, new in replacements:
                updated = updated.replace(old, new)
                
            if updated != content:
                workflow.write_text(updated)
                changes.append((workflow.name, generate_diff(content, updated, workflow.name)))
    
    return changes

def generate_diff(original, updated, workflow_name):
    """Returns a colored diff string for terminal display"""
    diff_lines = []
    for line in difflib.unified_diff(
        original.splitlines(),
        updated.splitlines(),
        fromfile=workflow_name,
        tofile=workflow_name,
        lineterm=''
    ):
        if line.startswith('+'):
            diff_lines.append(click.style(line, fg='green'))
        elif line.startswith('-'):
            diff_lines.append(click.style(line, fg='red'))
        elif line.startswith('^'):
            diff_lines.append(click.style(line, fg='blue'))
        else:
            diff_lines.append(line)
            
    return '\n'.join(diff_lines)