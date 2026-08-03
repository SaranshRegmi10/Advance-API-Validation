import requests
from config.env_config import Config

class BaseClient:
    def __init__(self):
        # Dynamically pulls base URL and timeout from Config
        self.base_url = Config.BASE_URL
        self.timeout = Config.API_TIMEOUT
        
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key":Config.API_KEY
        })

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        
        # Pass configured timeout if not specified in kwargs
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
            
        return self.session.request(method, url, **kwargs)
        
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)