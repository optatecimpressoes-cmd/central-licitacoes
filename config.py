"""Configurações da aplicação"""
import os

# Diretório da aplicação
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Banco de dados
DB_PATH = os.path.join(DATA_DIR, "central_licitacoes.db")

# Configurações da UI
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
APP_TITLE = "Central de Licitações"

# Temas CustomTkinter
APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"

# Criar diretórios se não existirem
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
