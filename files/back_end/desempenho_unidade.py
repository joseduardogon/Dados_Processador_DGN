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