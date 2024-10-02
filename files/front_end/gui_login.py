from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from PyQt5.QtGui import QFont, QPainterPath, QRegion

from analista_dados.files.back_end.controle_login import verificar_tabela_login, obter_dados_usuario


class LoginWindow(QWidget):
    login_sucedido = pyqtSignal(dict)  # Sinal emitido quando o login for bem-sucedido

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)
        self.setFixedSize(self.size())
        self.setStyleSheet("background-color: white;")

        # Layouts
        layout_principal = QVBoxLayout()
        layout_campos = QVBoxLayout()
        layout_botao = QHBoxLayout()

        # Widgets
        label_usuario = QLabel("Usuário:", self)
        self.campo_usuario = QLineEdit(self)

        label_senha = QLabel("Senha:", self)
        self.campo_senha = QLineEdit(self)
        self.campo_senha.setEchoMode(QLineEdit.Password)

        self.botao_entrar = QPushButton("Entrar", self)
        self.botao_entrar.setObjectName("botao_selecionar")
        self.botao_entrar.clicked.connect(self.autenticar)

        # Adicionar widgets aos layouts
        layout_campos.addWidget(label_usuario)
        layout_campos.addWidget(self.campo_usuario)
        layout_campos.addWidget(label_senha)
        layout_campos.addWidget(self.campo_senha)
        layout_botao.addWidget(self.botao_entrar)

        layout_principal.addLayout(layout_campos)
        layout_principal.addLayout(layout_botao)
        self.setLayout(layout_principal)

        # Centralizar a janela
        self.centrar_janela()

    def centrar_janela(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def autenticar(self):
        """Autentica o usuário."""
        nome_usuario = self.campo_usuario.text()
        senha_digitada = self.campo_senha.text()

        # 1. Verificar se a tabela de usuários existe (e cria se não existir)
        verificar_tabela_login()

        # 2. Buscar os dados do usuário no banco de dados
        dados_usuario = obter_dados_usuario(nome_usuario)

        if dados_usuario:
            senha_banco, tipo_usuario, unidade = dados_usuario

            # 3. Verificar a senha
            if senha_digitada == senha_banco:  # Substitua senha_correta pela sua lógica de verificação
                # 4. Login bem-sucedido!
                global usuario_atual  # Defina usuario_atual como global
                usuario_atual = {"nome": nome_usuario, "tipo": tipo_usuario, "unidade": unidade}
                self.login_sucedido.emit(usuario_atual)  # Emite o sinal de login bem-sucedido
            else:
                QMessageBox.warning(self, "Erro", "Senha incorreta!")
        else:
            QMessageBox.warning(self, "Erro", "Usuário não encontrado!")
        print(f"gui_login: {usuario_atual}")