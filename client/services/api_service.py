import requests
from requests.exceptions import RequestException

class ApiService:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def register_user(self, username: str, password: str) -> dict:
        try:
            payload = {"username": username, "password": password}
            response = requests.post(f"{self.base_url}/auth/register", json=payload)
            if response.status_code in (200, 201):
                return {"success": True, "data": response.json()}
            else:
                detail = response.json().get("detail", "Erro desconhecido")
                return {"success": False, "detail": detail}
        except RequestException as e:
            return {"success": False, "detail": str(e)}

    def login_user(self, username: str, password: str) -> dict:
        try:
            payload = {"username": username, "password": password}
            response = requests.post(f"{self.base_url}/auth/login", json=payload)
            if response.status_code in (200, 201):
                return {"success": True, "data": response.json()}
            else:
                detail = response.json().get("detail", "Erro desconhecido")
                return {"success": False, "detail": detail}
        except RequestException as e:
            return {"success": False, "detail": str(e)}