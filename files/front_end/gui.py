from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Digitalização")
        # self.setGeometry(100, 100, 800, 600)  # Descomente para tamanho fixo
        self.setStyleSheet("background-color: #f0f0f0;")

        botao = QPushButton("Clique aqui", self)
        botao.setGeometry(350, 250, 100, 50)

        # Centraliza a janela na tela
        self.centrar_janela()

        # Define as flags da janela para permitir bordas
        self.setWindowFlags(self.windowFlags() | Qt.Window)

    def centrar_janela(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())