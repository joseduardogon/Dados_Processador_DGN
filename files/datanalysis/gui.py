import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox, QFileDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
from importar_arquivo import ler_excel_para_dicionarios
from manipular_database import inserir_dados_no_banco, ler_dados_do_banco, conectar_banco
from datetime import date, time, datetime

class Janela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controle de Produtividade")
        self.setWindowIcon(QIcon('icon.png'))  # Substitua  'icon.png' pelo caminho  do  seu ícone
        self.layout = QVBoxLayout()
        self.tabela = QTableWidget()
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)  #  Desabilitar  edição na tabela

        # Criando  o  ComboBox  para  seleção do  usuário
        self.combo_usuario = QComboBox()
        self.atualizar_combo()
        self.layout.addWidget(QLabel("Selecione o Usuário:"))
        self.layout.addWidget(self.combo_usuario)

        self.botoes()
        self.layout.addWidget(QLabel("Dados de Funcionários:"))
        self.layout.addWidget(self.tabela)
        self.setLayout(self.layout)

        # Conecta  o  evento  de  seleção  da  ComboBox  à  função  `carregar_dados`
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
            self,
            "Selecione um arquivo",
            "",
            "Todos os arquivos (*);;Arquivos de Texto (*.txt);;Arquivos Excel (*.xlsx)"
        )
        if caminho_arquivo:
            try:
                dados = ler_excel_para_dicionarios(caminho_arquivo)
                if inserir_dados_no_banco(dados):
                    print("Dados inseridos com sucesso!")
                    self.atualizar_combo() # Atualiza a ComboBox com os novos usuários
                else:
                    QMessageBox.warning(self, "Erro", "Erro ao inserir os dados.")
            except ValueError as erro:
                QMessageBox.warning(self, "Erro", str(erro))
                print(f"Erro ao ler o arquivo: {erro}")

    def popular_tabela(self, dados):
        """Popula a tabela com dados do SQLite."""
        self.tabela.clear()
        # Define a  quantidade  de colunas  baseado nos dados:
        if dados:
            self.tabela.setColumnCount(len(dados[0]))
            # Define  os  cabeçalhos:
            self.tabela.setHorizontalHeaderLabels(dados[0].keys())
        else:
            self.tabela.setColumnCount(0)
            self.tabela.setHorizontalHeaderLabels([])

        self.tabela.setRowCount(len(dados))
        for row, documento in enumerate(dados):
            for col, (chave, valor) in enumerate(documento.items()):
                # Converter para string  (se necessário):
                if isinstance(valor, (date, datetime, time)):
                    valor = valor.strftime("%Y-%m-%d %H:%M:%S")
                item = QTableWidgetItem(str(valor))
                self.tabela.setItem(row, col, item)


    def atualizar_combo(self):
        """Atualiza a ComboBox com os nomes das tabelas do banco de dados (funcionários)."""
        self.combo_usuario.clear()
        con, cursor = conectar_banco()
        if con and cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tabelas = cursor.fetchall()
            con.close()

            for tabela in tabelas:
                if tabela[0] != 'sqlite_sequence':  # Ignora a tabela sqlite_sequence (interna)
                    self.combo_usuario.addItem(tabela[0])

    def carregar_dados(self):
        """Carrega os dados do funcionário selecionado na ComboBox."""
        nome_tabela = self.combo_usuario.currentText()
        dados = ler_dados_do_banco(nome_tabela)  #  Busca os  dados do  SQLite
        self.popular_tabela(dados)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = Janela()
    janela.show()
    sys.exit(app.exec_())