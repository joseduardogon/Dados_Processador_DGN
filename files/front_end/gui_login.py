import flet as ft
from tema import meu_tema

from analista_dados.files.back_end.controle_login import verificar_tabela_login, obter_dados_usuario


class LoginWindow(ft.UserControl):  # Herda de ft.UserControl
    def __init__(self):
        super().__init__()
        self.login_sucedido = ft.event()

        self.campo_usuario = ft.CupertinoTextField(
            placeholder_text="Usuário",
            autocorrect=False,
            autofocus=True,
            bgcolor=ft.colors.GREY_200,
            color="black",
            cursor_color="grey",
            width=400,
        )
        self.campo_senha = ft.CupertinoTextField(
            placeholder_text="Senha",
            autocorrect=False,
            bgcolor=ft.colors.GREY_200,
            color="black",
            cursor_color="grey",
            width=400,
            password=True,
            can_reveal_password=True,
        )
        self.botao_entrar = ft.FilledButton(
            text="Entrar",
            width=450,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.GREY_200,
                color=ft.colors.GREEN_800,
                shape=ft.RoundedRectangleBorder(radius=7),
                overlay_color=ft.colors.LIGHT_GREEN_200,
            ),
            on_click=self.autenticar,  # Conecte o botão à função autenticar
        )

    def build(self):  # Método build para criar o layout
        return ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(value="Usuário", size=12, weight=ft.FontWeight.BOLD),
                            self.campo_usuario,
                            ft.Text(value="Senha", size=12, weight=ft.FontWeight.BOLD),
                            self.campo_senha
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.YELLOW_700,
                    width=450,
                    height=200,
                    border_radius=7,
                ),
                self.botao_entrar  # Adicione o botão ao layout
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def autenticar(self, e):  # Função para autenticar o usuário
        """Autentica o usuário."""
        nome_usuario = self.campo_usuario.value  # Obtenha o valor do campo de usuário
        senha_digitada = self.campo_senha.value  # Obtenha o valor do campo de senha

        # 1. Verificar se a tabela de usuários existe (e cria se não existir)
        verificar_tabela_login()

        # 2. Buscar os dados do usuário no banco de dados
        dados_usuario = obter_dados_usuario(nome_usuario)

        if dados_usuario:
            senha_banco, tipo_usuario, unidade = dados_usuario

            # 3. Verificar a senha
            if senha_digitada == senha_banco:
                # 4. Login bem-sucedido!
                global usuario_atual  # Defina usuario_atual como global
                usuario_atual = {"nome": nome_usuario, "tipo": tipo_usuario, "unidade": unidade}
                self.login_sucedido.data = usuario_atual  # Atribuir dados ao evento
                self.login_sucedido.set()  # Disparar o evento
            else:
                print("Erro", "Senha incorreta!")
        else:
            print("Erro", "Usuário não encontrado!")
        print(f"gui_login: {usuario_atual}")


def main(page: ft.Page):
    page.title = "Login - Ardia"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 500
    page.window.height = 300
    page.window.resizable = False
    page.window.center()
    page.bgcolor = ft.colors.GREY_50
    page.window.always_on_top = True
    page.window.maximizable = False
    page.window.shadow = True
    page.window.icon = "assets/icon.ico"
    login_control = LoginWindow()

    # Adicione o UserControl à página
    page.add(login_control)

    page.theme = meu_tema()
    page.update()


ft.app(target=main)