import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QFont, QPainterPath, QRegion
from analista_dados.files.front_end.gui import MainWindow

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicializando...")
        self.setGeometry(0, 0, 300, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")

        label = QLabel("Inicializando...", self)
        label.setGeometry(10, 10, 280, 20)  # Ajuste a posição para a barra
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 14))  # Fonte menor

        # Barra de Progresso
        self.progresso = QProgressBar(self)
        self.progresso.setGeometry(20, 50, 260, 15)  # Posição abaixo do label
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

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.splash = SplashScreen()
        self.splash.show()

        # Configuração do timer para atualização da barra de progresso
        self.timer_progresso = QTimer()
        self.timer_progresso.timeout.connect(self.atualizar_progresso)
        self.timer_progresso.start(50)  # A cada 100ms a barra é atualizada

        # Simula um processo de inicialização (3 segundos)
        QTimer.singleShot(3000, self.iniciar_janela_principal)

        sys.exit(self.app.exec_())

    def iniciar_janela_principal(self):
        self.janela_principal = MainWindow()
        self.janela_principal.showMaximized()  # Maximiza a janela primeiro
        self.splash.close()

    def atualizar_progresso(self):
        valor_atual = self.splash.progresso.value()
        if valor_atual < 100:
            self.splash.progresso.setValue(valor_atual + 3) # Incrementa de 1 em 1
        else:
            self.timer_progresso.stop()

if __name__ == '__main__':
    aplicacao = App()