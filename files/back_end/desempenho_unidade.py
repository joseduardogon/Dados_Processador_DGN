import sqlite3

def obter_estatisticas_unidade(unidade, data=None):
    """Obtém as estatísticas de imagens por fase e data para a unidade.

    Args:
        unidade (str): Nome da unidade.
        data (str, optional): Data no formato 'aaaa-mm-dd'. Se None, retorna todas as datas.

    Returns:
        dict: Um dicionário com as estatísticas.
    """
    try:
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()

        # Consulta SQL com filtro opcional por data
        if data:
            cursor.execute("""
                SELECT 
                    fase,               
                    SUM(imgs_depois) AS total_imagens
                FROM 
                    atividades_digitalizacao
                WHERE 
                    unidade = ? AND STRFTIME('%Y-%m-%d', DATE(termino)) = ?
                GROUP BY 
                    fase   
                ORDER BY 
                    fase; 
            """, (unidade, data))
        else:
            cursor.execute("""
                SELECT 
                    STRFTIME('%Y-%m-%d', DATE(termino)) AS data,
                    fase,               
                    SUM(imgs_depois) AS total_imagens
                FROM 
                    atividades_digitalizacao
                WHERE 
                    unidade = ?
                GROUP BY 
                    data, fase   
                ORDER BY 
                    fase, data; 
            """, (unidade,))

        estatisticas = {}
        if data:  # Organiza as estatísticas para uma data específica
            for fase, total_imagens in cursor.fetchall():
                estatisticas[fase] = total_imagens
        else:  # Organiza as estatísticas por data
            for data, fase, total_imagens in cursor.fetchall():
                if data not in estatisticas:
                    estatisticas[data] = {}
                estatisticas[data][fase] = total_imagens

        conexao.close()
        print("Dicionário de Estatísticas:")
        print(estatisticas)
        return estatisticas

    except sqlite3.Error as e:
        print(f"Erro ao obter estatísticas da unidade: {e}")
        return {}

def obter_anos_disponiveis(unidade):
    """Obtém os anos disponíveis no banco de dados para a unidade."""
    try:
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT DISTINCT STRFTIME('%Y', DATE(termino)) AS ano_disponivel 
            FROM atividades_digitalizacao
            WHERE unidade = ?
            ORDER BY ano_disponivel
        """, (unidade,))
        anos = [row[0] for row in cursor.fetchall()]
        conexao.close()
        print("Anos disponíveis:", anos)
        return anos
    except sqlite3.Error as e:
        print(f"Erro ao obter anos disponíveis: {e}")
        return []

def obter_meses_disponiveis(unidade, ano):
    """Obtém os meses disponíveis no banco de dados para a unidade e ano."""
    try:
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT DISTINCT STRFTIME('%m', DATE(termino)) AS mes_disponivel
            FROM atividades_digitalizacao
            WHERE unidade = ? AND STRFTIME('%Y', DATE(termino)) = ?
            ORDER BY mes_disponivel
        """, (unidade, ano))
        meses = [row[0] for row in cursor.fetchall()]
        conexao.close()
        print("Meses disponíveis:", meses)
        return meses
    except sqlite3.Error as e:
        print(f"Erro ao obter meses disponíveis: {e}")
        return []

def obter_dias_disponiveis(unidade, ano, mes):
    """Obtém os dias disponíveis no banco de dados para a unidade, ano e mês."""
    try:
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT DISTINCT STRFTIME('%d', DATE(termino)) AS dia_disponivel
            FROM atividades_digitalizacao
            WHERE unidade = ? AND STRFTIME('%Y', DATE(termino)) = ? AND STRFTIME('%m', DATE(termino)) = ?
            ORDER BY dia_disponivel
        """, (unidade, ano, mes))
        dias = [row[0] for row in cursor.fetchall()]
        conexao.close()
        print("Dias disponíveis:", dias)
        return dias
    except sqlite3.Error as e:
        print(f"Erro ao obter dias disponíveis: {e}")
        return []