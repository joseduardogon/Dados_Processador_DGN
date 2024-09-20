# styles.py
# Define a stylesheet para a aplicação

STYLESHEET = """
    QWidget { /* Aplica estilo a todos os widgets */
        font-family: Arial;  /* Define a fonte como Arial para todos os widgets */
        font-size: 12pt;   /* Define o tamanho da fonte como 12 pontos para todos os widgets */
    }

    QPushButton {  /* Aplica estilo a todos os botões (QPushButton) */
        border: none;       /* Remove a borda padrão dos botões */
        padding: 10px 20px;  /* Define espaçamento interno (padding) dos botões: 10px acima/abaixo, 20px esquerda/direita */
        border-radius: 5px;  /* Define o raio das bordas dos botões para 5 pixels (arredondamento) */
    }

    QPushButton#botao_confirmar { /* Aplica estilo ao botão com objectName "botao_confirmar" */
        background-color: #2196F3; /* Define a cor de fundo como azul (#2196F3) */
        color: white;             /* Define a cor do texto como branco */
    }
    QPushButton#botao_confirmar:hover { /* Aplica estilo quando o mouse passa por cima do botão "botao_confirmar" */
        background-color: #1976D2; /* Define a cor de fundo como azul mais escuro (#1976D2) */
    }

    QPushButton#botao_selecionar { /* Aplica estilo ao botão com objectName "botao_selecionar" */
        background-color: #4CAF50; /* Define a cor de fundo como verde (#4CAF50) */
        color: white;             /* Define a cor do texto como branco */
    }
    QPushButton#botao_selecionar:hover {  /* Aplica estilo quando o mouse passa por cima do botão "botao_selecionar" */
        background-color: #388E3C; /* Define a cor de fundo como verde mais escuro (#388E3C) */
    }

    QPushButton#botao_cancelar { /* Aplica estilo ao botão com objectName "botao_cancelar" */
        background-color: #f44336; /* Define a cor de fundo como vermelho (#f44336) */
        color: white;             /* Define a cor do texto como branco */
    }
    QPushButton#botao_cancelar:hover {  /* Aplica estilo quando o mouse passa por cima do botão "botao_cancelar" */
        background-color: #d32f2f; /* Define a cor de fundo como vermelho mais escuro (#d32f2f) */
    }

    QPushButton#botao_selecionar:disabled, /* Aplica estilo ao botão "botao_selecionar" quando estiver desabilitado */
    QPushButton#botao_cancelar:disabled { /* Aplica estilo ao botão "botao_cancelar" quando estiver desabilitado */
        background-color: #bdbdbd; /* Define a cor de fundo como cinza claro (#bdbdbd) */
        color: #616161;          /* Define a cor do texto como cinza escuro (#616161) */
    }

    QLabel {  /* Aplica estilo a todos os rótulos (QLabel) */
        color: #333; /* Define a cor do texto como cinza escuro (#333) */
    }

    QLineEdit {  /* Aplica estilo a todos os campos de texto (QLineEdit) */
        border: 1px solid #ccc; /* Define uma borda sólida com 1 pixel de largura e cor cinza claro (#ccc) */
        padding: 5px;           /* Define um espaçamento interno (padding) de 5 pixels em todos os lados */
    }
"""