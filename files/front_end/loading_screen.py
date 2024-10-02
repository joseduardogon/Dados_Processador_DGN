from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer, QRectF, pyqtSignal
from PyQt5.QtGui import QFont, QPainterPath, QRegion

class LoadingScreen(QWidget):
    loading_completo = pyqtSignal()  # Sinal emitido quando a loading screen termina

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicializando...")
        self.setGeometry(0, 0, 300, 100)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")

        label = QLabel("Inicializando...", self)
        label.setGeometry(30, 10, 240, 15)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 14))

        # Barra de Progresso
        self.progresso = QProgressBar(self)
        self.progresso.setGeometry(20, 50, 260, 10)
        self.progresso.setValue(0)

        self.centrar_janela()
        self.criar_mascara_arredondada(16)

        # Configuração do timer para atualização da barra de progresso
        self.timer_progresso = QTimer()
        self.timer_progresso.timeout.connect(self.atualizar_progresso)
        self.timer_progresso.start(50)

        # Simula um processo de inicialização (3 segundos)
        QTimer.singleShot(3000, self.finalizar_loading)

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

    def atualizar_progresso(self):
        valor_atual = self.progresso.value()
        if valor_atual < 100:
            self.progresso.setValue(valor_atual + 3)
        else:
            self.timer_progresso.stop()

    def finalizar_loading(self):
        """Emite o sinal de loading completo e fecha a tela."""
        self.loading_completo.emit()
        self.close()