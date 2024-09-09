import os
import json
from unidecode import unidecode

from calcular_pontos import Funcionario, PESOS

def processar_funcionario(info_funcionario, pontuacoes):
    """Processa as informações de um funcionário e acumula seus pontos."""
    funcionario = Funcionario(
        info_funcionario["nome"],
        info_funcionario.get("Atividade"),
        int(info_funcionario.get("Imagens Aprovadas", 0)),
        int(info_funcionario.get("Documentos Aprovados", 0)),
        int(info_funcionario.get("Pastas Aprovadas", 0))
    )
    if funcionario.nome in pontuacoes:
        pontuacoes[funcionario.nome]["Total"] += funcionario.calcular_pontos()["Total"]
    else:
        pontuacoes[funcionario.nome] = funcionario.calcular_pontos()
    return pontuacoes

def calcular_pontos_arquivo_formatado(caminho_arquivo):
    """Calcula os pontos de um arquivo já formatado e salva em um novo arquivo JSON."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        print(f"Linhas do arquivo: {linhas}")  # Debug

        pontuacoes = {}
        info_funcionario_atual = {}

        for linha in linhas[1:]:  # Pula a primeira linha (cabeçalho)
            linha = linha.strip()
            print(f"Processando linha: {linha}")  # Debug

            if linha.startswith("Funcionario:"):
                # Processa o funcionário anterior se houver dados
                if info_funcionario_atual: 
                    pontuacoes = processar_funcionario(info_funcionario_atual, pontuacoes)

                # Inicia um novo dicionário para o próximo funcionário
                info_funcionario_atual = {"nome": linha.split(": ")[1]}
            elif ": " in linha:
                chave, valor = linha.split(": ")
                info_funcionario_atual[chave] = valor

        # Processa o último funcionário do arquivo
        if info_funcionario_atual:  
            pontuacoes = processar_funcionario(info_funcionario_atual, pontuacoes)

        print(f"Pontuações calculadas: {pontuacoes}")  # Debug

        # Salva as pontuações em um novo arquivo JSON
        caminho_pontos_arquivo = os.path.join("files", "intern", "pontos_formatados.json")
        with open(caminho_pontos_arquivo, 'w', encoding='utf-8') as f:
            json.dump(pontuacoes, f, ensure_ascii=False, indent=4)

        return pontuacoes

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {caminho_arquivo}")
        return {}
    except Exception as e:
        print(f"Erro ao processar o arquivo formatado: {e}")
        return {}