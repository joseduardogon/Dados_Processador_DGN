import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def criar_campo_entrada(janela, label_texto, var, sugestoes=None):
    """Cria um campo de entrada com label e Combobox (opcional)."""
    label = tk.Label(
        janela, text=label_texto, bg="#202020", fg="#FFFFFF", anchor="w"
    )
    label.pack(padx=(20, 0), pady=(0, 5), anchor="w")

    if sugestoes:
        campo = ttk.Combobox(
            janela, textvariable=var, width=47, values=sugestoes
        )
    else:
        campo = tk.Entry(
            janela,
            width=50,
            bg="#3C3C3C",
            fg="#FFFFFF",
            insertbackground="white",
        )
    campo.pack(padx=(20, 0), pady=(0, 20), anchor="w")
    return campo

def criar_botao_arquivo(janela, command):
    """Cria o botão "Escolher Arquivo" e a caixa de ícone."""
    frame_arquivo = tk.Frame(janela, bg="#202020")
    frame_arquivo.pack(pady=(10, 20), padx=20, anchor="w")

    botao = tk.Button(
        frame_arquivo,
        text="Escolher Arquivo",
        command=command,
        bg="#4C4C4C",
        fg="#FFFFFF",
        borderwidth=2,
        relief="raised",
    )
    botao.pack(side="left")

    caixa_icone = tk.Label(frame_arquivo, bg="#202020")
    caixa_icone.pack(side="left", padx=(5, 0))
    return botao, caixa_icone

def criar_botao_processar(janela, command):
    """Cria o botão "Processar Dados" estilizado."""
    botao = tk.Button(
        janela,
        text="Processar Dados",
        command=command,
        bg="#2ECC71",
        fg="#FFFFFF",
        font=("Arial", 12, "bold"),
        borderwidth=0,
        relief="flat",
    )
    botao.pack(pady=(20, 20), padx=20, fill="x", expand=False)
    return botao

def criar_label_arquivo(janela):
    """Cria a label para exibir o arquivo selecionado."""
    label = tk.Label(
        janela, text="", bg="#202020", fg="#FFFFFF", anchor="w"
    )
    label.pack(padx=(20, 0), pady=(0, 10), anchor="w")
    return label

def atualizar_arquivo_selecionado(label, caminho):
    """Atualiza a label com o nome do arquivo."""
    label.config(text=f"Arquivo Selecionado: {caminho}")

def exibir_icone(caixa_icone, caminho_icone):
    """Exibe o ícone na caixa."""
    try:
        icone = Image.open(caminho_icone)
        icone.thumbnail((20, 20))
        foto = ImageTk.PhotoImage(icone)
        caixa_icone.config(image=foto)
        caixa_icone.image = foto
    except Exception as e:
        print(f"Erro ao exibir ícone: {e}")