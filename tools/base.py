from pathlib import Path

class Tool:
    def find_replacements(self, content, config):
        """Return list of (old, new) replacement tuples"""
        raise NotImplementedError
        
    def get_workflow_files(self, repo_path):
        """Return list of workflow files to process"""
        return Path(repo_path).glob('.github/workflows/*.y*ml')