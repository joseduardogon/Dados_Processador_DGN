# interface_inicial.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

import funcoes_preenchimento as funcoes
import historico_preenchimento as historico
import interface_elementos as elementos
import calcular_pontos
import logica_aplicacao 

# Variável global para armazenar o caminho do arquivo selecionado
caminho_arquivo_txt = None

def escolher_arquivo_formatado():
    """Permite que o usuário escolha um arquivo formatado para calcular os pontos."""
    caminho_arquivo = filedialog.askopenfilename(
        initialdir=os.path.join("files", "data"),
        title="Selecione um Arquivo Formatado",
        filetypes=(("Arquivos de Texto", "*.txt"),)
    )
    if caminho_arquivo:
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados_formatados = f.read().strip().split('\n\n')
                calcular_pontos.exibir_pontuacoes(
                    calcular_pontos.calcular_pontuacao(
                        calcular_pontos.criar_arquivo_json_temporario(dados_formatados)
                    )
                )
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao abrir o arquivo: {e}")

def processar_dados():
    """Processa os dados do arquivo selecionado e abre a interface de dados."""
    global caminho_arquivo_txt
    if caminho_arquivo_txt:
        try:
            # Obter os valores dos widgets Entry/Combobox
            nome_supervisor = combo_nome_supervisor.get()
            data = entrada_data.get()
            unidade = combo_unidade.get()

            # Validação simples dos campos de entrada
            if not all([nome_supervisor, data, unidade]):
                raise ValueError("Por favor, preencha todos os campos.")

            # Chamar a função de lógica para processar os dados
            novo_caminho_arquivo, dados_formatados = logica_aplicacao.salvar_dados(
                nome_supervisor, data, unidade, caminho_arquivo_txt
            )

            if novo_caminho_arquivo:
                # Abrir a interface para exibir os dados formatados
                funcoes.iniciar_interface_dados(novo_caminho_arquivo, dados_formatados)
            else:
                raise Exception("Não foi possível salvar os dados.")

            # Atualizar o histórico após o processamento
            historico.atualizar_historico(nome_supervisor, unidade)
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    else:
        messagebox.showerror("Erro", "Nenhum arquivo foi selecionado.")

def escolher_arquivo():
    """Abre a caixa de diálogo para seleção de arquivo, 
    atualiza a label e exibe o ícone.
    """
    global caminho_arquivo_txt
    caminho_arquivo = filedialog.askopenfilename(
        filetypes=[("Arquivos TXT", "*.txt")]
    )

    if caminho_arquivo:
        caminho_arquivo_txt = caminho_arquivo
        elementos.atualizar_arquivo_selecionado(
            label_arquivo_selecionado, caminho_arquivo
        )
        elementos.exibir_icone(
            caixa_icone, os.path.join("files", "intern", "txt.ico")
        )

def atualizar_sugestoes(event, chave):
    """Atualiza a lista de sugestões do Combobox com base no histórico.

    Args:
        event (tk.Event): Evento que disparou a função.
        chave (str): Chave para buscar no histórico ('nome_supervisor' ou 'unidade').
    """
    widget = event.widget
    texto = widget.get()
    sugestoes = historico.obter_sugestoes(chave)

    if texto:
        widget.config(values=[s for s in sugestoes if texto.lower() in s.lower()])
    else:
        widget.config(values=sugestoes)

# --- Interface Gráfica ---
janela = tk.Tk()
janela.title("Dados de Supervisores")
janela.geometry("720x600")
janela.configure(bg="#202020")  # Cor de fundo escura

# Estilo para o Combobox
estilo_combobox = ttk.Style()
estilo_combobox.theme_use("clam")
estilo_combobox.configure(
    "TCombobox",
    background="#3C3C3C",
    foreground="#FFFFFF",
    fieldbackground="#3C3C3C",
    selectbackground="#3C3C3C",
    selectforeground="#FFFFFF",
)

# Criação dos widgets usando as funções de interface_elementos.py
label_nome_supervisor = tk.Label(
    janela, text="Nome do Supervisor:", bg="#202020", fg="#FFFFFF", anchor="w"
)
label_nome_supervisor.pack(padx=(20, 0), pady=(20, 5), anchor="w")

entrada_nome_supervisor = tk.StringVar()
combo_nome_supervisor = ttk.Combobox(
    janela, textvariable=entrada_nome_supervisor, width=47, values=historico.obter_sugestoes("nome_supervisor")
)
combo_nome_supervisor.pack(padx=(20, 0), pady=(0, 20), anchor="w")

label_data = tk.Label(janela, text="Data:", bg="#202020", fg="#FFFFFF", anchor="w")
label_data.pack(padx=(20, 0), pady=(0, 5), anchor="w")

entrada_data = tk.StringVar()
entrada_data = tk.Entry(
    janela,
    width=50,
    bg="#3C3C3C",
    fg="#FFFFFF",
    insertbackground="white",
    textvariable=entrada_data
)
entrada_data.pack(padx=(20, 0), pady=(0, 20), anchor="w")

label_unidade = tk.Label(
    janela, text="Unidade:", bg="#202020", fg="#FFFFFF", anchor="w"
)
label_unidade.pack(padx=(20, 0), pady=(0, 5), anchor="w")

entrada_unidade = tk.StringVar()
combo_unidade = ttk.Combobox(
    janela, textvariable=entrada_unidade, width=47, values=historico.obter_sugestoes("unidade")
)
combo_unidade.pack(padx=(20, 0), pady=(0, 20), anchor="w")

botao_escolher = tk.Button(
    janela,
    text="Escolher Arquivo",
    command=escolher_arquivo,
    bg="#4C4C4C",
    fg="#FFFFFF",
    borderwidth=2,
    relief="raised",
)
botao_escolher.pack(pady=(0, 10), padx=20, anchor="w")

caixa_icone = tk.Label(janela, bg="#202020")
caixa_icone.pack(padx=(20, 0), pady=(0, 10), anchor="w")

label_arquivo_selecionado = tk.Label(
    janela, text="", bg="#202020", fg="#FFFFFF", anchor="w"
)
label_arquivo_selecionado.pack(padx=(20, 0), pady=(0, 10), anchor="w")

botao_processar = tk.Button(
    janela,
    text="Processar Dados",
    command=processar_dados,
    bg="#2ECC71",
    fg="#FFFFFF",
    font=("Arial", 12, "bold"),
    borderwidth=0,
    relief="flat",
)
botao_processar.pack(pady=(0, 10), padx=20, fill="x", expand=False)

botao_escolher_formatado = tk.Button(
    janela,
    text="Calcular Pontos de Arquivo Formatado",
    command=escolher_arquivo_formatado,
    bg="#4C4C4C",
    fg="#FFFFFF",
    borderwidth=2,
    relief="raised",
)
botao_escolher_formatado.pack(padx=20, pady=(0, 10))

# Binding para atualizar sugestões enquanto digita
combo_nome_supervisor.bind(
    "<KeyRelease>", lambda event: atualizar_sugestoes(event, "nome_supervisor")
)
combo_unidade.bind("<KeyRelease>", lambda event: atualizar_sugestoes(event, "unidade"))

janela.mainloop()