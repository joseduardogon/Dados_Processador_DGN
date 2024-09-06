# funcoes_preenchimento.py

import tkinter as tk
from tkinter import messagebox, Text
import calcular_pontos

def iniciar_interface_dados(caminho_arquivo, dados_formatados):
    """Inicializa a interface gráfica para exibir os dados formatados.

    Args:
        caminho_arquivo (str): Caminho para o arquivo de dados formatado.
        dados_formatados (list): Lista de strings contendo os dados formatados.
    """
    try:
        janela_dados = tk.Toplevel()
        janela_dados.title("Dados do Arquivo")
        janela_dados.configure(bg="#2C2C2C")

        # Área de texto para exibir os dados formatados
        area_texto = Text(
            janela_dados,
            bg="#1E1E1E",
            fg="#FFFFFF",
            wrap=tk.WORD,
            font=("Consolas", 10),
        )
        area_texto.pack(expand=True, fill="both", padx=20, pady=20)

        # Inserir os dados formatados na área de texto
        exibir_dados_formatados(area_texto, dados_formatados)

        area_texto.config(state=tk.DISABLED)  # Impede edição dos dados

        # Botão para calcular pontos
        botao_calcular = calcular_pontos.criar_botao_calcular(janela_dados, dados_formatados)
        botao_calcular.pack(pady=(0, 20))

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao exibir os dados: {e}")

def exibir_dados_formatados(area_texto, dados_formatados):
    """Exibe os dados formatados na área de texto.

    Args:
        area_texto (tk.Text): Widget de área de texto para exibir os dados.
        dados_formatados (list): Lista de strings contendo os dados formatados.
    """
    for dado in dados_formatados:
        area_texto.insert(tk.END, dado + "\n")