import json

from PyQt6.QtCore import QObject, pyqtSignal

from client.database.chat_database import ChatDatabase
from client.services.api_service import ApiService

class ChatSignals(QObject):
    messageReceived = pyqtSignal(str)

class ConversationChatController:
    def __init__(self, ui, main_window, api_service: ApiService, contact):
        self.ui = ui
        self.main_window = main_window
        self.api_service = api_service
        self.contact = contact
        self.db = ChatDatabase(api_service.user_id)
        self.contact_db = ChatDatabase(contact["id"])

        self.ui.set_contact_name(contact["username"])

        self.main_window.signals.message_received.connect(self.handle_message)

        self.ui.send_button.clicked.connect(self.send_message)
        self.ui.voltar_btn.clicked.connect(self.tp_main_chat)

    def handle_message(self, data):
        msg_type = data.get("type")

        if msg_type not in ["message", "pending_messages", "unhandled_message"]:
            return

        sender_id = data.get("from")
        receiver_id = data.get("to")
        content = data.get("msg")

        if sender_id != self.contact["id"] and receiver_id != self.contact["id"]:
            return

        msg_id = self.db.save_message(sender_id, receiver_id, content, delivered=0)
        if sender_id != receiver_id:
            msg_delivered = self.contact_db.save_message(sender_id, receiver_id, content, delivered=0)

        if receiver_id == self.api_service.user_id or self.contact["status"] == "online":
            self.db.mark_as_delivered(int(msg_id))

        sender_name = "Você" if sender_id == self.api_service.user_id else self.contact["username"]
        self.ui.chat_display.append(f"{sender_name}: {content}")

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

    def load_conversation_chat(self, contact_id):
        self.ui.chat_display.clear()
        history = self.db.get_conversation(self.api_service.user_id, contact_id)

        for sender_id, receiver_id, content, delivered in history:
            if sender_id == self.api_service.user_id:
                self.ui.chat_display.append("Você: " + content)
            else:
                self.ui.chat_display.append(f"{self.contact["username"]}: {content}")

    def tp_main_chat(self):
        self.main_window.mostrar_tela("main_chat")
        self.main_window.main_chat_controller.load_contacts()