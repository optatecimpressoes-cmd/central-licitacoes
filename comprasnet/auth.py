"""Autenticação no ComprasNet via Selenium"""
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from .exceptions import ComprasNetAuthError, ComprasNetSessionError

logger = logging.getLogger(__name__)

class ComprasNetAuth:
    """Gerencia autenticação no ComprasNet"""
    
    COMPRASNET_URL = "https://www.comprasnet.gov.br"
    LOGIN_URL = "https://www.comprasnet.gov.br/login"
    
    def __init__(self, headless=True):
        """
        Inicializa autenticação
        
        Args:
            headless: Executar navegador em modo headless
        """
        self.headless = headless
        self.driver = None
        self.session_active = False
        self.last_login_time = None
        
    def criar_driver(self):
        """Cria instância do Selenium WebDriver"""
        options = Options()
        
        if self.headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0")
        options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=options)
            logger.info("WebDriver Chrome iniciado")
            return True
        except Exception as e:
            logger.error(f"Erro ao iniciar WebDriver: {e}")
            raise ComprasNetAuthError(f"Falha ao iniciar navegador: {e}")
    
    def fazer_login(self, cpf, senha):
        """
        Realiza login no ComprasNet
        
        Args:
            cpf: CPF do usuário
            senha: Senha do usuário
            
        Returns:
            bool: Sucesso do login
            
        Raises:
            ComprasNetAuthError: Se falhar no login
        """
        if not self.driver:
            self.criar_driver()
        
        try:
            logger.info(f"Iniciando login para CPF: {cpf[:3]}***")
            
            # Acessar página de login
            self.driver.get(self.LOGIN_URL)
            time.sleep(2)
            
            # Preencher CPF
            wait = WebDriverWait(self.driver, 10)
            campo_cpf = wait.until(
                EC.presence_of_element_located((By.ID, "cpf"))
            )
            campo_cpf.clear()
            campo_cpf.send_keys(cpf)
            logger.debug("CPF preenchido")
            
            # Preencher Senha
            campo_senha = self.driver.find_element(By.ID, "senha")
            campo_senha.clear()
            campo_senha.send_keys(senha)
            logger.debug("Senha preenchida")
            
            # Clique em Login
            botao_login = self.driver.find_element(By.ID, "btnLogin")
            botao_login.click()
            
            # Aguardar carregamento
            time.sleep(3)
            
            # Verificar se login foi bem-sucedido
            if self.verificar_sessao():
                self.session_active = True
                self.last_login_time = time.time()
                logger.info("✅ Login bem-sucedido no ComprasNet")
                return True
            else:
                raise ComprasNetAuthError("Falha na autenticação - verifique credenciais")
                
        except ComprasNetAuthError:
            raise
        except Exception as e:
            logger.error(f"Erro ao fazer login: {e}")
            raise ComprasNetAuthError(f"Erro no login: {e}")
    
    def verificar_sessao(self):
        """
        Verifica se a sessão está ativa
        
        Returns:
            bool: Se a sessão está válida
        """
        try:
            if not self.driver:
                return False
            
            # Verificar se está na página de login (sessão expirada)
            if "login" in self.driver.current_url.lower():
                logger.warning("Sessão expirada - redirecionado para login")
                self.session_active = False
                return False
            
            # Tentar encontrar elemento que existe apenas quando logado
            try:
                self.driver.find_element(By.CLASS_NAME, "navbar-user")
                logger.info("✅ Sessão validada")
                return True
            except:
                logger.warning("Sessão inválida")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao verificar sessão: {e}")
            return False
    
    def renovar_sessao(self):
        """Renova a sessão se necessário"""
        if not self.session_active:
            logger.warning("Sessão inativa")
            return False
        
        try:
            # Fazer requisição para manter sessão ativa
            self.driver.get(self.COMPRASNET_URL)
            time.sleep(1)
            
            if self.verificar_sessao():
                logger.info("✅ Sessão renovada")
                self.last_login_time = time.time()
                return True
            else:
                logger.warning("Falha ao renovar sessão")
                self.session_active = False
                return False
                
        except Exception as e:
            logger.error(f"Erro ao renovar sessão: {e}")
            self.session_active = False
            return False
    
    def fechar(self):
        """Fecha o navegador e finaliza a sessão"""
        try:
            if self.driver:
                self.driver.quit()
                self.session_active = False
                logger.info("WebDriver fechado")
        except Exception as e:
            logger.error(f"Erro ao fechar WebDriver: {e}")
    
    def __del__(self):
        """Garante que o driver seja fechado"""
        self.fechar()
