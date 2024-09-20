import os, openpyxl


def dicionario_xlsx(caminho_arquivo):
    """Processa um arquivo .xlsx.

    Args:
        caminho_arquivo (str): Caminho do arquivo .xlsx
    """
    print(f"Processando arquivo XLSX: {caminho_arquivo}")


def dicionario_txt(caminho_arquivo):
    """Processa um arquivo .txt.

    Args:
        caminho_arquivo (str): Caminho do arquivo .txt
    """
    print(f"Processando arquivo TXT: {caminho_arquivo}")


def validar_arquivo(caminho_arquivo):
    """Verifica a extensão do arquivo e chama a função apropriada.

    Args:
        caminho_arquivo (str): O caminho completo do arquivo.

    Returns:
        bool: True se o arquivo for válido e processado, False caso contrário.
    """
    nome_arquivo, extensao = os.path.splitext(caminho_arquivo)
    if extensao.lower() == '.xlsx':
        try:
            workbook = openpyxl.load_workbook(caminho_arquivo, read_only=True)  # Abre em modo leitura
            sheet = workbook.active  # Pega a planilha ativa

            # Validação do número de colunas
            if sheet.max_column != 19:
                print(
                    f"Erro: Número de colunas inválido no arquivo .xlsx! (Esperado: 19, Encontrado: {sheet.max_column})")
                return False

            # Validação dos nomes das colunas (cabeçalho)
            cabecalho_esperado = ["Usuário", "Computador", "Ordem", "Cod. Projeto", "Cod. Lote", "Cod. Pasta",
                                  "Projeto", "Lote", "Pasta", "Fase", "Fase Destino", "Imgs. Antes",
                                  "Imgs. Depois", "Docs. Antes", "Docs. Depois", "Início", "Término",
                                  "Tempo Gasto", "Local"]

            for i in range(1, sheet.max_column + 1):  # Percorre as colunas do cabeçalho
                if sheet.cell(row=1, column=i).value != cabecalho_esperado[i - 1]:
                    print(f"Erro: Nome da coluna inválido no arquivo .xlsx! (Coluna: {i})")
                    return False

            dicionario_xlsx(caminho_arquivo)
            return True

        except Exception as e:
            print(f"Erro ao abrir ou processar o arquivo .xlsx: {e}")
            return False
    elif extensao.lower() == '.txt':
            # Validação do cabeçalho para arquivos .txt
            cabecalho_esperado = "Usuário;Computador;Ordem;Cod. Projeto;Cod. Lote;Cod. Pasta;Projeto;Lote;Pasta;Fase;Fase Destino;Imgs. Antes;Imgs. Depois;Docs. Antes;Docs. Depois;Início;Término;Tempo Gasto;Local;"
            with open(caminho_arquivo, 'r', encoding='latin-1') as arquivo:
                primeira_linha = arquivo.readline().strip()  # Lê a primeira linha
                if primeira_linha != cabecalho_esperado:
                    print(f"Erro: Cabeçalho do arquivo .txt inválido!")
                    return False

            dicionario_txt(caminho_arquivo)
            return True
    else:
        return False