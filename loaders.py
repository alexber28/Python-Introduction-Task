import json
from abc import ABC, abstractmethod

# This is an Abstract Base Class (like an Interface in Java)
class BaseLoader(ABC):
    @abstractmethod
    def load(self, file_path):
        pass

class JSONLoader(BaseLoader):
    def load(self, file_path):
        """Reads a JSON file and returns a list of dictionaries."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return []
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {file_path}")
            return []
