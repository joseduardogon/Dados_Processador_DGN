import os
import sqlite3
import openpyxl

def dicionario_xlsx(caminho_arquivo, supervisor, unidade):
    """Processa um arquivo .xlsx e insere os dados no banco de dados."""
    print(f"--- Iniciando processamento de XLSX: {caminho_arquivo} ---")
    try:
        workbook = openpyxl.load_workbook(caminho_arquivo, read_only=True)
        sheet = workbook.active

        print("--- Planilha aberta com sucesso! ---")

        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()
        print("--- Conexão com banco de dados estabelecida! ---")

        # Itera sobre as linhas da planilha a partir da segunda linha (índice 1)
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Cria uma lista com os dados da linha, pulando o campo "Computador" e "Local"
            dados = list(row[:1]) + list(row[2:17]) + list(row[19:]) + [supervisor, unidade]

            print(f"Dados a serem inseridos: {dados}")

            # Executa a consulta SQL para inserir os dados na tabela
            cursor.execute("""
                INSERT INTO atividades_digitalizacao (
                    usuario, ordem, cod_projeto, cod_lote, cod_pasta, projeto, lote, 
                    pasta, fase, fase_destino, imgs_antes, imgs_depois, docs_antes, 
                    docs_depois, inicio, termino, tempo_gasto, supervisor, unidade 
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, dados)
            print("--- Linha inserida com sucesso! ---")

        conexao.commit()
        conexao.close()
        print(f"--- Dados do arquivo '{caminho_arquivo}' inseridos no banco de dados. ---")

    except Exception as e:
        print(f"Erro ao abrir ou processar o arquivo .xlsx: {e}")
    print(f"--- Fim do processamento de XLSX: {caminho_arquivo} ---")

def dicionario_txt(caminho_arquivo, supervisor, unidade):
    """Processa um arquivo .txt e insere os dados no banco de dados."""
    print(f"--- Iniciando processamento de TXT: {caminho_arquivo} ---")
    try:
        conexao = sqlite3.connect("database/banco_producao.db")
        cursor = conexao.cursor()
        print("--- Conexão com banco de dados estabelecida! ---")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS atividades_digitalizacao (
                usuario TEXT,
                ordem INTEGER,
                cod_projeto INTEGER,
                cod_lote INTEGER,
                cod_pasta INTEGER,
                projeto TEXT,
                lote TEXT,
                pasta TEXT,
                fase TEXT,
                fase_destino TEXT,
                imgs_antes INTEGER,
                imgs_depois INTEGER,
                docs_antes INTEGER,
                docs_depois INTEGER,
                inicio TEXT,
                termino TEXT,
                tempo_gasto TEXT,
                supervisor TEXT,
                unidade TEXT
            )
        """)
        print("--- Tabela criada (ou já existente)! ---")

        with open(caminho_arquivo, 'r', encoding='latin-1') as arquivo:
            next(arquivo)  # Pula o cabeçalho
            for linha in arquivo:
                print(f"Processando linha: {linha.strip()}")
                if linha.startswith("Total"):
                    continue

                # Remove o ponto e vírgula extra do final da linha, se existir
                if linha.endswith(";"):
                    linha = linha[:-1]

                dados = linha.strip().split(';')
                del dados[1]  # Remove "Computador"
                del dados[17] # Remove local

                # Ignora o último campo se ele for vazio ou tiver apenas espaços em branco
                if dados[-1].strip() == "":
                    dados = dados[:-1]

                dados.extend([supervisor, unidade])

                print(f"Dados a serem inseridos: {dados}")
                cursor.execute("""
                    INSERT INTO atividades_digitalizacao (
                        usuario, ordem, cod_projeto, cod_lote, cod_pasta, projeto, lote, 
                        pasta, fase, fase_destino, imgs_antes, imgs_depois, docs_antes, 
                        docs_depois, inicio, termino, tempo_gasto, supervisor, unidade 
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, dados)
                print("--- Linha inserida com sucesso! ---")

        conexao.commit()
        conexao.close()
        print(f"--- Dados do arquivo '{caminho_arquivo}' inseridos no banco de dados. ---")

    except sqlite3.Error as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")
    print(f"--- Fim do processamento de TXT: {caminho_arquivo} ---")

def validar_arquivo(caminho_arquivo, supervisor, unidade):
    """Valida e processa o arquivo."""
    print(f"--- Iniciando validação do arquivo: {caminho_arquivo} ---")
    print(f"Supervisor: {supervisor}, Unidade: {unidade}")
    nome_arquivo, extensao = os.path.splitext(caminho_arquivo)
    if extensao.lower() == '.txt':
        # (Validação do cabeçalho para .txt - código já existente)
        print("--- Arquivo TXT válido! Chamando dicionario_txt... ---")
        dicionario_txt(caminho_arquivo, supervisor, unidade)
        return True
    elif extensao.lower() == '.xlsx':
        print("--- Arquivo XLSX válido! Chamando dicionario_xlsx... ---")
        dicionario_xlsx(caminho_arquivo, supervisor, unidade)
        return True
    else:
        print("--- Extensão de arquivo inválida! ---")
        return False