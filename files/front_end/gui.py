from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QPushButton, QFileDialog,
                             QMessageBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QMenuBar,
                             QMenu, QAction, QTabWidget, QTableWidget, QComboBox, QTableWidgetItem)  # Importe QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from analista_dados.files.back_end.interpretador import validar_arquivo, excluir_dados_banco
from .styles import STYLESHEET  # Importa a stylesheet
from analista_dados.files.back_end.desempenho_unidade import obter_estatisticas_unidade
from .estatisticas import criar_tabela_estatisticas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("----- Iniciando __init__ da MainWindow -----")

        print("Definindo título da janela...")
        self.setWindowTitle("Sistema de Digitalização")
        print("Título da janela definido.")

        # 1. Criar o QTabWidget
        print("Criando QTabWidget...")
        try:
            self.abas = QTabWidget(self)
            print("QTabWidget criado.")
        except Exception as e:
            print(f"Erro ao criar QTabWidget: {e}")
            return  # Encerra a inicialização se houver erro

        print("Definindo QTabWidget como widget central...")
        try:
            self.setCentralWidget(self.abas)
            print("QTabWidget definido como widget central.")
        except Exception as e:
            print(f"Erro ao definir widget central: {e}")
            return

        # 2. Criar os widgets para as abas
        print("Criando abas...")
        try:
            self.criar_aba_importar()
            self.criar_aba_desempenho()  # Nova aba
            self.criar_aba_configuracoes()
            print("Abas criadas.")
        except Exception as e:
            print(f"Erro ao criar abas: {e}")
            return

        # 3. Layouts
        print("Criando layouts...")
        try:
            layout_principal = QVBoxLayout()
            layout_logo = QHBoxLayout()
            print("Layouts criados.")
        except Exception as e:
            print(f"Erro ao criar layouts: {e}")
            return

        # --- Logo ---
        print("Adicionando logo...")
        try:
            label_logo = QLabel(self)
            pixmap_logo = QPixmap("front_end/logo.png")
            label_logo.setPixmap(pixmap_logo)
            label_logo.setFixedSize(pixmap_logo.width(), pixmap_logo.height())
            layout_logo.addWidget(label_logo)
            print("Logo adicionado ao layout.")
        except Exception as e:
            print(f"Erro ao adicionar logo: {e}")

        print("Adicionando layouts ao layout principal...")
        try:
            layout_principal.addLayout(layout_logo)
            layout_principal.addWidget(self.abas)
            print("Layouts adicionados ao layout principal.")
        except Exception as e:
            print(f"Erro ao adicionar layouts ao layout principal: {e}")

        # Widget central
        print("Criando widget central...")
        try:
            widget_central = QWidget()
            widget_central.setLayout(layout_principal)
            self.setCentralWidget(widget_central)
            print("Widget central criado e definido.")
        except Exception as e:
            print(f"Erro ao criar ou definir widget central: {e}")

        # 4. Aplicar a StyleSheet
        print("Aplicando StyleSheet...")
        try:
            self.setStyleSheet(STYLESHEET)
            print("StyleSheet aplicada.")
        except Exception as e:
            print(f"Erro ao aplicar StyleSheet: {e}")

        # 5. Mover a aba "Configurações" para o canto direito
        print("Movendo aba 'Configurações'...")
        try:
            self.abas.tabBar().moveTab(1, 3)
            print("Aba 'Configurações movida.")
        except Exception as e:
            print(f"Erro ao mover aba 'Configurações': {e}")

        print("----- Fim do __init__ da MainWindow -----")

    def criar_aba_desempenho(self):
        """Cria a aba 'Desempenho'."""
        widget_principal = QWidget()
        abas_internas = QTabWidget(widget_principal)
        layout_principal = QVBoxLayout(widget_principal)
        layout_principal.addWidget(abas_internas)

        self.criar_subaba_unidade(abas_internas)  # Cria a subaba "Unidade"
        #self.criar_subaba_funcionarios(abas_internas)

        self.abas.addTab(widget_principal, "Desempenho")
        self.abas.tabBar().moveTab(1, 3)

        subaba2 = QWidget()
        layout_subaba2 = QVBoxLayout()
        layout_subaba2.addWidget(QLabel("Label na Subaba 2"))
        subaba2.setLayout(layout_subaba2)

        abas_internas.addTab(subaba2, "Funcionarios")  # Mudança de nome: Subaba 2 -> Funcionarios

        # Adiciona o widget principal com as subabas ao QTabWidget principal
        self.abas.addTab(widget_principal, "Desempenho")  # Mudança de nome:  Aba com Subabas -> Desempenho

    def criar_subaba_unidade(self, abas_internas):
        """Cria a subaba 'Unidade'."""
        self.widget_unidade = QWidget()
        layout_unidade = QVBoxLayout(self.widget_unidade)

        # Seletor de datas
        self.seletor_data = QComboBox()
        # Remova a conexão aqui:  self.seletor_data.currentIndexChanged.connect(self.atualizar_tabela_unidade)
        layout_unidade.addWidget(self.seletor_data)

        # Botão "Gerar"
        botao_gerar = QPushButton("Gerar", self)
        botao_gerar.clicked.connect(self.atualizar_tabela_unidade)  # Conecte ao método
        layout_unidade.addWidget(botao_gerar)

        # Tabela para exibir as estatísticas da unidade
        self.tabela_unidade = criar_tabela_estatisticas({})
        layout_unidade.addWidget(self.tabela_unidade)

        abas_internas.addTab(self.widget_unidade, "Unidade")

    def atualizar_estatisticas_unidade(self):
        """Atualiza as opções de data no seletor."""
        print("----- Iniciando atualizar_estatisticas_unidade -----")
        try:
            unidade = self.campo_unidade.text()
            estatisticas = obter_estatisticas_unidade(unidade)  # Busca todas as datas

            # Atualiza as datas no seletor
            datas = sorted(estatisticas.keys())
            self.seletor_data.clear()
            self.seletor_data.addItems(datas)
            print("----- Fim de atualizar_estatisticas_unidade -----")
        except Exception as e:
            print(f"Erro em atualizar_estatisticas_unidade: {e}")

    def atualizar_tabela_unidade(self):
        """Atualiza a tabela com as estatísticas da unidade."""
        print("----- Iniciando atualizar_tabela_unidade -----")
        try:
            unidade = self.campo_unidade.text()
            data_selecionada = self.seletor_data.currentText()

            # --- Atualiza a tabela ---
            self.tabela_unidade.setRowCount(0)  # Limpa a tabela

            if data_selecionada:  # Só atualiza se uma data foi selecionada
                estatisticas = obter_estatisticas_unidade(unidade, data_selecionada)
                row_index = 0
                for data, fases in estatisticas.items():
                    for fase, total_imagens in fases.items():
                        self.tabela_unidade.insertRow(row_index)
                        self.tabela_unidade.setItem(row_index, 0, QTableWidgetItem(str(data)))
                        self.tabela_unidade.setItem(row_index, 1, QTableWidgetItem(fase))
                        self.tabela_unidade.setItem(row_index, 2, QTableWidgetItem(str(total_imagens)))
                        row_index += 1

            self.tabela_unidade.resizeColumnsToContents()
            # ---------------------------

            print("----- Fim de atualizar_tabela_unidade -----")
        except Exception as e:
            print(f"Erro em atualizar_tabela_unidade: {e}")

    def criar_aba_importar(self):
        """Cria a aba 'Importar Arquivo'."""
        print("----- Iniciando criar_aba_importar -----")
        try:
            widget_importar = QWidget()
            layout_importar = QVBoxLayout()
            layout_campos = QVBoxLayout()
            layout_botao_confirmar = QHBoxLayout()
            layout_botoes_arquivo = QHBoxLayout()

            label_supervisor = QLabel("Nome do Supervisor:", self)
            self.campo_supervisor = QLineEdit(self)
            layout_campos.addWidget(label_supervisor)
            layout_campos.addWidget(self.campo_supervisor)

            label_unidade = QLabel("Unidade:", self)
            self.campo_unidade = QLineEdit(self)
            layout_campos.addWidget(label_unidade)
            layout_campos.addWidget(self.campo_unidade)

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

            layout_importar.addLayout(layout_campos)
            layout_importar.addLayout(layout_botao_confirmar)
            layout_importar.addLayout(layout_botoes_arquivo)

            widget_importar.setLayout(layout_importar)
            self.abas.addTab(widget_importar, "Importar")

            self.botao_confirmar.setObjectName("botao_confirmar")
            self.botao_selecionar.setObjectName("botao_selecionar")
            self.botao_cancelar.setObjectName("botao_cancelar")
            print("----- Fim de criar_aba_importar -----")
        except Exception as e:
            print(f"Erro em criar_aba_importar: {e}")

    def criar_aba_configuracoes(self):
        """Cria a aba 'Configurações'."""
        print("----- Iniciando criar_aba_configuracoes -----")
        try:
            widget_configuracoes = QWidget()
            layout_configuracoes = QVBoxLayout()

            botao_excluir_dados = QPushButton("Excluir Dados do Banco", self)
            botao_excluir_dados.setObjectName("botao_cancelar")
            botao_excluir_dados.clicked.connect(self.excluir_dados)
            layout_configuracoes.addWidget(botao_excluir_dados)

            widget_configuracoes.setLayout(layout_configuracoes)
            self.abas.addTab(widget_configuracoes, "Configurações")
            print("----- Fim de criar_aba_configuracoes -----")
        except Exception as e:
            print(f"Erro em criar_aba_configuracoes: {e}")

    def validar_campos(self):
        """Valida os campos e desabilita a edição."""
        print("----- Iniciando validar_campos -----")
        try:
            supervisor = self.campo_supervisor.text()
            unidade = self.campo_unidade.text()
            if supervisor and unidade:
                self.botao_selecionar.setEnabled(True)
                self.botao_cancelar.setEnabled(True)
                QMessageBox.information(self, "Sucesso", "Campos preenchidos corretamente!")
                self.campo_supervisor.setEnabled(False)
                self.campo_unidade.setEnabled(False)
                self.atualizar_estatisticas_unidade()
                #self.gerar_graficos_unidade()  # Adicione esta linha para chamar a função
                print("----- Fim de validar_campos -----")
            else:
                QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
                print("----- Fim de validar_campos -----")
        except Exception as e:
            print(f"Erro em validar_campos: {e}")

    def cancelar_selecao(self):
        """Limpa os campos e desabilita os botões."""
        print("----- Iniciando cancelar_selecao -----")
        try:
            self.campo_supervisor.setText("")
            self.campo_unidade.setText("")
            self.campo_supervisor.setEnabled(True)
            self.campo_unidade.setEnabled(True)
            self.botao_selecionar.setEnabled(False)
            self.botao_cancelar.setEnabled(False)
            print("----- Fim de cancelar_selecao -----")
        except Exception as e:
            print(f"Erro em cancelar_selecao: {e}")

    def abrir_seletor_arquivo(self):
        """Abre a janela de diálogo para seleção de arquivo e valida a extensão."""
        print("----- Iniciando abrir_seletor_arquivo -----")
        try:
            arquivo, _ = QFileDialog.getOpenFileName(self, "Selecione um Arquivo")
            if arquivo:
                if validar_arquivo(arquivo, self.campo_supervisor.text(), self.campo_unidade.text()):
                    print("Arquivo válido selecionado:", arquivo)
                    print("----- Fim de abrir_seletor_arquivo -----")
                else:
                    QMessageBox.warning(self, "Erro",
                                        "Tipo de arquivo inválido. Selecione um arquivo .txt ou .xlsx.")
                    print("----- Fim de abrir_seletor_arquivo -----")
        except Exception as e:
            print(f"Erro em abrir_seletor_arquivo: {e}")

    def excluir_dados(self):
        """Exclui os dados do banco de dados (apenas para protótipo!)."""
        print("----- Iniciando excluir_dados -----")
        try:
            resposta = QMessageBox.question(self, "Confirmação",
                                             "Tem certeza que deseja excluir TODOS os dados do banco de dados?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if resposta == QMessageBox.Yes:
                excluir_dados_banco()
                QMessageBox.information(self, "Sucesso", "Dados excluídos do banco de dados!")
            print("----- Fim de excluir_dados -----")
        except Exception as e:
            print(f"Erro em excluir_dados: {e}")
