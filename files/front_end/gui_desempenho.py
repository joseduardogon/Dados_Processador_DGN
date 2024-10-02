from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTabWidget, QTableWidget, QComboBox, QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt

from analista_dados.files.back_end.desempenho_unidade import obter_estatisticas_unidade, obter_meses_anos_disponiveis
from analista_dados.files.back_end.desempenho_funcionario import obter_estatisticas_funcionario
from .estatisticas import criar_tabela_estatisticas, criar_tabela_funcionarios

class DesempenhoWidget(QWidget):
    def __init__(self, usuario, parent=None):
        """Inicializa a aba 'Desempenho'."""
        super().__init__(parent)

        # Armazene os dados do usuário
        self.usuario_atual = usuario
        print(f"gui_desempenho:{self.usuario_atual}")

        print("----- Iniciando __init__ da DesempenhoWidget -----")
        try:
            layout_principal = QVBoxLayout(self)

            # Criar as subabas
            self.abas_internas = QTabWidget(self)
            layout_principal.addWidget(self.abas_internas)
            self.criar_subaba_unidade()
            self.criar_subaba_funcionarios()

            print("----- Fim do __init__ da DesempenhoWidget -----")
        except Exception as e:
            print(f"Erro no __init__ da DesempenhoWidget: {e}")

    def criar_subaba_unidade(self):
        """Cria a subaba 'Unidade'."""
        print("----- Iniciando criar_subaba_unidade -----")
        try:
            self.widget_unidade = QWidget()
            layout_unidade = QVBoxLayout(self.widget_unidade)

            # Layout horizontal para os seletores de data
            layout_seletores_data = QHBoxLayout()

            # Seletor de Mês/Ano
            self.seletor_mes_ano = QComboBox(self)
            #self.seletor_mes_ano.currentIndexChanged.connect(self.habilitar_campo_dia)
            layout_seletores_data.addWidget(self.seletor_mes_ano)

            # Campo para digitar o dia
            self.campo_dia = QLineEdit(self)
            self.campo_dia.setPlaceholderText("Dia")
            self.campo_dia.setEnabled(True)
            self.campo_dia.setFixedWidth(40)
            layout_seletores_data.addWidget(self.campo_dia)

            # Botão "Gerar"
            botao_gerar = QPushButton("Gerar", self)
            botao_gerar.setObjectName("botao_selecionar")
            botao_gerar.setMaximumSize(120, 40)
            botao_gerar.clicked.connect(self.atualizar_tabela_unidade)
            layout_seletores_data.addWidget(botao_gerar)

            layout_unidade.addLayout(layout_seletores_data)

            # Tabela para exibir as estatísticas da unidade
            self.tabela_unidade = criar_tabela_estatisticas({})
            layout_unidade.addWidget(self.tabela_unidade)

            self.abas_internas.addTab(self.widget_unidade, "Unidade")

            # --- Remova a chamada de self.atualizar_estatisticas_unidade() daqui  ---
            # --- Ela será chamada em validar_campos em gui.py ---

            print("----- Fim de criar_subaba_unidade -----")
        except Exception as e:
            print(f"Erro em criar_subaba_unidade: {e}")

    def atualizar_tabela_unidade(self):
        """Atualiza a tabela com as estatísticas da unidade."""
        print("----- Iniciando atualizar_tabela_unidade -----")
        try:
            global usuario_atual
            unidade = self.usuario_atual['unidade']
            mes_ano = self.seletor_mes_ano.currentText()
            dia = self.campo_dia.text()

            # Verifica se o mês/ano e o dia foram selecionados
            if not (mes_ano and dia):
                QMessageBox.warning(self, "Erro", "Selecione o Mês/Ano e o Dia.")
                return

            # Formata a data
            mes, ano = mes_ano.split('/')
            data_selecionada = f"{ano}-{mes}-{dia.zfill(2)}"  # Formato aaaa-mm-dd

            print("----- Fim de atualizar_tabela_unidade -----")
        except Exception as e:
            print(f"Erro em atualizar_tabela_unidade: {e}")

    def criar_subaba_funcionarios(self):
        """Cria a subaba 'Funcionarios'."""
        print("----- Iniciando criar_subaba_funcionarios -----")
        try:
            self.widget_funcionarios = QWidget()
            layout_funcionarios = QVBoxLayout(self.widget_funcionarios)

            # Layout horizontal para o botão "Gerar"
            layout_botao_gerar = QHBoxLayout()
            botao_gerar_funcionarios = QPushButton("Gerar", self)
            botao_gerar_funcionarios.setObjectName("botao_selecionar")
            botao_gerar_funcionarios.setMaximumSize(300, 40)
            botao_gerar_funcionarios.clicked.connect(self.atualizar_tabela_funcionarios)
            layout_botao_gerar.addWidget(botao_gerar_funcionarios)
            layout_botao_gerar.setAlignment(Qt.AlignCenter)

            # Tabela para exibir as estatísticas dos funcionários
            self.tabela_funcionarios = criar_tabela_estatisticas({})
            layout_funcionarios.addWidget(self.tabela_funcionarios)

            layout_funcionarios.addLayout(layout_botao_gerar)

            self.abas_internas.addTab(self.widget_funcionarios, "Funcionarios")

            print("----- Fim de criar_subaba_funcionarios -----")
        except Exception as e:
            print(f"Erro em criar_subaba_funcionarios: {e}")

    def atualizar_tabela_funcionarios(self):
        """Atualiza a tabela com as estatísticas dos funcionários."""
        print("----- Iniciando atualizar_tabela_funcionarios -----")
        try:
            unidade = self.usuario_atual['unidade']
            print("Unidade obtida:", unidade)

            print("Obtendo estatísticas do funcionário...")
            estatisticas_funcionarios = obter_estatisticas_funcionario(unidade)
            print("Estatísticas do funcionário obtidas.")

            # Obter todas as datas únicas
            print("Obtendo datas únicas...")
            todas_datas = set()
            for func, dados in estatisticas_funcionarios.items():
                for data in dados['dias']:
                    todas_datas.add(data)
            datas_ordenadas = sorted(todas_datas, reverse=True)
            print("Datas únicas obtidas:", datas_ordenadas)

            # Define as colunas da tabela
            print("Definindo colunas da tabela...")
            colunas = ["Funcionário - Tarefa", "Média"] + list(
                datas_ordenadas)  # Colunas: Funcionário - Tarefa, Média e Datas
            self.tabela_funcionarios.setColumnCount(len(colunas))
            self.tabela_funcionarios.setHorizontalHeaderLabels(colunas)
            print("Colunas da tabela definidas.")

            print("Limpando tabela...")
            self.tabela_funcionarios.setRowCount(0)  # Limpa a tabela
            print("Tabela limpa.")

            print("Preenchendo a tabela...")
            row_index = 0
            for funcionario, dados in estatisticas_funcionarios.items():
                print(f"Processando funcionário: {funcionario}")
                # Itera sobre as fases do funcionário
                for fase in dados['fases']:
                    self.tabela_funcionarios.insertRow(row_index)
                    self.tabela_funcionarios.setItem(row_index, 0, QTableWidgetItem(f"{funcionario} - {fase}"))
                    media_fase = estatisticas_funcionarios[funcionario]['medias'].get(fase, 0)
                    self.tabela_funcionarios.setItem(row_index, 1, QTableWidgetItem(f"{media_fase:.2f}"))

                    col_index = 2
                    # Preenche os totais de cada data para a fase
                    for data in datas_ordenadas:
                        total = dados['dias'].get(data, {}).get(fase, 0)
                        self.tabela_funcionarios.setItem(row_index, col_index, QTableWidgetItem(str(total)))
                        col_index += 1

                    row_index += 1  # Incrementa o índice da linha para a próxima fase do funcionário

            self.tabela_funcionarios.resizeColumnsToContents()
            print("Tabela preenchida.")

            print("----- Fim de atualizar_tabela_funcionarios -----")
        except Exception as e:
            print(f"Erro em atualizar_tabela_funcionarios: {e}")