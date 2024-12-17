from .base import Tool
from ruamel.yaml import YAML

class UbuntuVersion(Tool):
    def find_replacements(self, content, config):
        yaml = YAML()
        data = yaml.load(content)
        replacements = []
        
        def process_data(data):
            if isinstance(data, dict):
                if 'runs-on' in data and isinstance(data['runs-on'], str):
                    if data['runs-on'].startswith('ubuntu-'):
                        current = data['runs-on']
                        replacements.append((
                            f"runs-on: {current}\n",
                            f"runs-on: ubuntu-24.04\n"
                        ))
                        
                # Look for matrix entries
                if 'matrix' in data:
                    matrix = data['matrix']
                    if isinstance(matrix, dict):
                        for key in ['os', 'operating-system']:  # common matrix names
                            if key in matrix and isinstance(matrix[key], list):
                                for i, os in enumerate(matrix[key]):
                                    if isinstance(os, str) and os.startswith('ubuntu-'):
                                        replacements.append((
                                            f"ubuntu-{os.split('-')[1]}",  # match just the ubuntu-* part
                                            "ubuntu-24.04"
                                        ))
                
                for value in data.values():
                    process_data(value)
            elif isinstance(data, list):
                for item in data:
                    process_data(item)
                    
        process_data(data)
        return replacements