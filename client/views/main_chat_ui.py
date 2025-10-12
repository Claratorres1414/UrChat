from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QPushButton, QListWidget


class MainChatUI(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel("Chat")
        self.contacts_list = QListWidget()
        self.sair_btn = QPushButton("Sair")

        layout.addWidget(self.label)
        layout.addWidget(self.contacts_list)
        layout.addWidget(self.sair_btn)

        self.setLayout(layout)