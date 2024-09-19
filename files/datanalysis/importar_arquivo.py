import openpyxl
import csv
import os
from datetime import date, time, datetime

def ler_excel_para_dicionarios(caminho_arquivo):
    """Lê um arquivo Excel e retorna uma lista de dicionários."""

    if not caminho_arquivo.lower().endswith(('.xlsx', '.txt')):
        raise ValueError("Formato de arquivo inválido. Selecione um arquivo .xlsx ou .txt.")

    if caminho_arquivo.lower().endswith('.xlsx'):
        workbook = openpyxl.load_workbook(caminho_arquivo)
        sheet = workbook.active
        dados = []
        cabecalhos = [coluna.value for coluna in sheet[1]]
        for linha in sheet.iter_rows(min_row=2, values_only=True):
            dicionario_linha = {}
            for i, valor in enumerate(linha):
                if isinstance(valor, str):
                    valor = valor.replace('ç', 'c').replace('ã', 'a').replace('õ', 'o').replace('á', 'a')
                elif isinstance(valor, datetime):
                    valor = valor.strftime("%H:%M:%S")
                elif isinstance(valor, time):
                    valor = valor.strftime("%H:%M:%S")
                dicionario_linha[cabecalhos[i]] = valor
            dados.append(dicionario_linha)
        return dados

    elif caminho_arquivo.lower().endswith('.txt'):
        dados = []
        with open(caminho_arquivo, 'r', encoding='latin-1') as arquivo:
            leitor = csv.reader(arquivo, delimiter=';')
            cabecalhos = next(leitor)
            for linha in leitor:
                dicionario_linha = dict(zip(cabecalhos, linha))
                for chave, valor in dicionario_linha.items():
                    if isinstance(valor, str):
                        valor = valor.replace('ç', 'c').replace('ã', 'a').replace('õ', 'o').replace('á', 'a')
                        dicionario_linha[chave] = valor
                dados.append(dicionario_linha)
        return dados

    else:
        raise ValueError("Formato de arquivo inválido. Selecione um arquivo .xlsx ou .txt.")