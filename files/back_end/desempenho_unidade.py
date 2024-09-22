import sqlite3
import datetime


def converter_para_data(data_str):
    """Converte uma string de data para um objeto datetime."""
    print(f"--- Convertendo data: {data_str} ---")
    try:
        data_datetime = datetime.datetime.strptime(data_str, "%m/%d/%Y %H:%M:%S")
        print(f"Data convertida: {data_datetime}")

        # Retorna a data formatada como string
        return data_datetime.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Erro na conversão de data: {e}")
        return None


def obter_estatisticas_unidade(unidade):
    """Obtém as estatísticas de imagens por fase e data para a unidade,
    com as seguintes exceções:
    - NÃO soma imagens de linhas com a mesma fase e pasta NA MESMA DATA.
    - NÃO soma linhas onde fase e fase_destino são iguais.
    - NÃO soma linhas onde fase_destino contém a palavra "Suspenso".

    Args:
        unidade (str): Nome da unidade.

    Returns:
        dict: Um dicionário com as estatísticas.
    """
    try:
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()
        conexao.create_function('TO_DATE', 1, converter_para_data)

        cursor.execute("""
            SELECT 
                STRFTIME('%Y-%m-%d', TO_DATE(termino)) AS data, 
                fase,
                fase_destino,  -- Adicionada a coluna fase_destino
                pasta,                
                SUM(imgs_depois) AS total_imagens
            FROM 
                atividades_digitalizacao
            WHERE 
                unidade = ?
            GROUP BY 
                data, fase, pasta
            ORDER BY 
                fase, pasta, data;
        """, (unidade,))

        estatisticas = {}
        fases_processadas_por_data = {}

        for data, fase, fase_destino, pasta, total_imagens in cursor.fetchall():
            if data not in estatisticas:
                estatisticas[data] = {}
                fases_processadas_por_data[data] = set()

            combinacao_fase_pasta = (fase, pasta)

            # --- Condições para somar a linha ---
            if (combinacao_fase_pasta not in fases_processadas_por_data[data] and
                fase != fase_destino and
                "Suspenso" not in fase_destino and
                (fase_destino != "" or fase == "Digitalização (Scanner)")):

                if fase not in estatisticas[data]:
                    estatisticas[data][fase] = 0
                estatisticas[data][fase] += total_imagens
                print(f"Somando: Fase: {fase}, Fase Destino: {fase_destino}, Pasta: {pasta}, Total: {total_imagens}, Soma: {estatisticas[data][fase]}")

                fases_processadas_por_data[data].add(combinacao_fase_pasta)
            else:
                print(f"Ignorando: Fase: {fase}, Fase Destino: {fase_destino}, Pasta: {pasta}")
            # ------------------------------------

        conexao.close()
        print("Dicionário de Estatísticas:")
        print(estatisticas)
        return estatisticas

    except sqlite3.Error as e:
        print(f"Erro ao obter estatísticas da unidade: {e}")
        return {}