import json
import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json" 
        }

    def get(self, endpoint, data = None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, data = json.dumps(data), headers=self.headers)
        return eval(response.content.decode())

    def put(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, data=json.dumps(data), headers=self.headers)
        return response.content.decode()

    def list(self, endpoint, data = None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, data = json.dumps(data), headers=self.headers)
        return eval(response.content.decode())

    def search(self, endpoint, data = None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, data = json.dumps(data), headers=self.headers)
        return eval(response.content.decode())


class MockClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json" 
        }

    def get(self, endpoint, data = None):
        return [["localhost"]]

    def put(self, endpoint, data):
        return "localhost"

    def list(self, endpoint, data = None):
        return "localhost"

    def search(self, endpoint, data = None):
        return "localhost"
