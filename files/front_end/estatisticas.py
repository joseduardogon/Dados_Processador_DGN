from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

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
    """)

    # Adiciona os dados à tabela
    row_index = 0
    for data, fases in dados.items():
        for fase, total_imagens in fases.items():
            tabela.insertRow(row_index)
            tabela.setItem(row_index, 0, QTableWidgetItem(str(data)))
            tabela.setItem(row_index, 1, QTableWidgetItem(fase))
            tabela.setItem(row_index, 2, QTableWidgetItem(str(total_imagens)))
            row_index += 1

    tabela.resizeColumnsToContents()  # Ajusta as colunas ao conteúdo

    return tabela