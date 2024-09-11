import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class AbaConfiguracoes:
    """Classe para criar e controlar a aba de configurações."""

    def __init__(self, master):
        self.master = master
        self.frame_aba = tk.Frame(self.master, bg="#2C2C2C", width=360) 
        self.frame_aba.pack_propagate(False) 
        self.aberta = False

        # Carrega o ícone e redimensiona para 32x32
        caminho_icone = os.path.join("files", "intern", "gear.png")
        imagem_icone = Image.open(caminho_icone)
        imagem_icone = imagem_icone.resize((32, 32), Image.LANCZOS) 
        self.icone = ImageTk.PhotoImage(imagem_icone)

        # Cria o botão de engrenagem
        self.botao_engrenagem = tk.Button(
            self.master,
            image=self.icone,
            command=self.alternar_aba,
            bg="#202020",
            borderwidth=0,
            relief="flat",
            activebackground = "#202020"
        )
        self.botao_engrenagem.image = self.icone
        self.botao_engrenagem.place(x=0, y=0, anchor="ne", relx=1, rely=0)

        # Frame para o título e o botão de fechar
        self.frame_titulo = tk.Frame(self.frame_aba, bg="#2C2C2C")
        self.frame_titulo.grid(row=0, column=0, sticky="ew", padx=10, pady=5) # Ocupa toda a largura da coluna

        # Botão "X" para fechar a aba
        self.botao_fechar = tk.Button(
            self.frame_titulo,
            text="X",
            command=self.fechar_aba,
            bg="#2C2C2C",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        self.botao_fechar.grid(row=0, column=0, sticky="w") # Alinhado à esquerda

        # Título "Configurações"
        self.label_titulo = tk.Label(
            self.frame_titulo, 
            text="Configurações", 
            font=("Poppins", 14, "bold"),
            fg="white",
            bg="#2C2C2C"
        )
        self.label_titulo.grid(row=0, column=1, sticky="ew") # Expande para ocupar o espaço restante

        # Configura as colunas do grid no frame_titulo
        self.frame_titulo.columnconfigure(0, weight=0) # Coluna 0 não se expande
        self.frame_titulo.columnconfigure(1, weight=1) # Coluna 1 se expande para centralizar o título

        # Cria os botões de configuração 
        self.botao_tema = tk.Button(self.frame_aba, text="Alterar Tema", command=self.alterar_tema)
        self.botao_tema.pack(pady=10)
        # ... (adicione outros botões de configuração aqui) ...

    def alternar_aba(self):
        """Alterna a visibilidade da aba de configurações com animação."""
        if self.aberta:
            self.fechar_aba()
        else:
            self.abrir_aba()

    def abrir_aba(self):
        """Abre a aba de configurações deslizando da direita para a esquerda."""
        self.aberta = True
        largura_janela = self.master.winfo_width()
        largura_aba = 360 # Largura final da aba

        self.frame_aba.place(x=largura_janela - largura_aba, y=0, relheight=1, width=largura_aba) 
        self.frame_aba.lift()

        for posicao_x in range(largura_janela - largura_aba, largura_janela - largura_aba // 2, -10): 
            self.frame_aba.place(x=posicao_x)
            self.master.update()

    def fechar_aba(self):
        """Fecha a aba de configurações deslizando para a direita."""
        self.aberta = False
        for largura in range(360, -1, -10):
            self.frame_aba.config(width=largura)
            self.master.update()
        self.frame_aba.place_forget() # Remove o frame da aba

    def alterar_tema(self):
        """Exemplo de função para alterar o tema da aplicação (ainda não implementada)."""
        print("Função 'alterar_tema' ainda não implementada.")
        # Implemente aqui a lógica para alterar o tema da aplicação

    def posicionar_botao_engrenagem(self, botao_arquivos_anteriores):
        """Posiciona o botão de engrenagem no canto superior direito,
        ajustando-se ao redimensionamento da janela.
        """
        botao_arquivos_anteriores.update_idletasks()
        x = botao_arquivos_anteriores.winfo_x() + botao_arquivos_anteriores.winfo_width() + 10
        y = botao_arquivos_anteriores.winfo_y()
        self.botao_engrenagem.place(x=x, y=y, anchor="ne", relx=0.95, rely=0)