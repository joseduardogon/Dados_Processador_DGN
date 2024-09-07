"""Módulo com funções auxiliares para interface gráfica."""
import os
import tkinter as tk
from tkinter import messagebox, Text
import calcular_pontos

def iniciar_interface_dados(caminho_arquivo, dados_formatados):
    """
    Cria uma nova janela para exibir os dados formatados do arquivo 
    e um botão para calcular os pontos.

    Args:
        caminho_arquivo (str): O caminho do arquivo que está sendo aberto.
        dados_formatados (list): Dados formatados para exibição.
    """
    try:
        janela_dados = tk.Toplevel()
        janela_dados.title(f"Dados do Arquivo - {os.path.basename(caminho_arquivo)}")
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
        for dado in dados_formatados:
            area_texto.insert(tk.END, dado + "\n")

        area_texto.config(state=tk.DISABLED)  # Impede edição dos dados

        def calcular_e_exibir_pontuacoes(dados_formatados):
            """Calcula e exibe as pontuações."""
            caminho_json = calcular_pontos.criar_arquivo_json_temporario(dados_formatados)
            if caminho_json:
                pontuacoes = calcular_pontos.calcular_pontuacao(caminho_json)
                if pontuacoes:
                    calcular_pontos.exibir_pontuacoes(pontuacoes)

        # Botão para calcular pontos
        botao_calcular = tk.Button(
            janela_dados,
            text="Calcular Pontos",
            command=lambda: calcular_e_exibir_pontuacoes(dados_formatados),  # Correção aqui
            bg="#2ECC71",  # Cor verde
            fg="#FFFFFF",
            font=("Arial", 12, "bold"),
            borderwidth=0,
            relief="flat",
        )
        botao_calcular.pack(pady=(0, 20))

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao exibir os dados: {e}")