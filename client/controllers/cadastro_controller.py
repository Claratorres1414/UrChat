from PyQt6.QtWidgets import QMessageBox
from client.services.api_service import ApiService

class CadastroController:
    def __init__(self, ui, api_service: ApiService):
        self.ui = ui
        self.api_service = api_service
        self.ui.cadastrar_btn.clicked.connect(self.cadastrar_usuario)
    def cadastrar_usuario(self):
        username = self.ui.username_input.text().strip()
        password = self.ui.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self.ui, "Erro", "Preencha todos os campos!")
            return

        if len(password) < 8:
            QMessageBox.warning(self.ui, "Erro", "Senha deve ter no mínimo 8 caracteres!")
            return

        result = self.api_service.register_user(username, password)
        if result["success"]:
            QMessageBox.information(self.ui, "Sucesso", "Usuario cadastrado com sucesso!")
            self.ui.username_input.clear()
            self.ui.password_input.clear()
        else:
            QMessageBox.critical(self.ui, "Erro", result["error"])