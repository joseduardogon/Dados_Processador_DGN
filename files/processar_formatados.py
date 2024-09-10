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

    # Calcula os pontos do funcionário para a atividade atual
    pontos_atuais = funcionario.calcular_pontos()

    if funcionario.nome not in pontuacoes:
        pontuacoes[funcionario.nome] = pontos_atuais  # Cria uma nova entrada se o funcionário não existir
    else:
        # Acumula os pontos de cada atividade individualmente
        for chave, valor in pontos_atuais.items():
            pontuacoes[funcionario.nome][chave] += valor 

    return pontuacoes

def calcular_pontos_arquivo_formatado(caminho_arquivo):
    """Calcula os pontos de um arquivo já formatado e salva em um novo arquivo JSON."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        pontuacoes = {}
        info_funcionario_atual = {}

        for linha in linhas[1:]:  # Pula a primeira linha (cabeçalho)
            linha = linha.strip()

            if linha.startswith("Funcionario:"):
                # Salva o nome do funcionário atual
                nome_funcionario_atual = linha.split(": ")[1]

                # Se já houver dados do funcionário, processe-o
                if info_funcionario_atual:  
                    pontuacoes = processar_funcionario(info_funcionario_atual, pontuacoes)

                # Reinicia o dicionário para o próximo funcionário
                info_funcionario_atual = {"nome": nome_funcionario_atual}  
            elif ": " in linha:
                chave, valor = linha.split(": ")
                info_funcionario_atual[chave] = valor

        # Processa o último funcionário do arquivo
        if info_funcionario_atual:
            pontuacoes = processar_funcionario(info_funcionario_atual, pontuacoes)

        print(f"Pontuações calculadas: {pontuacoes}")

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