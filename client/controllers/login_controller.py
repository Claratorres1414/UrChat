from PyQt6.QtWidgets import QMessageBox

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
            QMessageBox.information(self.ui, "Sucesso", f"Bem vindo {username}!")
            self.ui.username_input.clear()
            self.ui.password_input.clear()
        else:
            QMessageBox.warning(self.ui, "Erro", result["error"])

    def tp_home(self):
        self.main_window.mostrar_tela("home")