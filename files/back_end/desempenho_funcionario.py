import sqlite3
from collections import defaultdict


def obter_estatisticas_funcionario(unidade):
    """Obtém estatísticas dos funcionários por tarefa,
       considerando o tempo gasto e evitando contagem duplicada de pastas.

    Args:
        unidade (str): Nome da unidade.

    Returns:
        dict: Dicionário com estatísticas por funcionário e tarefa.
    """
    print("----- Iniciando obter_estatisticas_funcionario -----")
    try:
        print("Conectando ao banco de dados...")
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()
        print("Conexão estabelecida.")

        print("Executando consulta SQL...")
        cursor.execute("""
            SELECT 
                usuario, 
                fase,
                tempo_gasto,
                fase_destino,
                SUM(imgs_depois) AS total_imagens,
                SUM(docs_depois) AS total_docs_depois,
                pasta,
                COUNT(DISTINCT STRFTIME('%Y-%m-%d', DATE(termino))) AS num_dias  -- Conta o número de datas distintas
            FROM 
                atividades_digitalizacao
            WHERE 
                unidade = ?
            GROUP BY
                usuario, fase, pasta
            ORDER BY 
                usuario, fase; 
        """, (unidade,))
        print("Consulta SQL executada.")

        estatisticas = defaultdict(lambda: {"medias": 0, "totais": 0})
        pastas_processadas = defaultdict(set)  # Controle de pastas por funcionário e fase

        print("Processando resultados da consulta...")
        for usuario, fase, tempo_gasto, fase_destino, total_imagens, total_docs_depois, pasta, num_dias in cursor.fetchall():
            chave = f"{usuario} - {fase}"
            print(
                f"Processando linha: {usuario}, {fase}, {tempo_gasto}, {total_imagens}, {total_docs_depois}, {pasta}, {num_dias}")

            # --- Condição para somar a linha ---
            if (fase != fase_destino and
                    "Suspenso" not in fase_destino and
                    pasta not in pastas_processadas[chave]):  # Verifica se a pasta já foi processada para essa tarefa

                try:
                    horas, minutos, segundos = map(int, tempo_gasto.split(':'))
                    tempo_gasto_segundos = horas * 3600 + minutos * 60 + segundos
                    print(f"Tempo gasto em segundos: {tempo_gasto_segundos}")

                    if tempo_gasto_segundos > 5 * total_docs_depois:
                        estatisticas[chave]["totais"] += total_imagens
                        pastas_processadas[chave].add(pasta)  # Marca a pasta como processada para a tarefa
                        print(
                            f"Somando: Funcionário: {usuario}, Fase: {fase}, Total: {total_imagens}, Soma: {estatisticas[chave]['totais']}")
                    else:
                        print(
                            f"Ignorando por tempo: Fase: {fase}, Tempo Gasto: {tempo_gasto_segundos} segundos, Docs. Depois: {total_docs_depois}")
                except ValueError:
                    print(f"Ignorando por formato de tempo inválido: {tempo_gasto}")
            # ------------------------------------

        print("Calculando médias...")
        for chave, dados in estatisticas.items():
            print(f"Calculando média para {chave}...")
            if dados["totais"] != 0:
                media = dados["totais"] / num_dias  # Calcula a média correta
                estatisticas[chave]["medias"] = media
            print(f"Média para {chave}: {media}")
        print("Médias calculadas.")

        conexao.close()
        print("Conexão fechada.")
        print("Dicionário de Estatísticas:", estatisticas)
        print("----- Fim de obter_estatisticas_funcionario -----")
        return estatisticas

    except sqlite3.Error as e:
        print(f"Erro ao obter estatísticas do funcionário: {e}")
        print("----- Fim de obter_estatisticas_funcionario -----")
        return {}