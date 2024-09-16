import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QFileDialog
import requests
import csv
import requests

class Janela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controle de Produtividade")
        self.layout = QVBoxLayout()
        self.tabela = QTableWidget()

        self.botoes()
        self.layout.addWidget(QLabel("Dados de Funcionários:"))
        self.layout.addWidget(self.tabela)
        self.setLayout(self.layout)

    def botoes(self):
        self.btn_carregar = QPushButton("Carregar Dados")
        self.btn_carregar.clicked.connect(self.carregar_dados)
        self.layout.addWidget(self.btn_carregar)

        self.btn_salvar = QPushButton("Salvar Dados")
        self.btn_salvar.clicked.connect(self.salvar_dados)
        self.layout.addWidget(self.btn_salvar)

    def carregar_dados(self):
        caminho_arquivo = 'data/data.csv'
        self.popular_tabela(caminho_arquivo)

    def salvar_dados(self):
        caminho_arquivo, _ = QFileDialog.getSaveFileName(self, "Salvar arquivo CSV", "", "CSV (*.csv)")
        if caminho_arquivo:
            self.salvar_tabela(caminho_arquivo)

    def popular_tabela(self, caminho_arquivo):
        # Limpe a tabela anterior (caso haja)
        self.tabela.clear()

        self.tabela.setColumnCount(2)
        self.tabela.setHorizontalHeaderLabels(['Nome', 'Pontuação'])

        with open(caminho_arquivo, 'r', newline='') as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor)
            self.tabela.setRowCount(len(list(leitor)))
            arquivo.seek(0)
            next(leitor)
            row = 0
            for linha in leitor:
                self.tabela.setItem(row, 0, QTableWidgetItem(linha[0]))
                self.tabela.setItem(row, 1, QTableWidgetItem(linha[1]))
                row += 1

    def salvar_tabela(self, caminho_arquivo):
        with open(caminho_arquivo, 'w', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(['Nome', 'Pontuação'])  # Cabeçalho
            for row in range(self.tabela.rowCount()):
                nome = self.tabela.item(row, 0).text()
                pontuacao = self.tabela.item(row, 1).text()
                escritor.writerow([nome, pontuacao])
        print(f'Dados salvos em {caminho_arquivo}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = Janela()
    janela.show()
    sys.exit(app.exec_())