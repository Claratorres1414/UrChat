import json
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget

from client.controllers.home_controller import HomeController
from client.controllers.login_controller import LoginController
from client.controllers.main_chat_controller import MainChatController
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

        self.api_service.set_message_callback(self.on_message_received)

        self.pending_messages_closed_chat = {}

    def mostrar_tela(self, name):
        self.stack.setCurrentIndex(self.telas[name])

    def mostrar_chat(self, contact):
        from client.controllers.conversation_chat_controller import ConversationChatController
        from client.views.conversation_chat_ui import ConversationChatUi

        contact_id = contact["id"]

        if contact_id in self.chat_telas:
            ui, _ = self.chat_telas[contact_id]
        else:
            ui = ConversationChatUi()
            controller = ConversationChatController(ui, self, self.api_service, contact)
            self.stack.addWidget(ui)
            self.chat_telas[contact_id] = (ui, controller)
            self.telas[contact_id] = self.stack.indexOf(ui)

            if contact_id in self.pending_messages_closed_chat:
                for message in self.pending_messages_closed_chat[contact_id]:
                    try:
                        controller.add_message(message)
                    except:
                        pass
                self.pending_messages_closed_chat[contact_id].clear()

        self.stack.setCurrentIndex(self.telas[contact_id])

    def on_message_received(self, msg):
        try:
            data = json.loads(msg) if isinstance(msg, str) else msg
        except Exception as e:
            print("Erro ao decodificar mensagem:", e)
            return

        msg_type = data.get("type")

        if msg_type == "message":
            sender_id = data.get("from")
            to_id = data.get("to")
            content = data.get("msg")

            print(f"Mensagem recebida de {sender_id}: {content}")

            if sender_id in self.chat_telas or to_id in self.chat_telas:
                if sender_id == to_id:
                    _, controller = self.chat_telas[to_id]
                    controller.add_message(data)
                    return
                if sender_id == self.api_service.user_id and to_id in self.chat_telas:
                    _, controller = self.chat_telas[to_id]
                    controller.add_message(data)
                elif sender_id != self.api_service.user_id and sender_id in self.chat_telas:
                    _, controller = self.chat_telas[sender_id]
                    controller.add_message(data)
                else:
                    if sender_id == self.api_service.user_id:
                        if to_id not in self.pending_messages_closed_chat:
                            self.pending_messages_closed_chat[to_id] = []
                        self.pending_messages_closed_chat[to_id].append(data)
                        print(f"Mensagem recebida de você, chat com {to_id} ainda não aberto.")
                        return
                    if sender_id not in self.pending_messages_closed_chat:
                        self.pending_messages_closed_chat[sender_id] = []
                    self.pending_messages_closed_chat[sender_id].append(data)
                    print(f"Mensagem recebida de {sender_id}, chat ainda não aberto.")
            else:
                if sender_id == self.api_service.user_id:
                    if to_id not in self.pending_messages_closed_chat:
                        self.pending_messages_closed_chat[to_id] = []
                    self.pending_messages_closed_chat[to_id].append(data)
                    print(f"Mensagem recebida de você, chat com {to_id} ainda não aberto.")
                    return
                if sender_id not in self.pending_messages_closed_chat:
                    self.pending_messages_closed_chat[sender_id] = []
                self.pending_messages_closed_chat[sender_id].append(data)
                print(f"Mensagem recebida de {sender_id}, chat ainda não aberto.")

    def logout(self):
        self.chat_telas.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())