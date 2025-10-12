from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel


class ConversationChatUi(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel()
        self.voltar_btn = QPushButton("Voltar")
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.message_input = QLineEdit()
        self.send_button = QPushButton("Enviar")

        layout.addWidget(self.label)
        layout.addWidget(self.voltar_btn)
        layout.addWidget(self.chat_display)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def set_contact_name(self, username: str):
        self.label.setText(username)