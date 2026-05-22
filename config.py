"""Configurações da aplicação"""
import os

# Diretório da aplicação
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Banco de dados
DB_PATH = os.path.join(DATA_DIR, "central_licitacoes.db")

# Configurações da UI
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
APP_TITLE = "Central de Licitações - ComprasNet"

# Temas CustomTkinter
APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"

# ComprasNet
COMPRASNET_URL = "https://www.comprasnet.gov.br"
COMPRASNET_LOGIN_URL = "https://www.comprasnet.gov.br/login"
COMPRASNET_HEADLESS = True  # Executar navegador em background
COMPRASNET_INTERVALO = 300  # 5 minutos entre buscas

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(LOGS_DIR, "app.log")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Alertas
TEMPO_VERIFICACAO_ALERTAS = 60  # segundos
MANTER_ALERTAS_LIDOS = 30  # dias

# Limites
MAX_TENTATIVAS_LOGIN = 3
TIMEOUT_SESSAO = 3600  # 1 hora
CACHE_LICITACOES = 1000  # máximo de licitações em cache

# Criar diretórios se não existirem
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
