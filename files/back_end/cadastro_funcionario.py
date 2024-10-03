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
                ultima_producao TEXT,
                salario FLOAT
            )
        """)
        conexao.commit()
        conexao.close()
        print("Tabela 'funcionarios' criada (ou já existe).")

        cadastrar_funcionarios()
        print("Funcionarios Atualizados")

    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'funcionarios': {e}")

import sqlite3

def cadastrar_funcionarios():
    """Lê os nomes de usuários da tabela 'atividades_digitalizacao',
       verifica se já existem na tabela 'funcionarios', e os insere ou atualiza
       os dados de primeira e última produção.
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

        # Para cada nickname, verificar se já existe e inserir ou atualizar
        for nickname in nicknames:
            print(f"Processando funcionário: {nickname}")

            # Verificar se o nickname já existe na tabela 'funcionarios'
            cursor.execute("SELECT 1 FROM funcionarios WHERE nickname = ?", (nickname,))
            funcionario_existe = cursor.fetchone() is not None

            if funcionario_existe:
                print(f"Funcionário '{nickname}' já existe. Atualizando datas de produção...")
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

                # Atualizar as datas de produção
                cursor.execute("""
                    UPDATE funcionarios 
                    SET primeira_producao = ?, ultima_producao = ? 
                    WHERE nickname = ?
                """, (primeira_producao, ultima_producao, nickname))

            else:
                print(f"Funcionário '{nickname}' não existe. Inserindo novo funcionário...")
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

                # Inserir o novo funcionário
                cursor.execute("""
                    INSERT INTO funcionarios (nickname, nome, primeira_producao, ultima_producao, salario) 
                    VALUES (?, ?, ?, ?, ?)
                """, (nickname, "", primeira_producao, ultima_producao, ""))

        conexao.commit()
        conexao.close()
        print("Funcionários cadastrados/atualizados com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao cadastrar funcionários: {e}")