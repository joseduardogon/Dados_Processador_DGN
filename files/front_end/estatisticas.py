from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QSpinBox, QCheckBox

def criar_tabela_estatisticas(dados):
    """Cria uma tabela com as estatísticas da unidade.

    Args:
        dados (dict): Um dicionário contendo as estatísticas da unidade, organizado por data e fase.

    Returns:
        QTableWidget: A tabela com os dados formatados.
    """

    tabela = QTableWidget()
    tabela.setColumnCount(3)  # 3 colunas: Data, Fase, Total de Imagens
    tabela.setHorizontalHeaderLabels(["Data", "Fase", "Total de Imagens"])

    # Estilos para a tabela
    tabela.setStyleSheet("""
        QTableWidget {
            alternate-background-color: #f2f2f2; /* Cor de fundo alternada para linhas */
            font-family: Arial;
            font-size: 12pt;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidgetItem {
            border: 1px solid #ccc; /* Bordas nas células */
        }
        QHeaderView::section { /* Estilo para o cabeçalho */
            background-color: #007BFF; /* Cor de fundo azul */
            color: white;
            padding: 8px;
            font-weight: bold;
        }

        QSpinBox { /* Estilo para células numéricas (inteiros) */
            background-color: #f8f9fa;
            color: #495057;
            border: 1px solid #dee2e6;
        }

        QCheckBox { /* Estilo para células booleanas */
            margin: 5px; /* Ajuste a margem conforme necessário */
        }
    """)

    # Adiciona os dados à tabela
    row_index = 0
    for data, fases in dados.items():
        for fase, total_imagens in fases.items():
            tabela.insertRow(row_index)
            tabela.setItem(row_index, 0, QTableWidgetItem(str(data)))
            tabela.setItem(row_index, 1, QTableWidgetItem(fase))

            # Define a célula da coluna "Total de Imagens" com base no tipo de dado:
            if isinstance(total_imagens, int):
                item = QSpinBox()
                item.setValue(total_imagens)
                tabela.setCellWidget(row_index, 2, item)
            else:
                tabela.setItem(row_index, 2, QTableWidgetItem(str(total_imagens)))

            row_index += 1


    tabela.resizeColumnsToContents()  # Ajusta as colunas ao conteúdo

    return tabela

def criar_tabela_funcionarios(estatisticas):
    """Cria uma tabela com as estatísticas dos funcionários.

    Args:
        estatisticas (dict): Um dicionário contendo as estatísticas dos funcionários.

    Returns:
        QTableWidget: A tabela com os dados formatados.
    """

    tabela = QTableWidget()
    tabela.setStyleSheet("""
        QTableWidget {
            alternate-background-color: #f2f2f2; 
            font-family: Arial;
            font-size: 12pt;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidgetItem {
            border: 1px solid #ccc; 
        }
        QHeaderView::section {
            background-color: #007BFF; 
            color: white;
            padding: 8px;
            font-weight: bold;
        }
    """)

    # Obter as datas em ordem decrescente
    datas = sorted(estatisticas[list(estatisticas.keys())[0]]["datas"].keys(), reverse=True)

    # Criar as colunas da tabela
    colunas = ["Funcionário"]
    for funcionario in estatisticas.keys():
        for fase in estatisticas[funcionario]['fases']:
            colunas.append(f"{fase}")
    tabela.setColumnCount(len(colunas))
    tabela.setHorizontalHeaderLabels(colunas)

    # Adicionar linhas com as médias e totais por data
    row_index = 0
    for funcionario in estatisticas:
        tabela.insertRow(row_index)
        tabela.setItem(row_index, 0, QTableWidgetItem(funcionario))
        col_index = 1
        for fase in estatisticas[funcionario]['fases']:
            # Adicionar a média da fase
            tabela.setItem(row_index, col_index, QTableWidgetItem(f"{estatisticas[funcionario]['medias'][fase]:.2f}"))
            col_index += 1

    # Adicionar linhas para cada data
    for data in datas:
        row_index += 1
        tabela.insertRow(row_index)
        tabela.setItem(row_index, 0, QTableWidgetItem(data))
        col_index = 1
        for funcionario in estatisticas:
            for fase in estatisticas[funcionario]['fases']:
                # Obter o total de imagens para a data e fase
                total_imagens = estatisticas[funcionario]['datas'].get(data, {}).get(fase, 0)
                tabela.setItem(row_index, col_index, QTableWidgetItem(str(total_imagens)))
                col_index += 1

    tabela.resizeColumnsToContents()  # Ajusta as colunas ao conteúdo

    return tabela