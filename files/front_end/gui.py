from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMessageBox # Importe QFileDialog
from PyQt5.QtCore import Qt
from analista_dados.files.back_end.interpretador import validar_arquivo


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Digitalização")
        self.setStyleSheet("background-color: #f0f0f0;")

        # Botão "Selecionar Arquivo"
        self.botao_selecionar = QPushButton("Selecionar Arquivo", self)
        self.botao_selecionar.clicked.connect(self.abrir_seletor_arquivo)  # Conecta a função
        self.botao_selecionar.setGeometry(100, 80, 150, 40)  # Ajuste o tamanho se necessário

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

    def abrir_seletor_arquivo(self):
        """Abre a janela de diálogo para seleção de arquivo e valida a extensão."""
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecione um Arquivo")
        if arquivo:
            if validar_arquivo(arquivo):
                # Arquivo válido - prossiga com o processamento
                print("Arquivo válido selecionado:", arquivo)
            else:
                # Arquivo inválido - mostre uma mensagem de erro
                QMessageBox.warning(self, "Erro", "Tipo de arquivo inválido. Selecione um arquivo .txt ou .xlsx.")