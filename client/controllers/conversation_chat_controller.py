from PyQt6.QtCore import QObject, pyqtSignal

from client.services.api_service import ApiService

class ChatSignals(QObject):
    messageReceived = pyqtSignal(str)

class ConversationChatController:
    def __init__(self, ui, main_window, api_service: ApiService, contact_username: str):
        self.ui = ui
        self.main_window = main_window
        self.api_service = api_service
        self.contact_info = contact_username

        self.ui.set_contact_name(contact_username)

        self.ui.send_button.clicked.connect(self.send_message)
        self.ui.voltar_btn.clicked.connect(self.tp_main_chat)

        self.api_service.set_message_callback(self.on_message_received)

    def send_message(self):
        msg = self.ui.message_input.text().strip()
        if not msg:
            return

        self.ui.message_input.clear()

        try:
            if self.api_service.ws:
                self.api_service.ws.send(msg)
        except Exception as e:
            print("Erro ao enviar mensagem: ", e)

    def on_message_received(self, msg):
        self.ui.chat_display.append(msg)

    def tp_main_chat(self):
        self.main_window.mostrar_tela("main_chat")
        self.main_window.main_chat_controller.load_contacts()