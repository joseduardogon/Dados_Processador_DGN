from PySide6.QtWidgets import QApplication, QWidget, QLabel, QProgressBar
from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QFont, QPainterPath, QRegion

class LoadingScreen(QWidget):
    loading_completo = Signal()  # Sinal emitido quando a loading screen termina

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processando...")
        self.setGeometry(0, 0, 300, 100)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")

        label = QLabel("Processando dados...", self)
        label.setGeometry(30, 10, 240, 15)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 14))

        # Barra de Progresso
        self.progresso = QProgressBar(self)
        self.progresso.setGeometry(20, 50, 260, 10)
        self.progresso.setValue(0)

        self.centrar_janela()
        self.criar_mascara_arredondada(16)

    def centrar_janela(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def criar_mascara_arredondada(self, radius):
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, self.width(), self.height()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def atualizar_progresso(self, valor):
        valor_atual = self.progresso.value()
        self.progresso.setValue(valor_atual + valor)
        print("atualizado interpretador")

    def finalizar_loading(self):
        """Emite o sinal de loading completo e fecha a tela."""
        self.loading_completo.emit()
        self.close()
        print("loading interpretador fim")