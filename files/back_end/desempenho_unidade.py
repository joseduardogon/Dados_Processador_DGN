import sqlite3

def obter_estatisticas_unidade(unidade, data):
    """Obtém as estatísticas de imagens por fase para a unidade e data especificadas.

    Args:
        unidade (str): Nome da unidade.
        data (str): Data no formato 'aaaa-mm-dd'.

    Returns:
        dict: Um dicionário com as estatísticas da unidade para a data,
              ou um dicionário vazio se não houver dados para a data.
    """
    print("----- Iniciando obter_estatisticas_unidade -----")
    try:
        print("Conectando ao banco de dados...")
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()
        print("Conexão estabelecida.")

        print("Executando consulta SQL...")
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
        print("Consulta executada.")

        estatisticas = {}
        print("Obtendo estatísticas...")
        for fase, total_imagens in cursor.fetchall():
            estatisticas[fase] = total_imagens
        print("Estatísticas obtidas.")

        conexao.close()
        print("Conexão fechada.")
        print("Dicionário de Estatísticas:", estatisticas)
        print("----- Fim de obter_estatisticas_unidade -----")
        return estatisticas

    except sqlite3.Error as e:
        print(f"Erro ao obter estatísticas da unidade: {e}")
        print("----- Fim de obter_estatisticas_unidade -----")
        return {}

import sqlite3

# ... (outras funções - sem alterações)

def obter_meses_anos_disponiveis(unidade):
    """Obtém os meses e anos disponíveis no banco de dados para a unidade."""
    print("----- Iniciando obter_meses_anos_disponiveis -----")
    try:
        print("Conectando ao banco de dados...")
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()
        print("Conexão estabelecida.")

        print("Executando consulta SQL (Meses/Anos)...")
        cursor.execute("""
            SELECT DISTINCT STRFTIME('%m/%Y', DATE(termino)) AS mes_ano_disponivel 
            FROM atividades_digitalizacao
            WHERE unidade = ?
            ORDER BY mes_ano_disponivel
        """, (unidade,))
        print("Consulta SQL (Meses/Anos) executada.")

        print("Obtendo meses/anos...")
        meses_anos = [row[0] for row in cursor.fetchall()]
        print("Meses/anos obtidos:", meses_anos) # Print para verificar a lista de meses/anos

        conexao.close()
        print("Conexão fechada.")
        print("----- Fim de obter_meses_anos_disponiveis -----")
        return meses_anos

    except sqlite3.Error as e:
        print(f"Erro ao obter meses/anos disponíveis: {e}")
        print("----- Fim de obter_meses_anos_disponiveis -----")
        return []