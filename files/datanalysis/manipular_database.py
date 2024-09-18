import openpyxl
import csv
import os
from datetime import date

def criar_arquivos_usuario(dados, pasta_base='data'):
    """Cria um arquivo CSV para cada usuário no diretório data."""

    data_hoje = date.today().strftime('%Y-%m-%d')  # Formato 'AAAA-MM-DD'
    for dicionario in dados:
        nome_usuario = dicionario['Usuário']
        nome_arquivo = f"{nome_usuario}.csv"
        caminho_arquivo = os.path.join(pasta_base, nome_arquivo)

        with open(caminho_arquivo, 'w', newline='', encoding='latin-1') as arquivo:
            escritor = csv.writer(arquivo)

            # Escreve o cabeçalho (legenda + data de hoje)
            cabecalho = ['Legenda'] + [data_hoje]
            escritor.writerow(cabecalho)

            # Escreve os dados (linha por linha, cada linha é um dicionário)
            for chave in dicionario:
                # Ignora as chaves "Status" e "Usuário"
                if chave != 'Status' and chave != 'Usuário':
                    escritor.writerow([chave] + [dicionario[chave]])