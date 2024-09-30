import sqlite3
from collections import defaultdict

def obter_estatisticas_funcionario(unidade):
    """Obtém estatísticas dos funcionários por tarefa,
       considerando o tempo gasto, evitando contagem duplicada de pastas
       e ignorando usuários específicos.

    Args:
        unidade (str): Nome da unidade.

    Returns:
        dict: Dicionário com estatísticas por funcionário e tarefa.
    """
    # --- Lista de Usuários a Serem Ignorados ---
    usuarios_ignorados = ["Admin", "Michael", "Kayo", "usu_robo_1", "usu_robo_2", "usu_robo_3", "usu_robo_4", "usu_robo_5", "usu_robo_6", "usu_robo_7", "usu_robo_8", "usu_robo_9", "usu_robo_10", "usu_robo_11"]  # Adicione os nomes dos usuários aqui
    # --------------------------------------------
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
                STRFTIME('%Y-%m-%d', DATE(termino)) AS data
            FROM 
                atividades_digitalizacao
            WHERE 
                unidade = ?
            GROUP BY
                usuario, fase, data, pasta
            ORDER BY 
                usuario, fase, data DESC; 
        """, (unidade,))
        print("Consulta SQL executada.")

        estatisticas = defaultdict(lambda: {"fases": set(), "medias": {}, "dias": defaultdict(lambda: {})})
        pastas_processadas = defaultdict(lambda: defaultdict(set))

        print("Processando resultados da consulta...")
        for usuario, fase, tempo_gasto, fase_destino, total_imagens, total_docs_depois, pasta, data in cursor.fetchall():
            # --- Ignorar Usuários ---
            if usuario in usuarios_ignorados:
                print(f"Ignorando usuário: {usuario}")
                continue  # Pula para a próxima iteração do loop
            # ------------------------

            chave = usuario
            print(
                f"Dados: Usuário: {usuario}, Fase: {fase}, Data: {data}, Tempo Gasto: {tempo_gasto}, Total Imagens: {total_imagens}, Total Docs Depois: {total_docs_depois}, Pasta: {pasta}")

            if fase not in estatisticas[chave]["fases"]:
                estatisticas[chave]["fases"].add(fase)
                estatisticas[chave]["medias"][fase] = 0  # Inicializa a média como 0

            # --- Condição para somar a linha ---
            if (fase != fase_destino and # Condição reescrita
                    "Suspenso" not in fase_destino and
                    pasta not in pastas_processadas[chave][fase]):  # Verifica se a pasta já foi processada para essa tarefa
                try:
                    horas, minutos, segundos = map(int, tempo_gasto.split(':'))
                    tempo_gasto_segundos = horas * 3600 + minutos * 60 + segundos
                    print(f"Tempo gasto em segundos: {tempo_gasto_segundos}")

                    if tempo_gasto_segundos > 5 * total_docs_depois:
                        if fase not in estatisticas[chave]['dias'][data]:
                            estatisticas[chave]['dias'][data][fase] = 0
                        estatisticas[chave]['dias'][data][fase] += total_imagens
                        pastas_processadas[chave][fase].add(pasta)  # Marca a pasta como processada para a tarefa
                        print(
                            f"Somando: Funcionário: {usuario}, Fase: {fase}, Total: {total_imagens}, Soma: {estatisticas[chave]['dias'][data][fase]}")
                    else:
                        print(
                            f"Ignorando por tempo: Fase: {fase}, Tempo Gasto: {tempo_gasto_segundos} segundos, Docs. Depois: {total_docs_depois}")
                except ValueError:
                    print(f"Ignorando por formato de tempo inválido: {tempo_gasto}")
            # ------------------------------------
        print("Calculando médias...")
        for chave, dados in estatisticas.items():
            for fase in dados['fases']:
                print(f"Calculando média para {chave} na fase {fase}...")
                valores = [total for data, totais in dados["dias"].items() for tarefa, total in totais.items() if
                           tarefa == fase]
                media = 0  # Inicializa a variável media com 0
                if valores:
                    media = sum(valores) / len(valores)
                    estatisticas[chave]["medias"][fase] = media
                print(f"Média para {chave} - {fase}: {media}")
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