from client.services.api_service import ApiService


class ConversationChatController:
    def __init__(self, ui, main_window, api_service: ApiService, contact_username: str):
        self.ui = ui
        self.main_window = main_window
        self.api_service = api_service
        self.contact_info = contact_username

        self.ui.set_contact_name(contact_username)

        self.ui.voltar_btn.clicked.connect(self.tp_main_chat)

    def tp_main_chat(self):
        self.main_window.mostrar_tela("main_chat")
        self.main_window.main_chat_controller.load_contacts()