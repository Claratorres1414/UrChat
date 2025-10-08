class HomeController:
    def __init__(self, ui, main_window):
        self.ui = ui
        self.main_window = main_window

        self.ui.cadastro_btn.clicked.connect(self.tp_cadastro)

    def tp_cadastro(self):
        self.main_window.mostrar_tela("cadastro")