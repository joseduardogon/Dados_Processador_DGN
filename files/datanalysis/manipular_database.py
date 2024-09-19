import sqlite3
from datetime import date, time

def conectar_banco():
    """Conecta-se ao banco de dados SQLite."""
    try:
        con = sqlite3.connect('meu_banco.db')
        cursor = con.cursor()
        return con, cursor
    except Exception as e:
        print(f"Erro ao conectar ao SQLite: {e}")
        return None, None

def inserir_dados_no_banco(dados):
    """Insere os dados no banco de dados."""

    con, cursor = conectar_banco()

    if con and cursor:
        for dicionario in dados:
            data_atual = date.today().strftime("%Y-%m-%d")

            # Conversão dos tipos de dados:
            for chave in ('Tempo Aprovado', 'Tempo Rejeitado', 'Total de Tempo'):
                if isinstance(dicionario.get(chave), time):
                    dicionario[chave] = dicionario[chave].strftime('%H:%M:%S')  # Formato hora

            nome_usuario = dicionario['Usuário'].replace(" ", "")  # Remover espaços
            nome_tabela = nome_usuario

            # Verificar se a tabela existe:
            cursor.execute(f"PRAGMA table_info({nome_tabela})")
            resultado = cursor.fetchall()
            tabela_existe = bool(resultado)

            # Cria a tabela caso não exista:
            if not tabela_existe:
                criar_tabela_sql = f"""
                    CREATE TABLE {nome_tabela} (
                        Data DATE PRIMARY KEY, 
                        Status TEXT,
                        Fase TEXT,
                        Pastas_Aprovadas INTEGER, 
                        Imagens_Aprovadas INTEGER, 
                        Documentos_Aprovados INTEGER,
                        Tempo_Aprovado TEXT,
                        Pastas_Rejeitadas INTEGER,
                        Imagens_Rejeitadas INTEGER, 
                        Documentos_Rejeitados INTEGER, 
                        Tempo_Rejeitado TEXT, 
                        Total_de_Pastas INTEGER, 
                        Total_de_Imagens INTEGER, 
                        Total_de_Documentos INTEGER,
                        Tempo_Total TEXT 
                    )
                """
                cursor.execute(criar_tabela_sql)
                print(f"Tabela '{nome_tabela}' criada com sucesso.")
                con.commit()

            # Insere os dados (ou atualiza se a data já existir):
            colunas = ', '.join(dicionario.keys())
            placeholders = ', '.join(['?'] * len(dicionario))
            valores = list(dicionario.values())

            sql = f"""
                INSERT OR REPLACE INTO {nome_tabela} (Data, {colunas}) 
                VALUES (?, {placeholders})
            """

            try:
                cursor.execute(sql, [data_atual] + valores)
                con.commit()
                print(f"Dados inseridos na tabela '{nome_tabela}'.")
            except sqlite3.Error as e:
                print(f"Erro ao inserir dados na tabela '{nome_tabela}': {e}")

        con.close()
    else:
        print("Erro ao conectar ao banco de dados.")

def ler_dados_do_banco(nome_tabela):
    """Lê os dados da tabela especificada no SQLite."""

    try:
        con, cursor = conectar_banco()
        if con and cursor:
            # Usando parâmetros para evitar SQL injection
            cursor.execute(f"SELECT * FROM {nome_tabela}")
            dados = cursor.fetchall()
            return dados
        else:
            print("Erro ao conectar ao banco de dados.")
            return []
    except sqlite3.Error as e:
        print(f"Erro ao ler dados da tabela '{nome_tabela}': {e}")
        return []