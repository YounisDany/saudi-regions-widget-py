import json
import os
import requests
from typing import Dict, Any

class DataLoader:
    def __init__(self, data_url: str, data_level: str):
        self.data_url = data_url
        self.data_level = data_level
        self.data = None

    def load_data(self) -> Dict[str, Any]:
        data_file = f"{self.data_level}.min.json"
        url = os.path.join(self.data_url, data_file)
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            self.data = response.json()
            return self.data
        except requests.exceptions.RequestException as e:
            print(f"Error loading data from {url}: {e}")
            raise

    def get_data(self) -> Dict[str, Any]:
        if self.data is None:
            self.load_data()
        return self.data

