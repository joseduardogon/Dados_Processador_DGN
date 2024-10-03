# styles.py
# Define a stylesheet para a aplicação

STYLESHEET = """
    QMainWindow {
        color: yellow;
    }
    
    QWidget { /* Aplica estilo a todos os widgets */
        font-family: Arial;  /* Define a fonte como Arial para todos os widgets */
        font-size: 12pt;   /* Define o tamanho da fonte como 12 pontos para todos os widgets */
    }

    QPushButton {  /* Aplica estilo a todos os botões (QPushButton) */
        border: none;       /* Remove a borda padrão dos botões */
        padding: 10px 20px;  /* Define espaçamento interno (padding) dos botões: 10px acima/abaixo, 20px esquerda/direita */
        border-radius: 5px;  /* Define o raio das bordas dos botões para 5 pixels (arredondamento) */
        color: green;
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
        background-color: white;   /* Cor de fundo branca */
        color: #333;                /* Cor do texto cinza escuro */
        font-family: Arial;          /* Fonte Arial */
        font-size: 14px;            /* Tamanho da fonte 14 pixels */
        border: 2px solid #007BFF;  /* Borda sólida azul com 2 pixels de largura */
        border-radius: 8px;         /* Borda arredondada com raio de 8 pixels */
        padding: 8px;               /* Espaçamento interno de 8 pixels */
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Sombra suave */
    }
    
    QMenuBar {
        background-color: #f0f0f0; /* Cor de fundo da barra de menus */
    }

    QMenuBar::item { /* Estilos dos itens de menu (Arquivo, Configurações) */
        spacing: 30px; /* Espaçamento entre os menus */
        padding: 5px 10px;
        background: transparent; /* Fundo transparente para os menus */
        border-radius: 5px;
    }

    QMenuBar::item:selected { /* Estilo quando o menu está selecionado */
        background-color: #ddd;  /* Cor de fundo cinza claro */
    }

    QMenuBar::item:pressed {  /* Estilo quando o menu é pressionado */
        background: #ccc;       /* Cor de fundo cinza mais escuro */
    }
    
    QTabWidget::pane { /* O painel que contém as abas */
        border: 1px solid #ccc; 
        border-top: none; /* Remove a borda superior */
        background-color: #fff; 
    }

    QTabWidget::tab-bar { /* A barra que contém os nomes das abas */
        alignment: center; /* Centraliza as abas */
    }

    QTabWidget::tab { /* Estilo para cada aba */
        background: #eee; /* Cinza claro */
        border: 1px solid #ccc;
        border-bottom-left-radius: 4px; 
        border-bottom-right-radius: 4px; 
        padding: 5px 10px;
        min-width: 80px; 
    }

    QTabWidget::tab:selected, QTabWidget::tab:hover {  /* Aba selecionada ou com mouse sobre */
        background: #ddd; /* Cinza mais escuro */
        font-weight: bold; 
    }
    
    QTableWidget::item:selected { /* Célula selecionada */
        background-color: #007BFF;  /* Azul */
        color: white; 
    }

    QTableWidget::item:hover { /* Célula com mouse sobre */
        background-color: #cce0ff;  /* Azul claro */
    }
"""