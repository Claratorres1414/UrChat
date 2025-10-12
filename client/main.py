import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget

from client.controllers.conversation_chat_controller import ConversationChatController
from client.controllers.home_controller import HomeController
from client.controllers.login_controller import LoginController
from client.controllers.main_chat_controller import MainChatController
from client.views.conversation_chat_ui import ConversationChatUi
from client.views.home_ui import HomeUi
from client.views.login_ui import LoginUI
from client.views.main_chat_ui import MainChatUI
from views.cadastro_ui import CadastroUi
from controllers.cadastro_controller import CadastroController
from services.api_service import ApiService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UrChat")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.api_service = ApiService(base_url="http://127.0.0.1:8000", base_ws_url="ws://127.0.0.1:8000/connect/ws?token=")

        self.home_ui = HomeUi()
        self.cadastro_ui = CadastroUi()
        self.login_ui = LoginUI()
        self.main_chat_ui = MainChatUI()

        self.stack.addWidget(self.home_ui)
        self.stack.addWidget(self.cadastro_ui)
        self.stack.addWidget(self.login_ui)
        self.stack.addWidget(self.main_chat_ui)

        self.telas = {
            "home": self.stack.indexOf(self.home_ui),
            "cadastro": self.stack.indexOf(self.cadastro_ui),
            "login": self.stack.indexOf(self.login_ui),
            "main_chat": self.stack.indexOf(self.main_chat_ui)
        }

        self.chat_telas = {}

        self.home_controller = HomeController(self.home_ui, self)
        self.cadastro_controller = CadastroController(self.cadastro_ui, self, self.api_service)
        self.login_controller = LoginController(self.login_ui, self, self.api_service)
        self.main_chat_controller = MainChatController(self.main_chat_ui, self, self.api_service)

        self.mostrar_tela("home")

    def mostrar_tela(self, name):
        self.stack.setCurrentIndex(self.telas[name])

    def mostrar_chat(self, username):
        from client.controllers.conversation_chat_controller import ConversationChatController
        from client.views.conversation_chat_ui import ConversationChatUi

        if username in self.chat_telas:
            ui, _ = self.chat_telas[username]
        else:
            ui = ConversationChatUi()
            controller = ConversationChatController(ui, self, self.api_service, username)
            self.stack.addWidget(ui)
            self.chat_telas[username] = (ui, controller)
            self.telas[username] = self.stack.indexOf(ui)

        self.stack.setCurrentIndex(self.telas[username])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())