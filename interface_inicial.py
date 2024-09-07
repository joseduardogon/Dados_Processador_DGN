"""Módulo responsável pela interface gráfica inicial da aplicação."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from datetime import datetime

# Importações de outros módulos da aplicação
import funcoes_preenchimento as funcoes
import historico_preenchimento as historico
import interface_elementos as elementos
import calcular_pontos
import logica_aplicacao

# Variável global para armazenar o caminho do arquivo selecionado
caminho_arquivo_txt = None

def abrir_arquivo_formatado():
    """
    Permite que o usuário selecione um arquivo formatado, abra-o 
    em uma nova janela e permita o cálculo de pontos.
    """
    caminho_arquivo = filedialog.askopenfilename(
        initialdir=os.path.join("files", "data"),
        title="Selecione um Arquivo Formatado",
        filetypes=(("Arquivos de Texto", "*.txt"),)
    )
    if caminho_arquivo:
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados_formatados = f.read().strip().split('\n\n')
                funcoes.iniciar_interface_dados(caminho_arquivo, dados_formatados)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao abrir o arquivo: {e}")

def processar_dados():
    """
    Processa os dados do arquivo selecionado, salva as informações 
    em um novo arquivo formatado e abre uma interface 
    para exibir os dados processados.
    """
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

            # Remove caracteres especiais da data, deixando apenas números
            data = "".join(e for e in data if e.isdigit())

            # Chamar a função de lógica para processar os dados
            novo_caminho_arquivo, dados_formatados = logica_aplicacao.salvar_dados(
                nome_supervisor, data, unidade, caminho_arquivo_txt
            )

            if novo_caminho_arquivo:
                funcoes.iniciar_interface_dados(novo_caminho_arquivo, dados_formatados)
            else:
                raise Exception("Não foi possível salvar os dados.")

            # Atualizar o histórico após o processamento
            historico.atualizar_historico(nome_supervisor, unidade, data)
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    else:
        messagebox.showerror("Erro", "Nenhum arquivo foi selecionado.")

def escolher_arquivo():
    """
    Abre a caixa de diálogo para seleção de arquivo, 
    atualiza a label com o nome do arquivo selecionado e 
    exibe o ícone correspondente ao tipo de arquivo.
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
    """
    Atualiza a lista de sugestões do Combobox com base 
    no histórico de entradas do usuário.

    Args:
        event (tk.Event): Evento que disparou a função.
        chave (str): Chave para buscar no histórico 
                   ('nome_supervisor', 'data' ou 'unidade').
    """
    widget = event.widget
    texto = widget.get()
    sugestoes = historico.obter_sugestoes(chave)

    if texto:
        if isinstance(widget, ttk.Combobox):  # Verifica se é um Combobox
            widget.config(values=[s for s in sugestoes if texto.lower() in s.lower()])
    else:
        if isinstance(widget, ttk.Combobox):  # Verifica se é um Combobox
            widget.config(values=sugestoes)

def formatar_data(event):
    """
    Formata a data no campo de entrada, removendo caracteres não numéricos 
    e inserindo barras (/) nos lugares corretos, no formato DD/MM/AA.
    """
    data = entrada_data.get().replace("/", "")
    nova_data = ""
    for i, digito in enumerate(data):
        if i == 2 or i == 4:
            nova_data += "/" + digito
        else:
            nova_data += digito
    entrada_data.delete(0, tk.END)
    entrada_data.insert(0, nova_data)

# --- Interface Gráfica ---

# Janela principal
janela = tk.Tk()
janela.title("Dados de Supervisores")
janela.geometry("720x600")
janela.configure(bg="#202020") 

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

# Botão para abrir arquivos anteriores
botao_arquivos_anteriores = tk.Button(
    janela,
    text="Processar Arquivos Anteriores",
    command=abrir_arquivo_formatado,
    bg="#4C4C4C",
    fg="#FFFFFF",
    borderwidth=2,
    relief="raised",
)
botao_arquivos_anteriores.pack(pady=10, padx=20, side="top", anchor="ne")

# Nome do Supervisor
label_nome_supervisor = tk.Label(
    janela, text="Nome do Supervisor:", bg="#202020", fg="#FFFFFF", anchor="w"
)
label_nome_supervisor.pack(padx=(20, 0), pady=(20, 5), anchor="w")

entrada_nome_supervisor = tk.StringVar()
combo_nome_supervisor = ttk.Combobox(
    janela, textvariable=entrada_nome_supervisor, width=47, values=historico.obter_sugestoes("nome_supervisor")
)
combo_nome_supervisor.pack(padx=(20, 0), pady=(0, 20), anchor="w")

# Data
label_data = tk.Label(janela, text="Data:", bg="#202020", fg="#FFFFFF", anchor="w")
label_data.pack(padx=(20, 0), pady=(0, 5), anchor="w")

# Define a data atual como sugestão no formato DD/MM/AA
data_atual = datetime.now().strftime("%d/%m/%y")
entrada_data = tk.StringVar(value=data_atual)
entrada_data = tk.Entry(
    janela,
    width=50,
    bg="#3C3C3C",
    fg="#FFFFFF",
    insertbackground="white",
    textvariable=entrada_data
)
entrada_data.pack(padx=(20, 0), pady=(0, 20), anchor="w")
entrada_data.bind("<KeyRelease>", formatar_data)

# Unidade
label_unidade = tk.Label(
    janela, text="Unidade:", bg="#202020", fg="#FFFFFF", anchor="w"
)
label_unidade.pack(padx=(20, 0), pady=(0, 5), anchor="w")

entrada_unidade = tk.StringVar()
combo_unidade = ttk.Combobox(
    janela, textvariable=entrada_unidade, width=47, values=historico.obter_sugestoes("unidade")
)
combo_unidade.pack(padx=(20, 0), pady=(0, 20), anchor="w")

# Botão Escolher Arquivo
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

# Ícone do arquivo
caixa_icone = tk.Label(janela, bg="#202020")
caixa_icone.pack(padx=(20, 0), pady=(0, 10), anchor="w")

# Label para exibir o arquivo selecionado
label_arquivo_selecionado = tk.Label(
    janela, text="", bg="#202020", fg="#FFFFFF", anchor="w"
)
label_arquivo_selecionado.pack(padx=(20, 0), pady=(0, 10), anchor="w")

# Botão Processar Dados
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


# Bindings para atualizar sugestões enquanto digita
combo_nome_supervisor.bind(
    "<KeyRelease>", lambda event: atualizar_sugestoes(event, "nome_supervisor")
)
combo_unidade.bind("<KeyRelease>", lambda event: atualizar_sugestoes(event, "unidade"))
entrada_data.bind("<KeyRelease>", lambda event: atualizar_sugestoes(event, "data"))


janela.mainloop()