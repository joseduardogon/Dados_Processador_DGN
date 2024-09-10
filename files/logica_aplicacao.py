# logica_aplicacao.py
import os

def salvar_dados(
    entrada_nome_supervisor, entrada_data, entrada_unidade, caminho_arquivo_txt
):
    """Processa os dados do arquivo TXT, remove funcionários com prefixo 'usu'
       e atividades inválidas, e retorna os dados formatados.
    """
    nome_supervisor = entrada_nome_supervisor
    data = entrada_data
    unidade = entrada_unidade

    # Remover caracteres especiais do nome do arquivo
    nome_supervisor = "".join(e for e in nome_supervisor if e.isalnum())
    data_limpa = "".join(e for e in data if e.isdigit())
    unidade_limpia = "".join(e for e in unidade if e.isalnum())

    try:
        with open(caminho_arquivo_txt, "r") as arquivo:
            linhas = arquivo.readlines()

        # Criar uma lista para armazenar os dados formatados
        dados_formatados = []

        # Atividades válidas
        atividades_validas = [
            "Controle de Qualidade",
            "Verificacao",
            "Digitalizacao (Scanner)",
            "Classificacao"
        ]

        # Dicionário de substituições para caracteres problemáticos
        substituicoes = {
            "Ã§": "c",
            "Ã£": "a",
            "Ã³": "o",
            "Âº": "o",
        }

        # Pular a primeira linha (cabeçalho)
        for linha in linhas[1:]:
            campos = linha.strip().split(";")
            if len(campos) >= 15:
                # Aplicar substituições nos campos
                for i in range(len(campos)):
                    for chave, valor in substituicoes.items():
                        campos[i] = campos[i].replace(chave, valor)
                
                # Verifica se o funcionário possui o prefixo "usu" e se a atividade é válida
                if not campos[1].startswith("usu") and campos[2] in atividades_validas and campos[1] != "Admin":
                    dados_formatados.append(
                        f"""
Funcionario: {campos[1]}
Atividade: {campos[2] if campos[2] != 'Digitalizacao (Scanner)' else 'Digitalizacao'}
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

        # Salvar os dados formatados no arquivo
        with open(novo_caminho_arquivo, "w") as arquivo_formatado:
            for dado in dados_formatados:
                arquivo_formatado.write(dado + "\n")

        # Excluir o arquivo original após o processamento
        os.remove(caminho_arquivo_txt)

        return novo_caminho_arquivo, dados_formatados
    except Exception as e:
        print(f"Ocorreu um erro ao salvar os dados: {e}")
        return None, None