import time
import requests
from requests.exceptions import RequestException
import threading
import websocket

class ApiService:
    def __init__(self, base_url: str, base_ws_url: str):
        self.base_url = base_url.rstrip('/')
        self.base_ws_url = base_ws_url.rstrip('/')
        self.contacts_map = {}
        self.ws = None
        self.ws_thread = None
        self.keep_running = False
        self.on_message = None
        self.user_id = None

    def list_contacts(self):
        try:
            response = requests.get(f'{self.base_url}/users/contacts')
            response.raise_for_status()
            contacts = response.json()
            self.contacts_map = {c["id"]: c["username"] for c in contacts}
            return contacts
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
                access_token = response.json()["access_token"]

                headers = {
                    "token": access_token
                }

                try:
                    user = requests.get(f"{self.base_url}/users/currentUser", headers=headers)
                    self.user_id = user.json()["id"]
                except RequestException as e:
                    return {"success": False, "detail": str(e)}
                return {"success": True, "data": response.json()}
            else:
                detail = response.json().get("detail", "Erro desconhecido")
                return {"success": False, "detail": detail}
        except RequestException as e:
            return {"success": False, "detail": str(e)}

    def connect_user(self, token: str):
        ws_url = f"{self.base_ws_url}{token}"
        self.keep_running = True

        def run_ws():
            try:
                self.ws = websocket.WebSocket()
                self.ws.connect(ws_url)
                print("Conexão WebSocket estabelecida com o servidor!")

                last_ping = time.time()

                while self.keep_running:
                    try:
                        msg = self.ws.recv()
                        if msg:
                            print(f'Mensagem recebida: {msg}')
                            self.on_message(msg)
                    except websocket.WebSocketTimeoutException:
                        pass
                    except Exception as e:
                        print("Erro no loop de conexão websocket", e)
                        break

                    if time.time() - last_ping > 30:
                        try:
                            self.ws.ping()
                            last_ping = time.time()
                        except Exception as e:
                            print("Falha ao enviar ping: ", e)
                            break

                    time.sleep(0.2)
            except Exception as e:
                print("Erro ao conectar websocket", e)
            finally:
                if self.ws:
                    self.ws.close()
                    print("Conexão WebSocket encerrada.")

        self.ws_thread = threading.Thread(target=run_ws, daemon=True)
        self.ws_thread.start()
        print("Thread WebSocket inicializada em background!")

    def disconnect_user(self):
        self.keep_running = False
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
        print("WebSocket encerrado pelo cliente")

    def set_message_callback(self, callback):
        self.on_message = callback

    def handle_message(self, msg):
        if self.on_message:
            self.on_message(msg)