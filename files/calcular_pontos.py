import os
import json
from unidecode import unidecode
import tkinter as tk

# Constantes para os caminhos dos arquivos
PESOS_ARQUIVO = os.path.join("files", "intern", "pesos.json")
TEMP_DATA_ARQUIVO = os.path.join("files", "intern", "temp_data.json")

# Carregar os pesos do arquivo JSON
try:
    with open(PESOS_ARQUIVO, "r") as f:
        PESOS = json.load(f)
except FileNotFoundError:
# Definir pesos padrão caso o arquivo não seja encontrado
    PESOS = {
    "DIGITALIZACAO": 0.006666666666666667,  # Correção aqui
    "CONTROLEDEQUALIDADE": 0.005,
    "CLASSIFICACAO": 0.015,
    "VERIFICACAO": 0.08,
    "OCR2": 0,
    "VALIDACAO2": 0,
    "EXPORTACAO": 0,
    "SUSPENSOEXPORTACAO": 0
    }

class Funcionario:
    """Representa um funcionário e seus pontos de produtividade."""

    def __init__(self, nome, atividade=None, imagens_aprovadas=0, documentos_aprovados=0):
        self.nome = nome
        self.atividade = atividade
        self.imagens_aprovadas = imagens_aprovadas
        self.documentos_aprovados = documentos_aprovados
        self.pontos = self._calcular_pontos()

    def _calcular_pontos(self):
        """Calcula os pontos do funcionário basedos em suas atividades."""
        pontos = {"DIGIT": 0, "CQ": 0, "CLASS": 0, "VERIFICACAO": 0, "SUSPENSOEXPORTACAO": 0}
        if self.atividade:
            chave_atividade = unidecode(self.atividade).replace(" ", "").upper()
            chave_atividade = chave_atividade.replace("(", "").replace(")", "")
            if chave_atividade in PESOS:
                if chave_atividade == "VERIFICACAO":  # Condição especial para Verificacao
                    pontos[chave_atividade] += self.documentos_aprovados * PESOS.get(chave_atividade, 0)
                else:
                    pontos[chave_atividade] += self.imagens_aprovadas * PESOS.get(chave_atividade, 0)
        pontos["Total"] = sum(pontos.values())
        return pontos

    def __str__(self):
        """Retorna uma representação em string do funcionário."""
        return f"Funcionário: {self.nome}\n" + \
               "\n".join(f"  {atividade}: {valor:.2f}" for atividade, valor in self.pontos.items())

def _extrair_dados_relevantes(dados_formatados):
    """Extrai dados relevantes para cálculo de pontuação."""
    funcionarios = []
    atividades_relevantes = ["Controle de Qualidade", "Verificacao", 
                              "Digitalizacao (Scanner)", "Classificacao"]

    for dado in dados_formatados:
        nome = None
        atividade = None
        imagens_aprovadas = 0
        documentos_aprovados = 0
        for linha in dado.strip().split("\n"):
            if ": " in linha:
                chave, valor = linha.split(": ")
                if chave == "Funcionario":
                    nome = valor
                elif chave == "Atividade" and valor in atividades_relevantes:
                    atividade = valor
                elif chave == "Imagens Aprovadas":
                    imagens_aprovadas = int(valor)
                elif chave == "Documentos Aprovados":
                    documentos_aprovados = int(valor)
        if nome and atividade:
            funcionario = Funcionario(nome, atividade, imagens_aprovadas, documentos_aprovados)
            funcionarios.append(funcionario)

    return funcionarios


def criar_arquivo_json_temporario(dados_formatados):
    """Cria um arquivo JSON temporário com os dados relevantes."""
    try:
        funcionarios = _extrair_dados_relevantes(dados_formatados)
        dados_json = [{
            "nome": func.nome,
            "atividade": func.atividade,
            "imagens_aprovadas": func.imagens_aprovadas,
            "documentos_aprovados": func.documentos_aprovados,
            "pontos": func.pontos
        } for func in funcionarios] 
        with open(TEMP_DATA_ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump(dados_json, f, ensure_ascii=False, indent=4)
        return TEMP_DATA_ARQUIVO
    except Exception as e:
        print(f"Erro ao criar arquivo JSON: {e}")
        return None

def calcular_pontuacao(caminho_json):
    """Calcula a pontuação de todos os funcionários do arquivo JSON."""
    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        funcionarios = [Funcionario(
            d["nome"],
            d["atividade"],
            d["imagens_aprovadas"],
            d["documentos_aprovados"]
        ) for d in dados]

        return {func.nome: func.pontos for func in funcionarios}

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao ler arquivo JSON: {e}")
        return None

def _exibir_pontuacoes_na_interface(janela_pontos, pontuacoes):
    """Exibe as pontuações na interface gráfica."""
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

def exibir_pontuacoes(pontuacoes):
    """Cria a janela e exibe as pontuações."""
    janela_pontos = tk.Toplevel()
    janela_pontos.title("Pontuação dos Funcionários")
    janela_pontos.configure(bg="#202020")
    _exibir_pontuacoes_na_interface(janela_pontos, pontuacoes)


def criar_botao_calcular(janela, dados_formatados):
    """Cria o botão 'Calcular Pontos' na janela."""
    def chamar_calcular_pontuacao():
        """Chama as funções para calcular e exibir pontuações."""
        caminho_json = criar_arquivo_json_temporario(dados_formatados)
        if caminho_json:
            pontuacoes = calcular_pontuacao(caminho_json)
            if pontuacoes:
                exibir_pontuacoes(pontuacoes)

    botao = tk.Button(janela, text="Calcular Pontos", command=chamar_calcular_pontuacao)
    botao.pack(pady=10)
    return botao