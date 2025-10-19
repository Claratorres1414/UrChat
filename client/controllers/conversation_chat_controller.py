import json

from PyQt6.QtCore import QObject, pyqtSignal

from client.services.api_service import ApiService

class ChatSignals(QObject):
    messageReceived = pyqtSignal(str)

class ConversationChatController:
    def __init__(self, ui, main_window, api_service: ApiService, contact):
        self.ui = ui
        self.main_window = main_window
        self.api_service = api_service
        self.contact = contact

        self.messages = []

        self.ui.set_contact_name(contact["username"])

        self.ui.send_button.clicked.connect(self.send_message)
        self.ui.voltar_btn.clicked.connect(self.tp_main_chat)

    def add_message(self, msg):
        self.messages.append(msg)
        sender_id = msg.get("from")
        content = msg.get("msg")
        if sender_id == self.api_service.user_id:
            self.ui.chat_display.append(f"Você: {content}")
            return
        sender = self.api_service.contacts_map.get(sender_id)
        self.ui.chat_display.append(f"{sender}: {content}")

    def send_message(self):
        content = self.ui.message_input.text().strip()
        if not content:
            return
        msg = {
            "to": self.contact["id"],
            "msg": content
        }
        try:
            if self.api_service.ws:
                self.api_service.ws.send(json.dumps(msg))
                self.ui.message_input.clear()
        except Exception as e:
            print("Erro ao enviar mensagem: ", e)

    def tp_main_chat(self):
        self.main_window.mostrar_tela("main_chat")
        self.main_window.main_chat_controller.load_contacts()