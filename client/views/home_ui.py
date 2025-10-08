from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class HomeUi(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel("Bem-vindo ao UrChat!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.cadastro_label = QLabel("É novo por aqui? Faça o seu cadastro clicando nesse botão:")
        self.cadastro_btn = QPushButton("Cadastrar")
        self.login_btn = QPushButton("Entrar")

        layout.addWidget(self.label)
        layout.addWidget(self.cadastro_label)
        layout.addWidget(self.cadastro_btn)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)