import tkinter as tk
from tkinter import filedialog, messagebox
import os

class ListaArquivos:
    def __init__(self, master):
        self.master = master
        self.master.title("Lista de Arquivos")
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=20, padx=20)

        self.lista_arquivos = tk.Listbox(self.frame, width=50, height=15)
        self.lista_arquivos.pack(side="left", fill="both", expand=True)
        self.lista_arquivos.bind("<<ListboxSelect>>", self.exibir_detalhes)

        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.lista_arquivos.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lista_arquivos.yview)

        self.frame_detalhes = tk.Frame(self.master, bg="#202020")  # Cor de fundo escura
        self.frame_detalhes.pack(pady=10, fill="x")
        self.label_detalhes = tk.Label(self.frame_detalhes, text="", bg="#202020", fg="white", wraplength=350)
        self.label_detalhes.pack()

        self.carregar_lista_arquivos()

    def carregar_lista_arquivos(self):
        """Carrega a lista de arquivos do diretório 'data'."""
        self.lista_arquivos.delete(0, tk.END)
        caminho_data = os.path.join("files", "data")
        try:
            arquivos = os.listdir(caminho_data)
            for arquivo in arquivos:
                if arquivo.endswith(".txt"):
                    self.lista_arquivos.insert(tk.END, arquivo)
        except FileNotFoundError:
            messagebox.showwarning("Aviso", "Diretório 'data' não encontrado!")

    def exibir_detalhes(self, event):
        """Exibe os detalhes do arquivo selecionado."""
        selecao = self.lista_arquivos.curselection()
        if selecao:
            indice = selecao[0]
            nome_arquivo = self.lista_arquivos.get(indice)
            caminho_arquivo = os.path.join("files", "data", nome_arquivo)

            try:
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    primeira_linha = f.readline().strip()

                # Extrair informações da primeira linha (ajuste conforme necessário)
                partes = primeira_linha.split(" ")
                supervisor = partes[1]
                data_envio = partes[4]
                data_informada = partes[7]
                unidade = partes[10]

                # Formatar os detalhes
                detalhes = f"Nome do arquivo: {nome_arquivo}\n"
                detalhes += f"Supervisor: {supervisor}\n"
                detalhes += f"Data de Envio: {data_envio}\n"
                detalhes += f"Data Informada: {data_informada}\n"
                detalhes += f"Unidade: {unidade}\n"

                self.label_detalhes.config(text=detalhes)

                # Botões Modificar e Deletar
                self.criar_botoes_acoes(caminho_arquivo)

            except FileNotFoundError:
                messagebox.showwarning("Aviso", f"Arquivo '{nome_arquivo}' não encontrado!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir o arquivo: {e}")

    def criar_botoes_acoes(self, caminho_arquivo):
        """Cria os botões 'Modificar' e 'Deletar' para o arquivo selecionado."""
        try:
            # Remove botões anteriores, se existirem
            for widget in self.frame_detalhes.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.destroy()

            def modificar_arquivo():
                """Abre o arquivo selecionado no Bloco de Notas."""
                os.system(f"notepad.exe {caminho_arquivo}")

            def deletar_arquivo():
                """Exclui o arquivo selecionado após confirmação do usuário."""
                if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o arquivo '{os.path.basename(caminho_arquivo)}'?"):
                    try:
                        os.remove(caminho_arquivo)
                        self.carregar_lista_arquivos()  # Atualiza a lista após a exclusão
                        self.label_detalhes.config(text="")  # Limpa os detalhes
                        messagebox.showinfo("Sucesso", f"Arquivo '{os.path.basename(caminho_arquivo)}' excluído com sucesso!")
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao excluir o arquivo: {e}")

            # Cria os botões
            botao_modificar = tk.Button(self.frame_detalhes, text="Modificar", command=modificar_arquivo, bg="#4C4C4C", fg="white")
            botao_modificar.pack(side="left", padx=5, pady=5)
            botao_deletar = tk.Button(self.frame_detalhes, text="Deletar", command=deletar_arquivo, bg="red", fg="white")
            botao_deletar.pack(side="left", padx=5, pady=5)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar botões: {e}")


def abrir_lista_arquivos():
    """Cria a janela da lista de arquivos."""
    janela_lista = tk.Tk()
    ListaArquivos(janela_lista)
    janela_lista.mainloop()