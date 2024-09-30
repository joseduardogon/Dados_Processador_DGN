import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from front_end.gui_login import LoginWindow  # Importe a janela de login
from front_end.loading_screen import LoadingScreen  # Importe a loading screen


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Inicia com a janela de login
        self.login_window = LoginWindow()
        self.login_window.show()

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
        self.janela_principal = QMainWindow()
        self.janela_principal.showMaximized()
        self.loading_screen.close()


if __name__ == '__main__':
    aplicacao = App()