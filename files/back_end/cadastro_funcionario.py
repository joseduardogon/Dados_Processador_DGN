import sqlite3

def criar_tabela_funcionarios():
    """Cria a tabela 'funcionarios' no banco de dados, se ela não existir."""
    print("----- Iniciando criar_tabela_funcionarios -----")
    try:
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios (
                nickname TEXT PRIMARY KEY,
                nome TEXT,
                primeira_producao TEXT,
                ultima_producao TEXT
            )
        """)
        conexao.commit()
        conexao.close()
        print("Tabela 'funcionarios' criada (ou já existe).")

    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'funcionarios': {e}")

def cadastrar_funcionarios():
    """Lê os nomes de usuários da tabela 'atividades_digitalizacao' e
       os insere na tabela 'funcionarios', calculando a primeira e última produção.
    """
    print("----- Iniciando cadastrar_funcionarios -----")
    try:
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()

        # Obter os nicknames dos funcionários da tabela atividades_digitalizacao
        cursor.execute("""
            SELECT DISTINCT usuario 
            FROM atividades_digitalizacao
        """)
        nicknames = [row[0] for row in cursor.fetchall()]

        # Para cada nickname, obter a primeira e última produção
        for nickname in nicknames:
            print(f"Processando funcionário: {nickname}")

            # Obter a primeira produção (data mais antiga)
            cursor.execute("""
                SELECT MIN(DATE(termino)) 
                FROM atividades_digitalizacao 
                WHERE usuario = ?
            """, (nickname,))
            primeira_producao = cursor.fetchone()[0]

            # Obter a última produção (data mais recente)
            cursor.execute("""
                SELECT MAX(DATE(termino)) 
                FROM atividades_digitalizacao 
                WHERE usuario = ?
            """, (nickname,))
            ultima_producao = cursor.fetchone()[0]

            # Inserir ou atualizar os dados na tabela 'funcionarios'
            cursor.execute("""
                INSERT OR REPLACE INTO funcionarios (nickname, nome, primeira_producao, ultima_producao) 
                VALUES (?, ?, ?, ?)
            """, (nickname, "", primeira_producao, ultima_producao)) # nome = ""

        conexao.commit()
        conexao.close()
        print("Funcionários cadastrados com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao cadastrar funcionários: {e}")

# --- Chamar as funções para criar a tabela e cadastrar os funcionários ---
criar_tabela_funcionarios()
cadastrar_funcionarios()