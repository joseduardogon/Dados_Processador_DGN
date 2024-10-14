import socket

# Obtém o nome do computador
nome_computador = socket.gethostname()

if nome_computador == "Galile0":
    caminho_db =  "/Users/josed/codes/project/analista_dados/files/database/banco_producao.db"
elif nome_computador == "Galile1":
    caminho_db = "/Users/josed/codes/Dados_Diginotas/project/analista_dados/files/database/banco_producao.db"
