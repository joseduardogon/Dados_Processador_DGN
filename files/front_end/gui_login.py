import flet as ft

from analista_dados.files.back_end.controle_login import verificar_tabela_login, obter_dados_usuario

def main(page: ft.Page):
    page.title = "Login - Ardia"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 500
    page.window.height = 300
    page.window.resizable = False
    page.window.center()
    page.bgcolor = ft.colors.AMBER_300
    page.window.always_on_top = True
    page.window.maximizable = False
    page.window.shadow = True

    page.add(
        ft.Row(
            [
                ft.Column([
                    ft.Container(
                        content=ft.Text("Non clickable"),
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.WHITE,
                        width=450,
                        height=200,
                        border_radius=7,
                    ),
                    ft.FilledButton(
                        text="Entrar",
                        width = 450,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.TEAL_ACCENT_700,
                            shape=ft.RoundedRectangleBorder(radius=7),
                        ),
                    )
                ]
                ),
            ],
            spacing = 10,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    def autenticar(self):
        """Autentica o usuário."""
        nome_usuario = self.campo_usuario.text()
        senha_digitada = self.campo_senha.text()

        # 1. Verificar se a tabela de usuários existe (e cria se não existir)
        verificar_tabela_login()

        # 2. Buscar os dados do usuário no banco de dados
        dados_usuario = obter_dados_usuario(nome_usuario)

        if dados_usuario:
            senha_banco, tipo_usuario, unidade = dados_usuario

            # 3. Verificar a senha
            if senha_digitada == senha_banco:  # Substitua senha_correta pela sua lógica de verificação
                # 4. Login bem-sucedido!
                global usuario_atual  # Defina usuario_atual como global
                usuario_atual = {"nome": nome_usuario, "tipo": tipo_usuario, "unidade": unidade}
                self.login_sucedido.emit(usuario_atual)  # Emite o sinal de login bem-sucedido
            else:
                print( "Erro", "Senha incorreta!")
        else:
            print("Erro", "Usuário não encontrado!")
        print(f"gui_login: {usuario_atual}")

ft.app(main)