from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class LoginUI(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.username_label = QLabel("Nome de usuário: ")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Senha: ")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.entrar_btn = QPushButton("Entrar")
        self.voltar_btn = QPushButton("Voltar")

        layout.addWidget(QLabel("Login"))
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.entrar_btn)
        layout.addWidget(self.voltar_btn)

        self.setLayout(layout)