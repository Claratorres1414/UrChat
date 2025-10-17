from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QListWidgetItem
from requests import RequestException

from client.services.api_service import ApiService


class MainChatController:
    def __init__(self, ui, main_window, api_service: ApiService):
        self.ui = ui
        self.main_window = main_window
        self.api_service = api_service

        self.chat_windows = {}

        self.ui.sair_btn.clicked.connect(self.tp_home)

        self.load_contacts()

        self.timer = QTimer()
        self.timer.timeout.connect(self.load_contacts)
        self.timer.start(1000) #Se aumentar o fluxo de clientes, aumentar tempo

        self.ui.contacts_list.itemDoubleClicked.connect(self.open_chat)

    def load_contacts(self):
        try:
            contacts = self.api_service.list_contacts()
            print("contatos recebidos", contacts)

            self.ui.contacts_list.clear()

            if not contacts:
                self.ui.contacts_list.addItem(QListWidgetItem("Nenhum contato encontrado."))
                return

            for contact in contacts:
                if contact["status"] == "online":
                    item_text = f"{contact["username"]} ({contact["status"]})"
                else:
                    item_text = f"{contact["username"]} ({contact["status"]} - {contact["last_seen"]})"

                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, contact)
                self.ui.contacts_list.addItem(item)

        except RequestException as e:
            print(f"Erro ao carregar contatos: {e}")

    def open_chat(self, item):
        contact = item.data(Qt.ItemDataRole.UserRole)
        contact_username = contact["username"]
        self.main_window.mostrar_chat(contact)
        print(f"Abrindo chat com {contact_username} | {contact["id"]}")

    def tp_home(self):
        self.main_window.mostrar_tela("home")
        self.api_service.disconnect_user()