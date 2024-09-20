from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QMenuBar, QMenu, QAction  # Importe QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from analista_dados.files.back_end.interpretador import validar_arquivo, excluir_dados_banco
from .styles import STYLESHEET  # Importa a stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Digitalização")
        self.setStyleSheet(STYLESHEET)

        # 1. Criar a barra de menus
        barra_menus = self.menuBar() # Use self.menuBar()

        label_logo = QLabel(self)
        pixmap_logo = QPixmap("front_end/logo.png")
        label_logo.setPixmap(pixmap_logo)
        label_logo.setFixedSize(pixmap_logo.width(), pixmap_logo.height())
        barra_menus.setCornerWidget(label_logo, Qt.TopLeftCorner)  # Define o logo no canto superior esque

        menu_arquivo = QMenu("Arquivo", self)
        barra_menus.addMenu(menu_arquivo)

        menu_configuracoes = QMenu("Configurações", self)
        barra_menus.addMenu(menu_configuracoes)
        acao_excluir_dados = QAction("Excluir Dados do Banco", self)
        menu_configuracoes.addAction(acao_excluir_dados)

        acao_excluir_dados.triggered.connect(self.excluir_dados)

        acao_importar = QAction("Importar Arquivo", self)
        menu_arquivo.addAction(acao_importar)

        acao_preferencias = QAction("Preferências", self)
        menu_configuracoes.addAction(acao_preferencias)

        # 2. Criar um widget central para os layouts
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        # 3. Layouts
        layout_principal = QVBoxLayout()
        layout_campos = QVBoxLayout()
        layout_botao_confirmar = QHBoxLayout()
        layout_botoes_arquivo = QHBoxLayout()

        # Rótulos e campos de entrada
        print("Criando rótulos e campos de entrada...")
        label_supervisor = QLabel("Nome do Supervisor:", self)
        self.campo_supervisor = QLineEdit(self)
        layout_campos.addWidget(label_supervisor)
        layout_campos.addWidget(self.campo_supervisor)

        label_unidade = QLabel("Unidade:", self)
        self.campo_unidade = QLineEdit(self)
        layout_campos.addWidget(label_unidade)
        layout_campos.addWidget(self.campo_unidade)
        print("Rótulos e campos de entrada criados e adicionados ao layout.")

        # Botões
        print("Criando botões...")
        self.botao_confirmar = QPushButton("Confirmar", self)
        self.botao_confirmar.clicked.connect(self.validar_campos)
        layout_botao_confirmar.addWidget(self.botao_confirmar)
        layout_botao_confirmar.setAlignment(Qt.AlignCenter)

        self.botao_selecionar = QPushButton("Selecionar Arquivo", self)
        self.botao_selecionar.clicked.connect(self.abrir_seletor_arquivo)
        self.botao_selecionar.setEnabled(False)
        layout_botoes_arquivo.addWidget(self.botao_selecionar)

        self.botao_cancelar = QPushButton("Cancelar", self)
        self.botao_cancelar.clicked.connect(self.cancelar_selecao)
        self.botao_cancelar.setEnabled(False)
        layout_botoes_arquivo.addWidget(self.botao_cancelar)
        print("Botões criados e adicionados aos layouts.")

        # Adicionando layouts ao layout principal
        print("Adicionando layouts ao layout principal...")
        layout_principal.addLayout(layout_campos)
        layout_principal.addLayout(layout_botao_confirmar)
        layout_principal.addLayout(layout_botoes_arquivo)
        print("Layouts adicionados ao layout principal.")

        print("Definindo layout principal na janela...")
        self.setLayout(layout_principal)
        print("Layout principal definido na janela.")

        # Define os objectName dos botões
        print("Definindo objectNames dos botões...")
        self.botao_confirmar.setObjectName("botao_confirmar")
        self.botao_selecionar.setObjectName("botao_selecionar")
        self.botao_cancelar.setObjectName("botao_cancelar")
        print("objectNames dos botões definidos.")

        # Define as flags da janela para permitir bordas
        print("Definindo flags da janela...")
        self.setWindowFlags(self.windowFlags() | Qt.Window)
        widget_central.setLayout(layout_principal)
        print("Flags da janela definidas.")

        print("----- Fim do __init__ da MainWindow -----")

    def centrar_widget(self, widget):
        """Centraliza um widget na janela."""
        qr = widget.frameGeometry()
        cp = self.frameGeometry().center()
        qr.moveCenter(cp)
        widget.move(qr.topLeft())

    def validar_campos(self):
        """Valida os campos e desabilita a edição."""
        supervisor = self.campo_supervisor.text()
        unidade = self.campo_unidade.text()
        if supervisor and unidade:
            self.botao_selecionar.setEnabled(True)
            self.botao_cancelar.setEnabled(True)  # Habilita o botão Cancelar
            QMessageBox.information(self, "Sucesso", "Campos preenchidos corretamente!")
            self.campo_supervisor.setEnabled(False)
            self.campo_unidade.setEnabled(False)
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")

    def cancelar_selecao(self):
        """Limpa os campos e desabilita os botões."""
        self.campo_supervisor.setText("")
        self.campo_unidade.setText("")
        self.campo_supervisor.setEnabled(True)
        self.campo_unidade.setEnabled(True)
        self.botao_selecionar.setEnabled(False)
        self.botao_cancelar.setEnabled(False)

    def abrir_seletor_arquivo(self):
        """Abre a janela de diálogo para seleção de arquivo e valida a extensão."""
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecione um Arquivo")
        if arquivo:
            if validar_arquivo(arquivo, self.campo_supervisor.text(), self.campo_unidade.text()):
                # Arquivo válido - prossiga com o processamento
                print("Arquivo válido selecionado:", arquivo)
            else:
                # Arquivo inválido - mostre uma mensagem de erro
                QMessageBox.warning(self, "Erro", "Tipo de arquivo inválido. Selecione um arquivo .txt ou .xlsx.")

    def excluir_dados(self):
        """Exclui os dados do banco de dados (apenas para protótipo!)."""
        resposta = QMessageBox.question(self, "Confirmação",
                                        "Tem certeza que deseja excluir TODOS os dados do banco de dados?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            excluir_dados_banco()  # Chame a função de interpretador.py
            QMessageBox.information(self, "Sucesso", "Dados excluídos do banco de dados!")