import sys
from PyQt6.QtWidgets import QApplication
from views.cadastro_ui import CadastroUi
from controllers.cadastro_controller import CadastroController
from services.api_service import ApiService

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = CadastroUi()

    api_service = ApiService("http://127.0.0.1:8000")

    controller = CadastroController(ui, api_service)

    ui.show()
    sys.exit(app.exec())