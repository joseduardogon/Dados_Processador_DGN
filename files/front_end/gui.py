from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from analista_dados.files.back_end.interpretador import validar_arquivo

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Digitalização")
        self.setStyleSheet("background-color: #f0f0f0;")

        # Layouts
        layout_principal = QVBoxLayout()
        layout_campos = QHBoxLayout()
        layout_botoes = QHBoxLayout()

        # Rótulos e campos de entrada
        label_supervisor = QLabel("Nome do Supervisor:", self)
        self.campo_supervisor = QLineEdit(self)
        layout_campos.addWidget(label_supervisor)
        layout_campos.addWidget(self.campo_supervisor)

        label_unidade = QLabel("Unidade:", self)
        self.campo_unidade = QLineEdit(self)
        layout_campos.addWidget(label_unidade)
        layout_campos.addWidget(self.campo_unidade)

        # Botões
        self.botao_confirmar = QPushButton("Confirmar", self)
        self.botao_confirmar.clicked.connect(self.validar_campos)
        layout_botoes.addWidget(self.botao_confirmar)

        self.botao_selecionar = QPushButton("Selecionar Arquivo", self)
        self.botao_selecionar.clicked.connect(self.abrir_seletor_arquivo)
        self.botao_selecionar.setEnabled(False)
        layout_botoes.addWidget(self.botao_selecionar)

        # Adicionando layouts ao layout principal
        layout_principal.addLayout(layout_campos)
        layout_principal.addLayout(layout_botoes)
        self.setLayout(layout_principal)

        # Centraliza o botão na tela
        self.centrar_widget(self.botao_selecionar)

        # Define as flags da janela para permitir bordas
        self.setWindowFlags(self.windowFlags() | Qt.Window)

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
            QMessageBox.information(self, "Sucesso", "Campos preenchidos corretamente!")
            # Desabilita os campos após a confirmação
            self.campo_supervisor.setEnabled(False)
            self.campo_unidade.setEnabled(False)
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")

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