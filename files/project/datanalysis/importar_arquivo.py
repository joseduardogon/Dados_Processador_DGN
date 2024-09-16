import openpyxl
import csv
import os

def ler_excel_para_dicionarios(caminho_arquivo):
    """Lê um arquivo Excel e retorna uma lista de dicionários."""

    # Validação de extensão de arquivo
    if not caminho_arquivo.lower().endswith(('.xlsx', '.txt')):
        raise ValueError("Formato de arquivo inválido. Por favor, selecione um arquivo .xlsx ou .txt.")

    if caminho_arquivo.lower().endswith('.xlsx'):
        # Lógica para arquivos Excel
        workbook = openpyxl.load_workbook(caminho_arquivo)
        sheet = workbook.active
        dados = []
        cabecalhos = [coluna.value for coluna in sheet[1]]
        for linha in sheet.iter_rows(min_row=2, values_only=True):
            dicionario_linha = {}

            # Preenche o dicionário com as colunas e os valores
            for i, valor in enumerate(linha):
                # Substitui caracteres especiais
                if isinstance(valor, str):  # Verifica se é uma string
                    valor = valor.replace('ç', 'c').replace('ã', 'a').replace('õ', 'o').replace('á', 'a')
                    valor = valor.replace('á', 'a')
                    # ... Adicione outros caracteres especiais aqui
                dicionario_linha[cabecalhos[i]] = valor

            dados.append(dicionario_linha)
        return dados

    elif caminho_arquivo.lower().endswith('.txt'):
        # Lógica para arquivos TXT
        dados = []
        with open(caminho_arquivo, 'r', encoding='latin-1') as arquivo:
            leitor = csv.reader(arquivo, delimiter=';')
            cabecalhos = next(leitor)
            for linha in leitor:
                dicionario_linha = dict(zip(cabecalhos, linha))
                # Substitui caracteres especiais
                for chave, valor in dicionario_linha.items():
                    if isinstance(valor, str):
                        valor = valor.replace('ç', 'c').replace('ã', 'a').replace('õ', 'o').replace('á', 'a')
                        dicionario_linha[chave] = valor
                dados.append(dicionario_linha)
        return dados

    else:
        raise ValueError("Formato de arquivo inválido. Por favor, selecione um arquivo .xlsx ou .txt.")

def printar_dicionarios(dados):
    """Imprime cada dicionário da lista."""
    for dicionario in dados:
        print(dicionario)


def validar_dicionarios(dados):
    """Valida se todos os dicionários da lista possuem as chaves esperadas."""
    chaves_esperadas = {'Status', 'Usuário', 'Fase', 'Pastas Aprovadas', 'Imagens Aprovadas', 'Documentos Aprovados',
                        'Tempo Aprovado', 'Pastas Rejeitadas', 'Imagens Rejeitadas', 'Documentos Rejeitados',
                        'Tempo Rejeitado', 'Total de Pastas', 'Total de Imagens', 'Total de Documentos',
                        'Total de Tempo'}

    for dicionario in dados:
        if not chaves_esperadas.issubset(set(dicionario.keys())):
            raise ValueError("O arquivo está com as colunas incorretas. Verifique o formato.")

"""caminho_arquivo = "C:\\Users\\josed\\Codes\\Dados_diginotas\\Dados_Processador_DGN\\dados\\estatistica_09092024.txt"
caminho_arquivo = "C:\\Users\\josed\\Codes\\Dados_diginotas\\Dados_Processador_DGN\\dados\\teste_estatisticas_09092024.xlsx"
dados = ler_excel_para_dicionarios(caminho_arquivo)
printar_dicionarios(dados)"""