class MainChatController:
    def __init__(self, ui, main_window):
        self.ui = ui
        self.main_window = main_window

        self.ui.sair_btn.clicked.connect(self.tp_home)

    def tp_home(self):
        self.main_window.mostrar_tela("home")