# logica_aplicacao.py
import os
from datetime import datetime

def salvar_dados(nome_supervisor, data, unidade, caminho_arquivo_txt):
    """Processa os dados do arquivo TXT e retorna os dados formatados.

    Args:
        nome_supervisor (str): Nome do supervisor.
        data (str): Data no formato desejado.
        unidade (str): Unidade.
        caminho_arquivo_txt (str): Caminho para o arquivo TXT a ser processado.

    Returns:
        tuple: Uma tupla contendo o novo caminho do arquivo e os dados formatados, 
               ou (None, None) em caso de erro.
    """
    # Remover caracteres especiais do nome do arquivo
    nome_supervisor = "".join(e for e in nome_supervisor if e.isalnum())
    data_limpa = "".join(e for e in data if e.isdigit())
    unidade_limpia = "".join(e for e in unidade if e.isalnum())

    try:
        with open(caminho_arquivo_txt, "r") as arquivo:
            linhas = arquivo.readlines()

        # Criar uma lista para armazenar os dados formatados
        dados_formatados = []

        # Dicionário de substituições para caracteres problemáticos
        substituicoes = {
            "Ã§": "c",
            "Ã£": "a",
            "Ã³": "o",
            "Âº": "o",
            # Adicione outras substituições conforme necessário
        }

        # Pular a primeira linha (cabeçalho)
        for linha in linhas[1:]:
            campos = linha.strip().split(";")
            if len(campos) >= 15:
                # Aplicar substituições nos campos
                for i in range(len(campos)):
                    for chave, valor in substituicoes.items():
                        campos[i] = campos[i].replace(chave, valor)

                dados_formatados.append(
                    f"""
Funcionario: {campos[1]}
Atividade: {campos[2]}
Pastas Aprovadas: {campos[3]}
Imagens Aprovadas: {campos[4]}
Documentos Aprovados: {campos[5]}
Tempo Aprovado: {campos[6]}
Pastas Rejeitadas: {campos[7]}
Imagens Rejeitadas: {campos[8]}
Documentos Rejeitados: {campos[9]}
Tempo Rejeitado: {campos[10]}
Total de Pastas: {campos[11]}
Total de Imagens: {campos[12]}
Total de Documentos: {campos[13]}
Total de Tempo: {campos[14]}
"""
                )

        pasta_dados = "files/data"
        os.makedirs(pasta_dados, exist_ok=True)
        novo_nome_arquivo = (
            f"{unidade_limpia}_{nome_supervisor}_{data_limpa}.txt"
        )
        novo_caminho_arquivo = os.path.join(pasta_dados, novo_nome_arquivo)

        # Obter data e hora atual
        data_hora_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Escrever dados formatados no arquivo com a nova linha de cabeçalho
        with open(novo_caminho_arquivo, "w") as arquivo_formatado:
            # Adicionar a linha de cabeçalho
            arquivo_formatado.write(f"Supervisor: {nome_supervisor} Data de Envio: {data_hora_envio} Data Informada: {data} Unidade: {unidade}\n\n")
            # Escrever os dados formatados
            for dado in dados_formatados:
                arquivo_formatado.write(dado + "\n")

        # Excluir o arquivo original após o processamento
        os.remove(caminho_arquivo_txt)

        return novo_caminho_arquivo, dados_formatados  # Retornar dados_formatados também
    except Exception as e:
        print(f"Ocorreu um erro ao salvar os dados: {e}")
        return None, None  # Retornar None para ambos em caso de erro