from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QPushButton, QFileDialog,
                             QMessageBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QMenuBar,
                             QMenu, QAction, QTabWidget, QTableWidget, QComboBox, QTableWidgetItem)  # Importe QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from analista_dados.files.back_end.interpretador import validar_arquivo, excluir_dados_banco
from .styles import STYLESHEET
from .gui_desempenho import DesempenhoWidget
from analista_dados.files.back_end.cadastro_funcionario import criar_tabela_funcionarios



class MainWindow(QMainWindow):
    def __init__(self, usuario):
        super().__init__()

        # Armazene os dados do usuário
        self.usuario_atual = usuario
        print(f"gui:{self.usuario_atual}")

        print("----- Iniciando __init__ da MainWindow -----")

        print("Definindo título da janela...")
        self.setWindowTitle("ArdIA")
        print("Título da janela definido.")

        # 1. Criar o QTabWidget
        print("Criando QTabWidget...")
        try:
            self.abas = QTabWidget(self)
            print("QTabWidget criado.")
        except Exception as e:
            print(f"Erro ao criar QTabWidget: {e}")
            return

        print("Definindo QTabWidget como widget central...")
        try:
            self.setCentralWidget(self.abas)
            print("QTabWidget definido como widget central.")
        except Exception as e:
            print(f"Erro ao definir widget central: {e}")
            return

        # 2. Criar os widgets para as abas
        print("Criando abas...")
        try:
            self.criar_aba_importar()
            self.criar_aba_desempenho()  # Nova aba
            self.criar_aba_controle_funcionarios()
            self.criar_aba_configuracoes()
            print("Abas criadas.")
        except Exception as e:
            print(f"Erro ao criar abas: {e}")
            return

        # 3. Layouts
        print("Criando layouts...")
        try:
            layout_principal = QVBoxLayout()
            layout_logo = QHBoxLayout()
            print("Layouts criados.")
        except Exception as e:
            print(f"Erro ao criar layouts: {e}")
            return

        # --- Logo ---
        print("Adicionando logo...")
        try:
            label_logo = QLabel(self)
            pixmap_logo = QPixmap("front_end/logo.png")
            label_logo.setPixmap(pixmap_logo)
            label_logo.setFixedSize(pixmap_logo.width(), pixmap_logo.height())
            layout_logo.addWidget(label_logo)
            print("Logo adicionado ao layout.")
        except Exception as e:
            print(f"Erro ao adicionar logo: {e}")

        print("Adicionando layouts ao layout principal...")
        try:
            layout_principal.addLayout(layout_logo)
            layout_principal.addWidget(self.abas)
            print("Layouts adicionados ao layout principal.")
        except Exception as e:
            print(f"Erro ao adicionar layouts ao layout principal: {e}")

        # Widget central
        print("Criando widget central...")
        try:
            widget_central = QWidget()
            widget_central.setLayout(layout_principal)
            self.setCentralWidget(widget_central)
            print("Widget central criado e definido.")
        except Exception as e:
            print(f"Erro ao criar ou definir widget central: {e}")

        # 4. Aplicar a StyleSheet DEPOIS de definir o layout e os widgets
        print("Aplicando StyleSheet...")
        try:
            self.setStyleSheet(STYLESHEET)
            print("StyleSheet aplicada.")
        except Exception as e:
            print(f"Erro ao aplicar StyleSheet: {e}")

        # 5. Mover a aba "Configurações" para o canto direito
        print("Movendo aba 'Configurações'...")
        """try:
            self.abas.tabBar().moveTab(1, 3)
            print("Aba 'Configurações' movida.")
        except Exception as e:
            print(f"Erro ao mover aba 'Configurações': {e}")"""

        print("----- Fim do __init__ da MainWindow -----")

    def criar_aba_importar(self):
        """Cria a aba 'Importar Arquivo'."""
        print("----- Iniciando criar_aba_importar -----")
        try:
            widget_importar = QWidget()
            layout_importar = QVBoxLayout()
            layout_botoes_arquivo = QHBoxLayout()

            self.botao_selecionar = QPushButton("Selecionar Arquivo", self)
            self.botao_selecionar.clicked.connect(self.abrir_seletor_arquivo)
            if self.usuario_atual['tipo'] == "admin":
                self.botao_selecionar.setEnabled(False)
            else:
                self.botao_selecionar.setEnabled(True)  # Botao desabilitado ate que o login seja feito
            layout_botoes_arquivo.addWidget(self.botao_selecionar)

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
            print(f"Erro em criar_aba_importar: {e}")

    def criar_aba_desempenho(self):
        """Cria a aba 'Desempenho'."""
        print("----- Iniciando criar_aba_desempenho -----")
        try:
            # Crie a aba "Desempenho" com a classe DesempenhoWidget
            self.desempenho_widget = DesempenhoWidget(self.usuario_atual, self)
            self.abas.addTab(self.desempenho_widget, "Desempenho")

            print("----- Fim de criar_aba_desempenho -----")
        except Exception as e:
            print(f"Erro em criar_aba_desempenho: {e}")

    def criar_aba_controle_funcionarios(self):
        """Cria a aba 'Configurações'."""
        print("----- Iniciando criar_aba_configuracoes -----")
        try:
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
            print(f"Erro em criar_aba_controle: {e}")

    def criar_aba_configuracoes(self):
        """Cria a aba 'Configurações'."""
        print("----- Iniciando criar_aba_configuracoes -----")
        try:
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
            print(f"Erro em criar_aba_configuracoes: {e}")

    def abrir_seletor_arquivo(self, arquivo):
        """Abre a janela de diálogo para seleção de arquivo e valida a extensão."""
        print("----- Iniciando abrir_seletor_arquivo -----")
        try:
            self.arquivo, _ = QFileDialog.getOpenFileName(self, "Selecione um Arquivo")
        except Exception as e:
            print(f"Erro em abrir_seletor_arquivo: {e}")

    def processar_arquivo(self):
        if self.arquivo:
            if validar_arquivo(self.arquivo, self.usuario_atual['nome'], self.usuario_atual['unidade']):
                print("Arquivo válido selecionado:", self.arquivo)
                print("----- Fim de abrir_seletor_arquivo -----")
            else:
                QMessageBox.warning(self, "Erro",
                                    "Tipo de arquivo inválido. Selecione um arquivo .txt ou .xlsx.")
                print("----- Fim de abrir_seletor_arquivo -----")

    def excluir_dados(self):
        """Exclui os dados do banco de dados (apenas para protótipo!)."""
        print("----- Iniciando excluir_dados -----")
        try:
            resposta = QMessageBox.question(self, "Confirmação",
                                             "Tem certeza que deseja excluir TODOS os dados do banco de dados?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if resposta == QMessageBox.Yes:
                excluir_dados_banco()
                QMessageBox.information(self, "Sucesso", "Dados excluídos do banco de dados!")
            print("----- Fim de excluir_dados -----")
        except Exception as e:
            print(f"Erro em excluir_dados: {e}")