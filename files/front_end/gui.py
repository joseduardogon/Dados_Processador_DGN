import flet as ft
from front_end.tema import meu_tema
import front_end.session as session
#from gui_login import dados_usuario
from analista_dados.files.back_end.interpretador import validar_arquivo, excluir_dados_banco

#from analista_dados.files.back_end.cadastro_funcionario import criar_tabela_funcionarios

arquivo_selecionado = None

def abrir_seletor_arquivo(e):
    global arquivo_selecionado
    print("----- Iniciando abrir_seletor_arquivo -----")

    # Verifica se um arquivo foi selecionado
    if file_picker.result and file_picker.result.files:
        arquivo_selecionado = file_picker.result.files[0]
        print(f"Arquivo selecionado: {arquivo_selecionado.name}")

        # Verifica a extensão do arquivo
        if arquivo_selecionado.name.endswith(".txt") or arquivo_selecionado.name.endswith(".TXT"):  # Altere a extensão conforme necessário
            label_resultado.value = f"Arquivo válido: {arquivo_selecionado.name}"
        else:
            label_resultado.value = "Extensão de arquivo inválida!"
        print(label_resultado.value)
        print(arquivo_selecionado.path)
        print(session.usuario_atual['nome'])
        print(session.usuario_atual['unidade'])

# Instância de FilePicker para abrir o diálogo de seleção de arquivos
file_picker = ft.FilePicker(on_result=abrir_seletor_arquivo)

# Label para exibir o resultado da seleção
label_resultado = ft.Text(value="Nenhum arquivo selecionado.")


# Função para processar o arquivo após a seleção
def processar_arquivo(e):
    print("----- Iniciando processar_arquivo -----")
    if arquivo_selecionado:
        # Suponha que `validar_arquivo` seja uma função existente no seu projeto
        if validar_arquivo(arquivo_selecionado.path, session.usuario_atual['nome'], session.usuario_atual['unidade']):
            print("Arquivo válido selecionado:", arquivo_selecionado.name)
            print("----- Fim de abrir_seletor_arquivo -----")
        else:
            label_resultado.value = "Tipo de arquivo inválido. Selecione um arquivo .txt ou .xlsx."
            print("----- Fim de abrir_seletor_arquivo -----")

def main_gui(page: ft.page):
    pass
    page.update()
    page.window.maximized = True
    page.bgcolor = ft.colors.GREY_50
    page.window.resizable = False
    page.window.maximizable = True
    page.window.frameless = False
    page.window.always_on_top = False
    page.update()

    page.overlay.append(file_picker)

    icon = ft.Text("teste de ícone", color="black")

    botao_importar = ft.FilledButton(
        text="Importar Arquivo",
        width=450,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.WHITE,
            color=ft.colors.BLACK,
            shape=ft.RoundedRectangleBorder(radius=7),
            overlay_color=ft.colors.GREY_200,
        ),
        on_click=lambda _: file_picker.pick_files(),  # Passa a função de callback para on_click
    )

    botao_processar = ft.FilledButton(
        text="Processar Arquivo",
        width=450,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.WHITE,
            color=ft.colors.BLACK,
            shape=ft.RoundedRectangleBorder(radius=7),
            overlay_color=ft.colors.GREY_200,
        ),
        on_click= processar_arquivo,  # Passa a função de callback para on_click
    )

    import_layout = ft.Row([
        ft.Column([
            ft.Container(
                content=ft.Column([
                        ft.Text(value=arquivo_selecionado, size=12, weight=ft.FontWeight.BOLD),
                    botao_importar,
                    botao_processar,
                ],
                alignment=ft.MainAxisAlignment.START,
                ),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.YELLOW_700,
            border_radius=7,
            height = 600
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        width = 500,
        height = 900,
        )
    ]
    )

    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        divider_color=ft.colors.YELLOW_700,
        indicator_color=ft.colors.YELLOW_200,
        indicator_tab_size=True,
        indicator_thickness=7,
        tabs=[
            ft.Tab(
                tab_content=ft.Text("Adicionar Dados", color="black"),
                content=import_layout,
            ),
            ft.Tab(
                tab_content=ft.Text("Dashboards de Dados", color="black"),
                content=ft.Text("This is Tab 2"),
            ),
            ft.Tab(
                tab_content=ft.Text("Cadastro de Funcionários", color="black"),
                content=ft.Text("This is Tab 3"),
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.icons.SETTINGS, color="black"),
                content=ft.Text("This is Tab 4"),
            ),
        ],
        expand=1,
    )

    layout = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Row(
                    [icon],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,
                width=450,
                height=80,
                border_radius=7,
            ),
            ft.Container(
                content=ft.Row(
                    [t],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,
                width=1920,
                height=990,
                border_radius=7,
            ),
        ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center
    )

    def handle_close(e):
        page.close(dlg_modal)
        page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Erro ao preocessar Dados"),
        content=ft.Text(' ArdIA: "Entre em contato conosco para suporte"', color=ft.colors.WHITE),
        actions=[
            ft.TextButton("ok", on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: page.add(
            ft.Text("Modal dialog dismissed"),
        )
    ),

    try:
        page.add(layout)
        page.theme = meu_tema()
        page.update()
        print('Página "layout" criada com sucesso')
    except Exception as e:
        page.open(dlg_modal)
        print(f'Erro: {e}')

    print(session.usuario_atual)


def criar_aba_importar(self):
    """Cria a aba 'Importar Arquivo'."""
    print("----- Iniciando criar_aba_importar -----")
    """try:
        widget_importar = QWidget()
        layout_importar = QVBoxLayout()
        layout_botoes_arquivo = QVBoxLayout()

        self.botao_selecionar = QPushButton("Selecionar Arquivo", self)
        self.botao_selecionar.clicked.connect(self.abrir_seletor_arquivo)
        if self.usuario_atual['tipo'] == "admin":
            self.botao_selecionar.setEnabled(False)
        else:
            self.botao_selecionar.setEnabled(True)  # Botao desabilitado ate que o login seja feito
        layout_botoes_arquivo.addWidget(self.botao_selecionar)

        # Crie o label para exibir o nome do arquivo
        self.label_arquivo = QLabel("", self)
        layout_botoes_arquivo.addWidget(self.label_arquivo)

        self.botao_processar = QPushButton("Processar Arquivo", self)
        self.botao_processar.clicked.connect(self.processar_arquivo)
        if self.usuario_atual['tipo'] == "admin":
            self.botao_processar.setEnabled(False)
        else:
            self.botao_processar.setEnabled(True)  # Botao desabilitado ate que o login seja feito
        layout_botoes_arquivo.addWidget(self.botao_processar)

        layout_importar.addLayout(layout_botoes_arquivo)
        widget_importar.setLayout(layout_importar)
        self.abas.addTab(widget_importar, "Importar")

        self.botao_selecionar.setObjectName("botao_selecionar")
        self.botao_processar.setObjectName("botao_selecionar")
        print("----- Fim de criar_aba_importar -----")
    except Exception as e:
        print(f"Erro em criar_aba_importar: {e}")"""


def criar_aba_desempenho(self):
    """Cria a aba 'Desempenho'."""
    print("----- Iniciando criar_aba_desempenho -----")
    """try:
        # Crie a aba "Desempenho" com a classe DesempenhoWidget
        self.desempenho_widget = DesempenhoWidget(self.usuario_atual, self)
        self.abas.addTab(self.desempenho_widget, "Desempenho")

        print("----- Fim de criar_aba_desempenho -----")
    except Exception as e:
        print(f"Erro em criar_aba_desempenho: {e}")"""


def criar_aba_controle_funcionarios(self):
    """Cria a aba 'Configurações'."""
    print("----- Iniciando criar_aba_configuracoes -----")
    """try:
        widget_controle = QWidget()
        layout_controle = QVBoxLayout()

        botao_funcionarios = QPushButton("Funcionarios", self)
        botao_funcionarios.setObjectName("botao_selecionar")
        botao_funcionarios.clicked.connect(criar_tabela_funcionarios)
        layout_controle.addWidget(botao_funcionarios)

        widget_controle.setLayout(layout_controle)
        self.abas.addTab(widget_controle, "Controle de Funcionários")
        print("----- Fim de criar_aba_controle -----")
    except Exception as e:
        print(f"Erro em criar_aba_controle: {e}")"""


def criar_aba_configuracoes(self):
    """Cria a aba 'Configurações'."""
    print("----- Iniciando criar_aba_configuracoes -----")
    """try:
        widget_configuracoes = QWidget()
        layout_configuracoes = QVBoxLayout()

        botao_excluir_dados = QPushButton("Excluir Dados do Banco", self)
        botao_excluir_dados.setObjectName("botao_cancelar")
        botao_excluir_dados.clicked.connect(self.excluir_dados)
        layout_configuracoes.addWidget(botao_excluir_dados)

        widget_configuracoes.setLayout(layout_configuracoes)
        self.abas.addTab(widget_configuracoes, "Configurações")
        print("----- Fim de criar_aba_configuracoes -----")
    except Exception as e:
        print(f"Erro em criar_aba_configuracoes: {e}")"""




def excluir_dados(self):
    """Exclui os dados do banco de dados (apenas para protótipo!)."""
    print("----- Iniciando excluir_dados -----")
    """try:
        resposta = QMessageBox.question(self, "Confirmação",
                                         "Tem certeza que deseja excluir TODOS os dados do banco de dados?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            excluir_dados_banco()
            QMessageBox.information(self, "Sucesso", "Dados excluídos do banco de dados!")
        print("----- Fim de excluir_dados -----")
    except Exception as e:
        print(f"Erro em excluir_dados: {e}")"""


def label_doc(self):  # Método da classe para atualizar o label
    """Atualiza o label com o nome do arquivo."""
    try:
        self.label_arquivo.setText(self.arquivo)  # Atualize o texto do label
        print("self.arquivo sucesso")
    except Exception as e:
        print(f"Erro em label_doc: {e}")


#ft.app(main_gui)