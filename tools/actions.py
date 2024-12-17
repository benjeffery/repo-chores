from .base import Tool
from github_utils import get_latest_version
from ruamel.yaml import YAML

class UpdateActions(Tool):
    def find_replacements(self, content, config):
        yaml = YAML()
        data = yaml.load(content)
        replacements = []
        
        def process_data(data):
            if isinstance(data, dict):
                if 'uses' in data and '@' in data['uses']:
                    full_ref = data['uses']
                    action_ref, current_version = full_ref.split('@')
                    if latest := get_latest_version(action_ref, config.github_token):
                        if current_version != latest:
                            replacements.append((
                                f"{action_ref}@{current_version}\n",
                                f"{action_ref}@{latest}\n"
                            ))
                            
                for value in data.values():
                    process_data(value)
            elif isinstance(data, list):
                for item in data:
                    process_data(item)
                    
        process_data(data)
        return replacements
