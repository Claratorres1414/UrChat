from PyQt6.QtWidgets import QMessageBox
from requests import RequestException

from client.services.api_service import ApiService


class LoginController:
    def __init__(self, ui, main_window, api_service: ApiService):
        self.ui = ui
        self.main_window = main_window
        self.api_service = api_service

        self.ui.entrar_btn.clicked.connect(self.entrar_usuario)
        self.ui.voltar_btn.clicked.connect(self.tp_home)

    def entrar_usuario(self):
        username = self.ui.username_input.text().strip()
        password = self.ui.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self.ui, "Erro", "Preencha todos campos!")
            return

        result = self.api_service.login_user(username, password)
        if result["success"]:
            try:
                self.api_service.connect_user(result["data"]["access_token"])
            except RequestException as e:
                QMessageBox.warning(self.ui, "Falha no servidor", f"Não foi possível conectar {username} ao servidor!")
                print("Erro de conexão: ", e)
                return
            QMessageBox.information(self.ui, "Sucesso", f"Bem vindo {username}!")
            self.ui.username_input.clear()
            self.ui.password_input.clear()
            self.main_window.mostrar_tela("main_chat")
        else:
            QMessageBox.warning(self.ui, "Erro", "Falha ao logar, usuário ou senha inválidos!")

    def tp_home(self):
        self.main_window.mostrar_tela("home")