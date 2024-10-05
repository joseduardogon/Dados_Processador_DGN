import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from front_end.gui_login import LoginWindow  # Importe a janela de login
from front_end.loading_screen import LoadingScreen  # Importe a loading screen
from front_end.gui import MainWindow
from front_end.styles import STYLESHEET

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(STYLESHEET)

        # Inicia com a janela de login
        self.login_window = LoginWindow()
        self.login_window.show()
        self.login_window.login_sucedido.connect(self.receber_dados_usuario)

        # Conecta o sinal de login bem-sucedido à função de iniciar a loading screen
        self.login_window.login_sucedido.connect(self.iniciar_loading_screen)

        sys.exit(self.app.exec_())

    def iniciar_loading_screen(self):
        """Inicia a loading screen após o login bem-sucedido."""
        self.loading_screen = LoadingScreen()
        self.loading_screen.show()
        self.login_window.close()  # Fecha a janela de login

        # Conecta o sinal da loading screen à função de iniciar a janela principal
        self.loading_screen.loading_completo.connect(self.iniciar_janela_principal)

    def iniciar_janela_principal(self):
        """Inicia a janela principal da aplicação."""
        print(f"main: {self.dados_usuario}")
        self.janela_principal = MainWindow(self.dados_usuario)
        self.janela_principal.showMaximized()
        self.loading_screen.close()

    def receber_dados_usuario(self, dados_usuario):
        """Recebe e armazena os dados do usuário."""
        self.dados_usuario = dados_usuario  # Armazena em um atributo da classe App
        print("Dados do usuário recebidos em main.py:", self.dados_usuario)


if __name__ == '__main__':
    aplicacao = App()