import flet as ft
from front_end.tema import meu_tema
from front_end.gui_login import LoginScreen

class App:
    def App(page: ft.Page):
        # Inicia com a janela de login
        ft.app(target=LoginScreen.login_window)
        LoginScreen.login_window.theme = meu_tema()
        #self.login_window.login_sucedido.connect(self.receber_dados_usuario)

        # Conecta o sinal de login bem-sucedido à função de iniciar a loading screen
        #self.login_window.login_sucedido.connect(self.iniciar_loading_screen)

        #self.login_window.destroy()

    """
    def receber_dados_usuario(self, dados_usuario):
        #Recebe e armazena os dados do usuário.
        self.dados_usuario = dados_usuario  # Armazena em um atributo da classe App
        print("Dados do usuário recebidos em main.py:", self.dados_usuario)"""


if __name__ == '__main__':
    aplicacao = App()