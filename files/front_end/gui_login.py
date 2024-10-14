import flet as ft
from loading_screen import loading_window

from analista_dados.files.back_end.controle_login import verificar_tabela_login, obter_dados_usuario


def login_window(page: ft.Page):
    pass
    page.title = "Login - Ardia"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 500
    page.window.height = 305
    page.window.resizable = False
    page.window.center()
    page.bgcolor = ft.colors.WHITE
    page.window.always_on_top = True
    page.window.maximizable = False
    page.window.shadow = True
    page.window.icon = "assets/icon.ico"

    campo_usuario = ft.CupertinoTextField(
        placeholder_text="Usuário",
        autocorrect=False,
        autofocus=True,
        bgcolor=ft.colors.GREY_200,
        color="black",
        cursor_color="grey",
        width=400,
    )
    campo_senha = ft.CupertinoTextField(
        placeholder_text="Senha",
        autocorrect=False,
        bgcolor=ft.colors.GREY_200,
        color="black",
        cursor_color="grey",
        width=400,
        password=True,
        can_reveal_password=True,
    )

    def handle_close(e):
        page.close(dlg_modal)
        page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Usuario ou Senha Incorretos"),
        content=ft.Text("Confirme seus dados de acesso", color=ft.colors.WHITE),
        actions=[
            ft.TextButton("ok", on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: page.add(
            ft.Text("Modal dialog dismissed"),
        ),
    )

    def autenticar(campo_usuario, campo_senha, page):  # Função para autenticar o usuário
        print("iniciando autenticar")
        """Autentica o usuário."""
        nome_usuario = campo_usuario.value  # Obtenha o valor do campo de usuário
        senha_digitada = campo_senha.value  # Obtenha o valor do campo de senha
        global usuario_atual  # Defina usuario_atual como global
        usuario_atual = {None}

        # 1. Verificar se a tabela de usuários existe (e cria se não existir)
        verificar_tabela_login()

        # 2. Buscar os dados do usuário no banco de dados
        dados_usuario = obter_dados_usuario(nome_usuario)

        print(f'Usuario: {nome_usuario} Senha: {senha_digitada}')

        if dados_usuario:
            senha_banco, tipo_usuario, unidade = dados_usuario

            # 3. Verificar a senha
            if senha_digitada == senha_banco:
                # 4. Login bem-sucedido!
                usuario_atual = {"nome": nome_usuario, "tipo": tipo_usuario, "unidade": unidade}
                return True
            else:
                print("Erro", "Senha incorreta!")
                return False
        else:
            print("Erro", "Usuário não encontrado!")
        print(f"Login: gui_login: {usuario_atual}")
        return False

    def click_botao_entrar(e):
        """Função chamada quando o botão 'Entrar' é clicado."""
        try:
            result = autenticar(campo_usuario, campo_senha, page)
            if result is True:
                page.clean()
                loading_window(page)
        except Exception as e:
            page.open(dlg_modal)
            print(f"Erro autenticar: {e}")

    botao_entrar = ft.FilledButton(
        text="Entrar",
        width=450,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.GREEN_400,
            color=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=7),
            overlay_color=ft.colors.LIGHT_GREEN_200,
        ),
        on_click=click_botao_entrar,  # Passa a função de callback para on_click
    )
    layout = ft.Column(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="Usuário", size=12, weight=ft.FontWeight.BOLD),
                        campo_usuario,
                        ft.Text(value="Senha", size=12, weight=ft.FontWeight.BOLD),
                        campo_senha
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                bgcolor=ft.colors.YELLOW_700,
                width=450,
                height=200,
                border_radius=7,
            ),
            botao_entrar  # Adicione o botão ao layout
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    try:
        page.add(layout)
        # page.theme = meu_tema()
        page.update()
        print("LoginScreen criada")
    except Exception as e:
        print(f'Erro Login: {e}')

ft.app(target=login_window)

'''def autenticar(campo_usuario,campo_senha, page):  # Função para autenticar o usuário
    print("iniciando autenticar")
    """Autentica o usuário."""
    nome_usuario = campo_usuario.value  # Obtenha o valor do campo de usuário
    senha_digitada = campo_senha.value  # Obtenha o valor do campo de senha

    # 1. Verificar se a tabela de usuários existe (e cria se não existir)
    verificar_tabela_login()

    # 2. Buscar os dados do usuário no banco de dados
    dados_usuario = obter_dados_usuario(nome_usuario)

    print(f'Usuario: {nome_usuario} Senha: {senha_digitada}')

    if dados_usuario:
        senha_banco, tipo_usuario, unidade = dados_usuario

        # 3. Verificar a senha
        if senha_digitada == senha_banco:
            # 4. Login bem-sucedido!
            global usuario_atual  # Defina usuario_atual como global
            usuario_atual = {"nome": nome_usuario, "tipo": tipo_usuario, "unidade": unidade}
            LoginScreen.login_window.disabled = True
        else:
            print("Erro", "Senha incorreta!")
    else:
        print("Erro", "Usuário não encontrado!")
    print(f"gui_login: {usuario_atual}")'''