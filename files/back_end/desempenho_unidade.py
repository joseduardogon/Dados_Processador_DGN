import sqlite3

def obter_estatisticas_unidade(unidade, data=None):
    """Obtém as estatísticas de imagens por fase para a unidade e data especificadas,
       aplicando as regras para evitar contagens duplicadas e considerando o tempo gasto.

    Args:
        unidade (str): Nome da unidade.
        data (str, optional): Data no formato 'aaaa-mm-dd'. Se None, retorna todas as datas.

    Returns:
        dict: Um dicionário com as estatísticas.
    """
    print("----- Iniciando obter_estatisticas_unidade -----")
    try:
        print("Conectando ao banco de dados...")
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()
        print("Conexão estabelecida.")

        print("Executando consulta SQL...")
        if data:
            if unidade == "admin":  # Se a unidade for "admin", busca todas as unidades
                cursor.execute("""
                    SELECT 
                        fase,
                        fase_destino,
                        pasta,
                        tempo_gasto,
                        SUM(imgs_depois) AS total_imagens,
                        SUM(docs_depois) AS total_docs_depois
                    FROM 
                        atividades_digitalizacao
                    WHERE 
                        STRFTIME('%Y-%m-%d', DATE(termino)) = ?
                    GROUP BY 
                        fase, fase_destino, pasta
                    ORDER BY 
                        fase; 
                """, (data,))
            else:
                cursor.execute("""
                    SELECT 
                        fase,
                        fase_destino,
                        pasta,
                        tempo_gasto,
                        SUM(imgs_depois) AS total_imagens,
                        SUM(docs_depois) AS total_docs_depois
                    FROM 
                        atividades_digitalizacao
                    WHERE 
                        unidade = ? AND STRFTIME('%Y-%m-%d', DATE(termino)) = ?
                    GROUP BY 
                        fase, fase_destino, pasta
                    ORDER BY 
                        fase; 
                """, (unidade, data))
        else:
            if unidade == "admin":
                cursor.execute("""
                    SELECT 
                        STRFTIME('%Y-%m-%d', DATE(termino)) AS data,
                        fase,
                        fase_destino,
                        pasta,
                        tempo_gasto,
                        SUM(imgs_depois) AS total_imagens,
                        SUM(docs_depois) AS total_docs_depois
                    FROM 
                        atividades_digitalizacao
                    GROUP BY 
                        data, fase, fase_destino, pasta
                    ORDER BY 
                        fase, data;
                    """)
            else:
                cursor.execute("""
                    SELECT 
                        STRFTIME('%Y-%m-%d', DATE(termino)) AS data,
                        fase,
                        fase_destino,
                        pasta,
                        tempo_gasto,
                        SUM(imgs_depois) AS total_imagens,
                        SUM(docs_depois) AS total_docs_depois
                    FROM 
                        atividades_digitalizacao
                    WHERE 
                        unidade = ?
                    GROUP BY 
                        data, fase, fase_destino, pasta
                    ORDER BY 
                        fase, data; 
                """, (unidade,))
        print("Consulta executada.")

        estatisticas = {}
        fases_processadas = set()

        print("Obtendo estatísticas...")
        for linha in cursor.fetchall():
            if data:  # Organiza as estatísticas para uma data específica
                fase = linha[0]
                fase_destino = linha[1]
                pasta = linha[2]
                tempo_gasto = linha[3]
                total_imagens = linha[4]
                total_docs_depois = linha[5]
                combinacao_fase_pasta = (fase, pasta)
                print(
                    f"Dados: Fase: {fase}, Fase Destino: {fase_destino}, Pasta: {pasta}, Tempo Gasto: {tempo_gasto}, Total Imagens: {total_imagens}, Total Docs Depois: {total_docs_depois}")

                # --- Condições para somar a linha ---
                if (combinacao_fase_pasta not in fases_processadas and
                        fase != fase_destino and
                        "Suspenso" not in fase_destino):
                    # --- Nova Condição: Tempo Gasto ---
                    try:
                        horas, minutos, segundos = map(int, tempo_gasto.split(':'))
                        tempo_gasto_segundos = horas * 3600 + minutos * 60 + segundos

                        # ---  Condição específica para as fases ---
                        if (
                                fase == "Verificação" or fase == "CLassificação" or fase == "Digitalização (Scanner)" or fase
                                == "Controle de Qualidade"):
                            if tempo_gasto_segundos > 5 * total_docs_depois:
                                if fase not in estatisticas:
                                    estatisticas[fase] = 0
                                estatisticas[fase] += total_imagens
                                fases_processadas.add(combinacao_fase_pasta)
                                print(
                                    f"Somando: Fase: {fase}, Total: {total_imagens}, Soma: {estatisticas[fase]}")
                            else:
                                print(
                                    f"Ignorando por tempo: Fase: {fase}, Tempo Gasto: {tempo_gasto_segundos} segundos, Docs. Depois: {total_docs_depois}")
                        elif tempo_gasto_segundos != 0:  # --- As demais fases sempre serão somadas
                            if fase not in estatisticas:
                                estatisticas[fase] = 0
                            estatisticas[fase] += total_imagens
                            fases_processadas.add(combinacao_fase_pasta)
                            print(
                                f"Somando: Fase: {fase}, Total: {total_imagens}, Soma: {estatisticas[fase]}")
                    except ValueError:
                        print(f"Ignorando por formato de tempo inválido: {tempo_gasto}")
                    # ------------------------------------

                else:
                    print(f"Ignorando: Fase: {fase}, Fase Destino: {fase_destino}, Pasta: {pasta}")

            else:  # Organiza as estatísticas por data
                print("Obtendo estatísticas para todas as datas.")
                data = linha[0]
                fase = linha[1]
                fase_destino = linha[2]
                pasta = linha[3]
                tempo_gasto = linha[4]
                total_imagens = linha[5]
                total_docs_depois = linha[6]
                combinacao_fase_pasta = (fase, pasta)
                print(
                    f"Dados: Fase: {fase}, Fase Destino: {fase_destino}, Pasta: {pasta}, Tempo Gasto: {tempo_gasto}, Total Imagens: {total_imagens}, Total Docs Depois: {total_docs_depois}")

                if data not in estatisticas:
                    estatisticas[data] = {}
                    self.tabela.fases_processadas_por_data[data] = set()
                # --- Condições para somar a linha ---
                if (combinacao_fase_pasta not in fases_processadas_por_data[data] and
                        fase != fase_destino and
                        "Suspenso" not in fase_destino):

                    # --- Nova Condição: Tempo Gasto ---
                    try:
                        horas, minutos, segundos = map(int, tempo_gasto.split(':'))
                        tempo_gasto_segundos = horas * 3600 + minutos * 60 + segundos

                        # ---  Condição específica para as fases ---
                        if (fase == "Verificação" or fase == "CLassificação" or fase == "Digitalização (Scanner)" or fase
                                == "Controle de Qualidade"):
                            if tempo_gasto_segundos > 5 * total_docs_depois:
                                if fase not in estatisticas[data]:
                                    estatisticas[data][fase] = 0
                                estatisticas[data][fase] += total_imagens
                                fases_processadas_por_data[data].add(combinacao_fase_pasta)
                                print(
                                    f"Somando: Fase: {fase}, Total: {total_imagens}, Soma: {estatisticas[data][fase]}")
                            else:
                                print(
                                    f"Ignorando por tempo: Fase: {fase}, Tempo Gasto: {tempo_gasto_segundos} segundos, Docs. Depois: {total_docs_depois}")
                        else:  # --- As demais fases sempre serão somadas
                            if fase not in estatisticas[data]:
                                estatisticas[data][fase] = 0
                            estatisticas[data][fase] += total_imagens
                            fases_processadas_por_data[data].add(combinacao_fase_pasta)
                            print(
                                f"Somando: Fase: {fase}, Total: {total_imagens}, Soma: {estatisticas[data][fase]}")
                    except ValueError:
                        print(f"Ignorando por formato de tempo inválido: {tempo_gasto}")
                    # ------------------------------------

                else:
                    print(f"Ignorando: Fase: {fase}, Fase Destino: {fase_destino}, Pasta: {pasta}")

        conexao.close()
        print("Conexão fechada.")
        print("Dicionário de Estatísticas:", estatisticas)
        print("----- Fim de obter_estatisticas_unidade -----")
        return estatisticas

    except sqlite3.Error as e:
        print(f"Erro ao obter estatísticas da unidade: {e}")
        print("----- Fim de obter_estatisticas_unidade -----")
        return {}

def obter_meses_anos_disponiveis(unidade):
    """Obtém os meses e anos disponíveis no banco de dados para a unidade."""
    print("----- Iniciando obter_meses_anos_disponiveis -----")
    try:
        print("Conectando ao banco de dados...")
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()
        print("Conexão estabelecida.")

        print("Executando consulta SQL (Meses/Anos)...")

        if unidade == 'admin':
            cursor.execute("""
                            SELECT DISTINCT STRFTIME('%m/%Y', DATE(termino)) AS mes_ano_disponivel 
                            FROM atividades_digitalizacao
                            ORDER BY mes_ano_disponivel
                        """)
        else:
            cursor.execute("""
                SELECT DISTINCT STRFTIME('%m/%Y', DATE(termino)) AS mes_ano_disponivel 
                FROM atividades_digitalizacao
                WHERE unidade = ?
                ORDER BY mes_ano_disponivel
            """, (unidade,))
        print("Consulta SQL (Meses/Anos) executada.")

        print("Obtendo meses/anos...")
        meses_anos = [row[0] for row in cursor.fetchall()]
        print("Meses/anos obtidos:", meses_anos)  # Print para verificar a lista de meses/anos

        conexao.close()
        print("Conexão fechada.")
        print("----- Fim de obter_meses_anos_disponiveis -----")
        return meses_anos

    except sqlite3.Error as e:
        print(f"Erro ao obter meses/anos disponíveis: {e}")
        print("----- Fim de obter_meses_anos_disponiveis -----")
        return []