import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox, QFileDialog, QFileDialog)
import csv
import os

from analista_dados.files.datanalysis.importar_arquivo import printar_dicionarios
from importar_arquivo import ler_excel_para_dicionarios
from manipular_database import inserir_dados_no_banco, ler_dados_do_banco

class Janela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controle de Produtividade")
        self.layout = QVBoxLayout()
        self.tabela = QTableWidget()
        self.tabela.setEditTriggers(QTableWidget.AllEditTriggers)  # Permite editar todas as células

        self.botoes()
        self.layout.addWidget(QLabel("Dados de Funcionários:"))
        self.layout.addWidget(self.tabela)
        self.setLayout(self.layout)

        # ComboBox para escolher o funcionário
        self.combo_usuario = QComboBox()
        self.atualizar_combo()
        self.layout.addWidget(self.combo_usuario)

        self.combo_usuario.currentIndexChanged.connect(self.carregar_dados)

    def botoes(self):
        """Cria os botões da aplicação."""
        hbox = QHBoxLayout()

        self.botao_selecionar = QPushButton("Selecionar Arquivo")
        self.botao_selecionar.clicked.connect(self.selecionar_arquivo)
        hbox.addWidget(self.botao_selecionar)

        self.layout.addLayout(hbox)

    def selecionar_arquivo(self):
        """Abre uma caixa de diálogo para o usuário selecionar o arquivo."""
        caminho_arquivo, _ = QFileDialog.getOpenFileName(
            self,  # A janela pai
            "Selecione um arquivo",  # Título da janela
            "C:\\Users\\josed\\codes\\project\\teste",  # Diretório inicial (vazio: o usuário escolhe)
            "Todos os arquivos (*);;Arquivos de Texto (*.txt);;Arquivos Excel (*.xlsx)"  # Filtros de arquivos
        )
        if caminho_arquivo:  # Verifica se o usuário selecionou um arquivo
            try:
                dados = ler_excel_para_dicionarios(caminho_arquivo)
                printar_dicionarios(dados)
                inserir_dados_no_banco(dados)  # Insere os dados no banco de dados
                self.popular_tabela(ler_dados_do_banco())  # Carrega os dados do banco de dados
            except ValueError as erro:
                QMessageBox.warning(self, "Erro", str(erro))
                print(f"Erro: {erro}")

    def popular_tabela(self, dados):
        """Popula a tabela com dados do MongoDB."""
        # Limpa a tabela anterior
        self.tabela.clear()

        # Define a estrutura da tabela
        self.tabela.setColumnCount(15)
        self.tabela.setHorizontalHeaderLabels(
            ['Legenda', 'Status', 'Fase', 'Pastas Aprovadas', 'Imagens Aprovadas', 'Documentos Aprovados',
             'Tempo Aprovado', 'Pastas Rejeitadas', 'Imagens Rejeitadas', 'Documentos Rejeitados',
             'Tempo Rejeitado', 'Total de Pastas', 'Total de Imagens', 'Total de Documentos',
             'Total de Tempo'])

        # Popula a tabela com os dados do MongoDB
        self.tabela.setRowCount(len(dados))
        row = 0
        for documento in dados:
            col = 0
            for chave in documento:
                # Define o valor para cada célula da tabela
                if chave == '2023-10-26':
                    self.tabela.setItem(row, col, QTableWidgetItem(str(documento[chave]['Tempo Aprovado'])))
                else:
                    self.tabela.setItem(row, col, QTableWidgetItem(str(documento[chave])))
                col += 1
            row += 1

    def atualizar_combo(self):
        """Atualiza a ComboBox com os nomes dos arquivos CSV."""
        self.combo_usuario.clear()
        for filename in os.listdir('data'):
            if filename.endswith('.csv'):
                nome_usuario = os.path.splitext(filename)[0]
                self.combo_usuario.addItem(nome_usuario)

    def carregar_dados(self):
        """Carrega os dados do arquivo CSV selecionado no ComboBox."""
        usuario_selecionado = self.combo_usuario.currentText()
        if usuario_selecionado:
            caminho_arquivo = os.path.join('data', f"{usuario_selecionado}.csv")
            with open(caminho_arquivo, 'r') as arquivo:
                leitor = csv.DictReader(arquivo)  # Lê como dicionário para manter a estrutura das colunas
                # Conversão para a estrutura que você está usando (com Tempo Aprovado etc)
                dados = []
                for linha in leitor:
                    dados.append({
                        'Legenda': linha['Legenda'],
                        'Status': linha['Status'],
                        'Fase': linha['Fase'],
                        'Pastas Aprovadas': linha['Pastas Aprovadas'],
                        'Imagens Aprovadas': linha['Imagens Aprovadas'],
                        'Documentos Aprovadas': linha['Documentos Aprovadas'],
                        'Tempo Aprovado': linha['Tempo Aprovado'],
                        'Pastas Rejeitadas': linha['Pastas Rejeitadas'],
                        'Imagens Rejeitadas': linha['Imagens Rejeitadas'],
                        'Documentos Rejeitados': linha['Documentos Rejeitados'],
                        'Tempo Rejeitado': linha['Tempo Rejeitado'],
                        'Total de Pastas': linha['Total de Pastas'],
                        'Total de Imagens': linha['Total de Imagens'],
                        'Total de Documentos': linha['Total de Documentos'],
                        'Total de Tempo': linha['Total de Tempo'],
                        '2023-10-26': {
                            'Tempo Aprovado': linha['Tempo Aprovado'],
                        },
                        '2023-10-27': {
                            'Tempo Aprovado': linha['Tempo Aprovado'],
                        }
                    })
                self.popular_tabela(dados)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = Janela()
    janela.show()
    sys.exit(app.exec_())