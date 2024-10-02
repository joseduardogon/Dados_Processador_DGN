import sqlite3  # Importa a biblioteca `sqlite3` para interagir com o banco de dados SQLite.

def obter_estatisticas_unidade(unidade, data=None):
    """Obtém as estatísticas de imagens processadas por fase para uma unidade e data específicas,
    aplicando regras para evitar contagem duplicada e considerando o tempo gasto.

    Args:
        unidade (str): Nome da unidade. Se for "admin", busca todas as unidades.
        data (str, optional): Data no formato "aaaa-mm-dd". Se None, retorna estatísticas para todas as datas.

    Returns:
        dict: Um dicionário contendo as estatísticas de imagens por fase.
              As chaves são as fases e os valores são o total de imagens processadas.
    """

    print("----- Iniciando obter_estatisticas_unidade -----")  # Imprime uma mensagem no console.
    try:
        print("Conectando ao banco de dados...")
        conexao = sqlite3.connect("database/banco_producao.db")  # Estabelece conexão com o banco de dados SQLite.
        cursor = conexao.cursor() # Cria um cursor para interagir com o banco de dados.
        print("Conexão estabelecida.")

        print("Executando consulta SQL...")
        # Verifica se uma data específica foi fornecida
        if data:
            # Se a unidade for 'admin', busca dados de todas as unidades para a data especificada
            if unidade == "admin":
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
            else:  # Caso contrário, busca dados apenas da unidade especificada na data
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
        else:  # Se nenhuma data específica for fornecida
            if unidade == "admin": # Se unidade for admin busca para todas as unidades em todas as datas
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
            else:  # Busca dados apenas da unidade especificada para todas as datas
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

        estatisticas = {} # Inicializa um dicionário vazio para armazenar as estatísticas.
        fases_processadas = set() # Inicializa um conjunto vazio para rastrear as combinações de fase e pasta já processadas, evitando contagem duplicada.
        fases_processadas_por_data = {}

        print("Obtendo estatísticas...")
        for linha in cursor.fetchall():  # Itera sobre as linhas retornadas pela consulta SQL.
            if data:  # Processamento para uma data específica
                fase = linha[
                    0]  # Extrai o nome da fase da primeira coluna (índice 0) da linha atual da consulta.
                fase_destino = linha[
                    1]  # Extrai a fase de destino da segunda coluna (índice 1) da linha atual da consulta.
                pasta = linha[2]  # Extrai o nome da pasta da terceira coluna (índice 2) da linha atual da consulta.
                tempo_gasto = linha[
                    3]  # Extrai o tempo gasto da quarta coluna (índice 3) da linha atual da consulta, representando a duração da tarefa.
                total_imagens = linha[
                    4]  # Extrai o total de imagens da quinta coluna (índice 4) da linha atual da consulta.
                total_docs_depois = linha[
                    5]  # Extrai o total de documentos após o processamento da sexta coluna (índice 5) da linha atual da consulta.
                combinacao_fase_pasta = (
                fase, pasta)  # Cria uma tupla contendo a fase e a pasta para identificar uma combinação única de tarefa e local.
                print(
                    f"Dados: Fase: {fase}, Fase Destino: {fase_destino}, Pasta: {pasta}, Tempo Gasto: {tempo_gasto}, Total Imagens: {total_imagens}, Total Docs Depois: {total_docs_depois}")  # Imprime as informações da linha atual.

                # --- Condições para somar a linha ---
                # Verifica se atende as condições para ser somado à estatística
                if (combinacao_fase_pasta not in fases_processadas and
                        fase != fase_destino and
                        "Suspenso" not in fase_destino):
                    # --- Nova Condição: Tempo Gasto ---
                    try:
                        # Divide o tempo gasto em horas, minutos e segundos
                        horas, minutos, segundos = map(int, tempo_gasto.split(':'))
                        # Calcula o tempo total gasto em segundos
                        tempo_gasto_segundos = horas * 3600 + minutos * 60 + segundos

                        # ---  Condição específica para as fases ---
                        # Verifica se a fase atual é uma das que requerem tempo mínimo de processamento
                        if (
                                fase == "Verificação" or fase == "CLassificação" or fase == "Digitalização (Scanner)" or fase
                                == "Controle de Qualidade"):
                            # Verifica se o tempo gasto é maior que 5 segundos multiplicado pelo total de documentos após o processamento
                            if tempo_gasto_segundos > 5 * total_docs_depois:
                                if fase not in estatisticas:
                                    estatisticas[fase] = 0 # Inicia a contagem para a fase se ainda não existir no dicionário `estatisticas`
                                estatisticas[
                                    fase] += total_imagens  # Adiciona o total de imagens ao dicionário `estatisticas` para a fase atual.
                                fases_processadas.add(combinacao_fase_pasta)  # Adiciona a combinação fase-pasta ao conjunto `fases_processadas` para evitar que seja contada novamente.
                                print(
                                    f"Somando: Fase: {fase}, Total: {total_imagens}, Soma: {estatisticas[fase]}")  # Imprime uma mensagem de debug indicando que a linha está sendo somada às estatísticas.
                            else:
                                print(
                                    f"Ignorando por tempo: Fase: {fase}, Tempo Gasto: {tempo_gasto_segundos} segundos, Docs. Depois: {total_docs_depois}") # Imprime uma mensagem indicando que a linha está sendo ignorada porque o tempo gasto é insuficiente.
                        # Para outras fases, soma o total de imagens se o tempo gasto for diferente de zero
                        elif tempo_gasto_segundos != 0:
                            if fase not in estatisticas:
                                estatisticas[fase] = 0
                            estatisticas[fase] += total_imagens
                            fases_processadas.add(combinacao_fase_pasta)
                            print(
                                f"Somando: Fase: {fase}, Total: {total_imagens}, Soma: {estatisticas[fase]}")
                    # Captura exceção caso o formato do tempo seja inválido
                    except ValueError:
                        print(
                            f"Ignorando por formato de tempo inválido: {tempo_gasto}")  # Imprime uma mensagem no console indicando que a linha está sendo ignorada porque o formato do tempo gasto é inválido.
                    # ------------------------------------
                else:
                    print(
                        f"Ignorando: Fase: {fase}, Fase Destino: {fase_destino}, Pasta: {pasta}")  # Imprime uma mensagem no console indicando que a linha está sendo ignorada porque não atende às condições.

            else: # Processamento para todas as datas
                print(
                    "Obtendo estatísticas para todas as datas.")  # Imprime uma mensagem no console, indicando que está processando todas as datas.
                data = linha[0] # Extrai a data da primeira coluna (índice 0).
                fase = linha[1] # Extrai a fase da segunda coluna (índice 1).
                fase_destino = linha[2]  # Extrai a fase de destino da terceira coluna (índice 2).
                pasta = linha[3] # Extrai a pasta da quarta coluna (índice 3).
                tempo_gasto = linha[4] # Extrai o tempo gasto da quinta coluna (índice 4).
                total_imagens = linha[5] # Extrai o total de imagens da sexta coluna (índice 5).
                total_docs_depois = linha[
                    6]  # Extrai o total de documentos depois da sétima coluna (índice 6).
                combinacao_fase_pasta = (fase,
                                        pasta)  # Cria uma tupla com a fase e a pasta da linha atual.
                print(
                    f"Dados: Fase: {fase}, Fase Destino: {fase_destino}, Pasta: {pasta}, Tempo Gasto: {tempo_gasto}, Total Imagens: {total_imagens}, Total Docs Depois: {total_docs_depois}")  # Imprime as informações da linha atual.

                # Se a data ainda não estiver no dicionário de estatísticas, inicializa um novo dicionário para essa data
                if data not in estatisticas:
                    estatisticas[data] = {}
                    fases_processadas_por_data[data] = set()
                # --- Condições para somar a linha ---
                # Verifica as condições para adicionar a linha atual às estatísticas
                if (combinacao_fase_pasta not in fases_processadas_por_data[data] and
                        fase != fase_destino and
                        "Suspenso" not in fase_destino):

                    # --- Nova Condição: Tempo Gasto ---
                    # Tenta converter a string `tempo_gasto` para um valor numérico em segundos
                    try:
                        horas, minutos, segundos = map(int, tempo_gasto.split(':')) # Separa a string `tempo_gasto` em horas, minutos e segundos, convertendo cada parte para um inteiro usando a função `map`.
                        tempo_gasto_segundos = horas * 3600 + minutos * 60 + segundos # Calcula o tempo total gasto em segundos.

                        # ---  Condição específica para as fases ---
                        # Verifica se a fase atual é uma das que requerem tempo mínimo de processamento
                        if (fase == "Verificação" or fase == "CLassificação" or fase == "Digitalização (Scanner)" or fase
                                == "Controle de Qualidade"):
                            if tempo_gasto_segundos > 5 * total_docs_depois: # Verifica se o tempo gasto é maior que 5 segundos multiplicado pelo número de documentos após o processamento (`total_docs_depois`).
                                if fase not in estatisticas[data]:
                                    estatisticas[data][fase] = 0
                                estatisticas[data][
                                    fase] += total_imagens  # Adiciona o `total_imagens` ao dicionário de estatísticas para a fase atual na data correspondente.
                                fases_processadas_por_data[data].add(
                                    combinacao_fase_pasta)  # Adiciona a combinação `fase` e `pasta`  ao conjunto de fases processadas para evitar contagem dupla
                                print(
                                    f"Somando: Fase: {fase}, Total: {total_imagens}, Soma: {estatisticas[data][fase]}")
                            else: # Se o tempo gasto for menor ou igual a 5 segundos pelo número de documentos, imprime uma mensagem no console e ignora a linha.
                                print(
                                    f"Ignorando por tempo: Fase: {fase}, Tempo Gasto: {tempo_gasto_segundos} segundos, Docs. Depois: {total_docs_depois}")
                        else:  # --- As demais fases sempre serão somadas
                            if fase not in estatisticas[data]:
                                estatisticas[data][fase] = 0
                            estatisticas[data][
                                fase] += total_imagens  # Se a fase não atender à condição de tempo, o total de imagens é somado diretamente ao dicionário `estatisticas`.
                            fases_processadas_por_data[data].add(combinacao_fase_pasta) # Adiciona a combinação fase-pasta ao conjunto.
                            print(
                                f"Somando: Fase: {fase}, Total: {total_imagens}, Soma: {estatisticas[data][fase]}")
                    except ValueError: # Captura a exceção `ValueError`, que pode ocorrer se a string `tempo_gasto` não estiver no formato correto ("hh:mm:ss").
                        print(
                            f"Ignorando por formato de tempo inválido: {tempo_gasto}") # Se houver erro na conversão, imprime uma mensagem de erro no console, indicando o formato inválido do tempo.
                    # ------------------------------------
                else:
                    print(
                        f"Ignorando: Fase: {fase}, Fase Destino: {fase_destino}, Pasta: {pasta}")  # Imprime uma mensagem indicando que a linha está sendo ignorada porque não atende a todas as condições.

        conexao.close() # Fecha a conexão com o banco de dados SQLite, liberando os recursos.
        print("Conexão fechada.")  # Imprime uma mensagem de debug.
        print("Dicionário de Estatísticas:", estatisticas)  # Imprime o dicionário de estatísticas, que contém a contagem de imagens por fase e data.
        print("----- Fim de obter_estatisticas_unidade -----")  # Imprime uma mensagem de debug.
        return estatisticas # Retorna o dicionário de estatísticas, que será usado para exibir os dados na interface da aplicação.

    except sqlite3.Error as e:  # Captura uma exceção específica do SQLite, `sqlite3.Error`, caso ocorra algum erro durante a interação com o banco de dados.
        print(
            f"Erro ao obter estatísticas da unidade: {e}")  # Imprime uma mensagem de erro, incluindo a descrição do erro, se ocorrer uma exceção relacionada ao banco de dados.
        print(
            "----- Fim de obter_estatisticas_unidade -----")  # Imprime uma mensagem de debug.
        return {}  # Retorna um dicionário vazio se ocorrer um erro ao obter as estatísticas, evitando erros na aplicação.


def obter_meses_anos_disponiveis(
        unidade):  # Define uma função para obter os meses e anos distintos com base nos dados no banco de dados.
    """Obtém os meses e anos disponíveis no banco de dados para a unidade."""
    print(
        "----- Iniciando obter_meses_anos_disponiveis -----")  # Imprime uma mensagem de debug no console.
    try:
        print("Conectando ao banco de dados...")
        conexao = sqlite3.connect(
            "database/banco_producao.db")  # Estabelece uma conexão com o banco de dados.
        cursor = conexao.cursor() # Cria um cursor para executar comandos no banco de dados.
        print("Conexão estabelecida.") # Imprime no console uma mensagem

        print(
            "Executando consulta SQL (Meses/Anos)...")  # Imprime no console uma mensagem informando o início da execução da consulta SQL para obter os meses e anos.
        # Verifica se a unidade é "admin"
        if unidade == 'admin': # Se unidade igual a admin
            cursor.execute("""
                            SELECT DISTINCT STRFTIME('%m/%Y', DATE(termino)) AS mes_ano_disponivel 
                            FROM atividades_digitalizacao
                            ORDER BY mes_ano_disponivel
                        """)
        else: # Se unidade for diferente de admin
            cursor.execute(""" 
                SELECT DISTINCT STRFTIME('%m/%Y', DATE(termino)) AS mes_ano_disponivel 
                FROM atividades_digitalizacao
                WHERE unidade = ?
                ORDER BY mes_ano_disponivel
            """, (unidade,))
        print("Consulta SQL (Meses/Anos) executada.")

        print("Obtendo meses/anos...")
        meses_anos = [row[0] for row in
                      cursor.fetchall()]  # Obtém todos os resultados da consulta, que são tuplas contendo a string no formato 'MM/AAAA', e cria uma lista `meses_anos` apenas com esses valores.
        print("Meses/anos obtidos:", meses_anos)  # Imprime no console os meses/anos encontrados no banco de dados.

        conexao.close()  # Fecha a conexão com o banco de dados após a consulta.
        print("Conexão fechada.") # Imprime uma mensagem de debug.
        print(
            "----- Fim de obter_meses_anos_disponiveis -----")  # Imprime uma mensagem de debug no console, indicando o fim da função.
        return meses_anos # Retorna a lista `meses_anos` contendo os meses e anos distintos, no formato "MM/AAAA", encontrados no banco de dados para a unidade especificada.

    except sqlite3.Error as e: # Captura um erro específico do SQLite (sqlite3.Error), caso ocorra durante a conexão com o banco ou a execução da consulta SQL.
        print(
            f"Erro ao obter meses/anos disponíveis: {e}")  # Se um erro ocorrer, imprime uma mensagem de erro no console, incluindo a descrição do erro.
        print("----- Fim de obter_meses_anos_disponiveis -----")
        return []  # Retorna uma lista vazia, caso haja erro na função, evitando que a aplicação pare inesperadamente.