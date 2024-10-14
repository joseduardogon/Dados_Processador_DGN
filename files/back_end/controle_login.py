import sqlite3
from back_end.db_path import caminho_db
import os

#from analista_dados.files.back_end.interpretador import caminho_arquivo

os.makedirs(os.path.dirname(caminho_db), exist_ok=True)  # Cria o diretório se não existir

def verificar_tabela_login():
    """Verifica se a tabela 'usuarios' existe no banco de dados.
       Se não existir, cria a tabela com usuários padrão.
    """
    print("----- Verificando tabela de login -----")
    try:
        conexao = sqlite3.connect(caminho_db)
        cursor = conexao.cursor()

        query = f"SELECT * FROM {'usuarios'}"
        cursor.execute(query)

        # Obtém todos os registros da consulta
        registros = cursor.fetchall()

        # Se houver registros, itera sobre eles e exibe no terminal
        if registros:
            for registro in registros:
                print(registro)  # Cada registro será uma tupla com os valores das colunas
        else:
            print(f"A tabela {'usuarios'} está vazia ou não existe.")

        print(f'caminho: {os.path.abspath(caminho_db)}')


        # Verifica se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        tabela_existe = bool(cursor.fetchone())

        # Se a tabela não existir, cria a tabela e adiciona os usuários padrão
        if not tabela_existe:
            print("Criando tabela 'usuarios'...")
            cursor.execute("""
                CREATE TABLE usuarios (
                    nome_usuario TEXT PRIMARY KEY,
                    senha TEXT,
                    tipo_usuario TEXT,
                    unidade TEXT
                )
            """)

            print("Inserindo usuários padrão...")
            usuarios_padrao = [
                ("dev", "ard14", "dev", "admin"),
                ("admin", "digidados", "admin", "admin")
            ]
            cursor.executemany("INSERT INTO usuarios VALUES (?, ?, ?, ?)", usuarios_padrao)
            conexao.commit()
            print("Tabela 'usuarios' criada com sucesso!")

        conexao.close()
        print("Tabela 'usuarios' existe:", tabela_existe)
        return tabela_existe

    except sqlite3.Error as e:
        print(f"Erro ao verificar ou criar tabela 'usuarios': {e}")
        return False


def obter_dados_usuario(nome_usuario):
    """Busca os dados do usuário pelo nome de usuário.

    Args:
        nome_usuario (str): Nome de usuário.

    Returns:
        tuple: Uma tupla contendo (senha, tipo_usuario, unidade) ou None se o usuário não for encontrado.
    """
    print(f"----- Buscando dados do usuário: {nome_usuario} -----")
    try:
        conexao = sqlite3.connect(caminho_db)
        cursor = conexao.cursor()
        cursor.execute("SELECT senha, tipo_usuario, unidade FROM usuarios WHERE nome_usuario = ?", (nome_usuario,))
        usuario = cursor.fetchone()
        conexao.close()
        print("Dados do usuário encontrados:", usuario)
        return usuario
    except sqlite3.Error as e:
        print(f"Erro ao buscar dados do usuário: {e}")
        return None
verificar_tabela_login()