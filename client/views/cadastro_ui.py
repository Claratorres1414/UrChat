from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class CadastroUi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("- Cadastro -")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.username_label = QLabel("Nome de usuário: ")
        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)

        self.password_label = QLabel("Senha: ")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        self.cadastrar_btn = QPushButton("Cadastrar")
        self.layout.addWidget(self.cadastrar_btn)