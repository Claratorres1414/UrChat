import requests
from requests.exceptions import RequestException
import threading
import websocket

class ApiService:
    def __init__(self, base_url: str, base_ws_url: str):
        self.base_url = base_url.rstrip('/')
        self.base_ws_url = base_ws_url.rstrip('/')

    def list_contacts(self):
        try:
            response = requests.get(f'{self.base_url}/users/contacts')
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print("Erro na requisição list_contacts", e)
            return []

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

    def connect_user(self, token: str):
        ws_url = f"{self.base_ws_url}{token}"

        def run_ws():
            try:
                ws = websocket.WebSocket()
                ws.connect(ws_url)
                print("Conexão WebSocket estabelecida com o servidor!")
            except Exception as e:
                print("Erro na conexão: ", e)

        threading.Thread(target=run_ws, daemon=True).start()
        print("Thread WebSocket inicializada em background")