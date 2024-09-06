import os
import json

# Constantes para os caminhos dos arquivos
PASTA_DADOS = os.path.join("files", "intern") 
ARQUIVO_HISTORICO = os.path.join(PASTA_DADOS, "historico.json")

# Constante para o tamanho máximo do histórico
MAX_HISTORICO = 5 

def _carregar_historico():
    """Carrega o histórico do arquivo, criando um novo se não existir."""
    try:
        with open(ARQUIVO_HISTORICO, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"nome_supervisor": [], "unidade": []}

def _salvar_historico(historico):
    """Salva o histórico no arquivo."""
    with open(ARQUIVO_HISTORICO, "w") as f:
        json.dump(historico, f, indent=4)

def atualizar_historico(nome_supervisor, unidade):
    """Atualiza o histórico com novos valores, limitando seu tamanho."""
    historico = _carregar_historico()
    for chave, valor in [("nome_supervisor", nome_supervisor), ("unidade", unidade)]:
        if valor and valor not in historico[chave]:
            historico[chave].insert(0, valor)
            historico[chave] = historico[chave][:MAX_HISTORICO]
    _salvar_historico(historico)

def obter_sugestoes(chave):
    """Retorna as sugestões para a chave especificada do histórico."""
    return _carregar_historico().get(chave, [])