import openpyxl
import csv
import os
from datetime import date, time, datetime
import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# URI de Conexão do MongoDB (Defina a URI correta do MongoDB Atlas)
URI = "mongodb+srv://pycharm:coding@datanalysis.k1lnl.mongodb.net/?retryWrites=true&w=majority&appName=Datanalysis"


def conectar_banco():
    """Conecta-se ao banco de dados do MongoDB Atlas."""
    try:
        client = MongoClient(URI, server_api=ServerApi('1'))
        db = client['diginotas']
        colecao = db['funcionarios']
        return colecao
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None


def inserir_dados_no_banco(dados, uri=URI):
    """Insere os dados no MongoDB."""
    try:
        colecao = conectar_banco()
        if colecao is not None:
            for dicionario in dados:
                data_atual = date.today().strftime('%Y-%m-%d')

                # Converter os campos de tempo para objetos datetime
                for chave in ('Tempo Aprovado', 'Tempo Rejeitado', 'Total de Tempo'):
                    if 'Tempo Aprovado' in dicionario and isinstance(dicionario[chave], time):
                        #  Converter para datetime.datetime
                        dicionario[chave] = datetime.combine(date.today(), dicionario[chave])

                dicionario['data_insercao'] = data_atual
                result = colecao.insert_one(dicionario)
                print(f"Dados inseridos no banco de dados com ID: {result.inserted_id}")
    except Exception as e:
        print(f"Erro ao inserir os dados no MongoDB: {e}")
        return False


def ler_dados_do_banco(uri=URI):
    """Lê os dados do MongoDB."""
    try:
        colecao = conectar_banco()
        if colecao is not None:
            dados = list(colecao.find())
            return dados
    except Exception as e:
        print(f"Erro ao ler os dados do MongoDB: {e}")
        return []  # Retorna uma lista vazia em caso de erro