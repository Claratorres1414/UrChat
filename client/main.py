import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from client.controllers.home_controller import HomeController
from client.controllers.login_controller import LoginController
from client.views.home_ui import HomeUi
from client.views.login_ui import LoginUI
from views.cadastro_ui import CadastroUi
from controllers.cadastro_controller import CadastroController
from services.api_service import ApiService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UrChat")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.api_service = ApiService(base_url="http://127.0.0.1:8000")

        self.home_ui = HomeUi()
        self.cadastro_ui = CadastroUi()
        self.login_ui = LoginUI()

        self.stack.addWidget(self.home_ui)
        self.stack.addWidget(self.cadastro_ui)
        self.stack.addWidget(self.login_ui)

        self.telas = {
            "home": self.stack.indexOf(self.home_ui),
            "cadastro": self.stack.indexOf(self.cadastro_ui),
            "login": self.stack.indexOf(self.login_ui)
        }

        self.home_controller = HomeController(self.home_ui, self)
        self.cadastro_controller = CadastroController(self.cadastro_ui, self, self.api_service)
        self.login_controller = LoginController(self.login_ui, self, self.api_service)

        self.mostrar_tela("home")

    def mostrar_tela(self, name):
        self.stack.setCurrentIndex(self.telas[name])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())