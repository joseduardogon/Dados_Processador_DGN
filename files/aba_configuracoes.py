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

        # Carrega o ícone e redimensiona para 20x20
        caminho_icone = os.path.join("files", "intern", "gear.png")
        imagem_icone = Image.open(caminho_icone)
        imagem_icone = imagem_icone.resize((20, 20), Image.LANCZOS) 
        self.icone = ImageTk.PhotoImage(imagem_icone)

        # Cria o botão de engrenagem
        self.botao_engrenagem = tk.Button(
            self.master,
            image=self.icone,
            command=self.alternar_aba,
            bg="#202020",
            borderwidth=0,
            relief="flat"
        )
        self.botao_engrenagem.image = self.icone
        # Define a posição inicial do botão (fora da tela)
        self.botao_engrenagem.place(x=0, y=0, anchor="ne", relx=1, rely=0) 

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
        """Abre a aba de configurações deslizando da direita."""
        self.aberta = True
        largura_janela = self.master.winfo_width() # Obtem a largura da janela principal
        self.frame_aba.place(x=largura_janela, y=0, relheight=1, width=0)
        self.frame_aba.lift()
        for largura in range(0, 361, 10):
            self.frame_aba.config(width=largura)
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

    def posicionar_botao_engrenagem(self):
        """Posiciona o botão de engrenagem no canto superior direito,
        ajustando-se ao redimensionamento da janela.
        """
        # Atualiza a posição do botão
        self.botao_engrenagem.pack(y=10, x=40, side="top", anchor="ne")