# calcular_pontos.py
import os
import json
from unidecode import unidecode
import tkinter as tk

# Dicionario para mapeamento de pesos
ATIVIDADES_MAPEAMENTO = {
    "Controle de Qualidade": "CONTROLEDEQUALIDADE",
    "Verificacao": "VERIFICACAO",
    "Digitalizacao (Scanner)": "DIGITALIZACAO",
    "Classificacao": "CLASSIFICACAO"
}

# Constantes para os caminhos dos arquivos
PESOS_ARQUIVO = os.path.join("files", "intern", "pesos.json")
TEMP_DATA_ARQUIVO = os.path.join("files", "intern", "temp_data.json")
PONTOS_ARQUIVO = os.path.join("files", "intern", "pontos.json")

# Carregar os pesos do arquivo JSON
try:
    with open(PESOS_ARQUIVO, "r") as f:
        PESOS = json.load(f)
except FileNotFoundError:
    # Definir pesos padrão caso o arquivo não seja encontrado
    PESOS = {
        "DIGITALIZACAO": 0.006666666666666667,
        "CONTROLEDEQUALIDADE": 0.005,
        "CLASSIFICACAO": 0.015,
        "VERIFICACAO": 0.08,
        "OCR2": 0,
        "VALIDACAO2": 0,
        "EXPORTACAO": 0,
        "SUSPENSOEXPORTACAO": 0
    }

class Funcionario:
    """Representa um funcionário."""

    def __init__(self, nome, atividade=None, imagens_aprovadas=0, documentos_aprovados=0, pastas_aprovadas=0):
        self.nome = nome
        self.atividade = atividade
        self.imagens_aprovadas = imagens_aprovadas
        self.documentos_aprovados = documentos_aprovados
        self.pastas_aprovadas = pastas_aprovadas
        # Calcula os pontos no construtor após definir os atributos
        self.pontos = self.calcular_pontos()

    def calcular_pontos(self):
        """Calcula os pontos do funcionário com base em suas atividades."""
        print(f"Calculando pontos para {self.nome} - Atividade: {self.atividade}")
        pontos = {"DIGIT": 0, "CQ": 0, "CLASS": 0, "VERIFICACAO": 0, "SUSPENSOEXPORTACAO": 0}
        if self.atividade:
            # Obtém a chave do dicionário PESOS a partir do mapeamento
            chave_atividade = ATIVIDADES_MAPEAMENTO.get(self.atividade) 
            print(f"Chave de atividade: {chave_atividade}")
            if chave_atividade and chave_atividade in PESOS:
                if chave_atividade == "VERIFICACAO":
                    pontos[chave_atividade] = self.documentos_aprovados * PESOS.get(chave_atividade, 0)
                    print(f"Pontos VERIFICACAO: {pontos[chave_atividade]}")
                else:
                    pontos[chave_atividade] = self.imagens_aprovadas * PESOS.get(chave_atividade, 0)
                    print(f"Pontos {chave_atividade}: {pontos[chave_atividade]}")
            else:
                print(f"Atividade '{self.atividade}' não encontrada no dicionário de mapeamento ou de pesos.")
        pontos["Total"] = sum(pontos.values())
        print(f"Pontos Totais: {pontos['Total']}\n")
        return pontos

    def to_dict(self):
        """Retorna um dicionário com os dados do funcionário."""
        return {
            "nome": self.nome,
            "atividade": self.atividade,
            "imagens_aprovadas": self.imagens_aprovadas,
            "documentos_aprovados": self.documentos_aprovados,
            "pastas_aprovadas": self.pastas_aprovadas,
            "pontos": self.pontos,
        }

def _extrair_dados_relevantes(dados_formatados):
    """Extrai dados relevantes para cálculo de pontuação."""
    funcionarios = []
    atividades_relevantes = ["Controle de Qualidade", "Verificacao",
                              "Digitalizacao (Scanner)", "Classificacao"]

    for dado in dados_formatados:
        info_funcionario = {}
        for linha in dado.strip().split("\n"):
            if ": " in linha:
                chave, valor = linha.split(": ")
                info_funcionario[chave] = valor
        if "Funcionario" in info_funcionario and "Atividade" in info_funcionario:
            if info_funcionario["Atividade"] in atividades_relevantes:
                funcionario = Funcionario(
                    info_funcionario["Funcionario"],
                    info_funcionario["Atividade"],
                    int(info_funcionario.get("Imagens Aprovadas", 0)),
                    int(info_funcionario.get("Documentos Aprovados", 0)),
                    int(info_funcionario.get("Pastas Aprovadas", 0))
                )
                funcionarios.append(funcionario)

    return funcionarios

def criar_arquivo_json_temporario(dados_formatados):
    """Cria um arquivo JSON temporário com os dados relevantes."""
    try:
        funcionarios = _extrair_dados_relevantes(dados_formatados)
        dados_json = [func.to_dict() for func in funcionarios] 
        with open(TEMP_DATA_ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump(dados_json, f, ensure_ascii=False, indent=4)
        return TEMP_DATA_ARQUIVO
    except Exception as e:
        print(f"Erro ao criar arquivo JSON: {e}")
        return None

def calcular_e_salvar_pontuacoes(caminho_json):
    """Calcula as pontuações e salva em um novo arquivo JSON."""
    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        pontuacoes = {}
        for d in dados:
            # Cria o objeto Funcionario e calcula os pontos
            funcionario = Funcionario(
                d["nome"],
                d["atividade"],
                d["imagens_aprovadas"],
                d["documentos_aprovados"],
                d["pastas_aprovadas"]
            )
            pontuacoes[funcionario.nome] = funcionario.pontos # Armazena os pontos calculados

        with open(PONTOS_ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump(pontuacoes, f, ensure_ascii=False, indent=4)

        return pontuacoes

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao ler arquivo JSON: {e}")
        return None

def exibir_pontuacoes(pontuacoes):
    """Cria a janela e exibe as pontuações."""
    janela_pontos = tk.Toplevel()
    janela_pontos.title("Pontuação dos Funcionários")
    janela_pontos.configure(bg="#202020")
    
    funcionario_max_pontos = max(pontuacoes, key=lambda k: pontuacoes[k]['Total'])
    pontos_max = pontuacoes[funcionario_max_pontos]['Total']

    label_funcionario_max = tk.Label(
        janela_pontos,
        text=f"Funcionário com Maior Pontuação: {funcionario_max_pontos} - Pontos: {pontos_max:.2f}",
        bg="#202020",
        fg="#2ECC71",
        font=("Arial", 12, "bold")
    )
    label_funcionario_max.pack(pady=(20, 10))

    area_texto = tk.Text(
        janela_pontos,
        bg="#3C3C3C",
        fg="#FFFFFF",
        wrap=tk.WORD,
        font=("Consolas", 10)
    )
    area_texto.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    for funcionario, pontos in pontuacoes.items():
        area_texto.insert(tk.END, f"Funcionário: {funcionario}\n")
        for atividade, valor in pontos.items():
            area_texto.insert(tk.END, f"  {atividade}: {valor:.2f}\n")
        area_texto.insert(tk.END, "\n")

    area_texto.config(state=tk.DISABLED)

def criar_botao_calcular(janela, dados_formatados):
    """Cria o botão 'Calcular Pontos' na janela."""
    def chamar_calcular_pontuacao():
        """Chama as funções para calcular, salvar e exibir pontuações."""
        caminho_json = criar_arquivo_json_temporario(dados_formatados)
        if caminho_json:
            pontuacoes = calcular_e_salvar_pontuacoes(caminho_json)
            if pontuacoes:
                exibir_pontuacoes(pontuacoes)

    botao = tk.Button(janela, text="Calcular Pontos", command=chamar_calcular_pontuacao)
    botao.pack(pady=10)
    return botao