"""Web Scraping de licitações do ComprasNet"""
import logging
import re
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

logger = logging.getLogger(__name__)

class ComprasNetScraper:
    """Realiza scraping de licitações no ComprasNet"""
    
    def __init__(self, driver):
        """
        Inicializa scraper
        
        Args:
            driver: WebDriver do Selenium
        """
        self.driver = driver
        self.licitacoes_cache = {}
    
    def buscar_licitacoes(self, palavras_chave=None, filtros=None):
        """
        Busca licitações no ComprasNet
        
        Args:
            palavras_chave: Lista de palavras-chave para buscar
            filtros: Dicionário com filtros adicionais
            
        Returns:
            list: Lista de licitações encontradas
        """
        try:
            licitacoes = []
            
            if palavras_chave:
                for palavra in palavras_chave:
                    logger.info(f"🔍 Buscando por: {palavra}")
                    resultados = self._buscar_por_palavra(palavra, filtros)
                    licitacoes.extend(resultados)
            else:
                # Buscar todas as licitações
                logger.info("📋 Buscando todas as licitações")
                licitacoes = self._buscar_todas()
            
            logger.info(f"✅ Encontradas {len(licitacoes)} licitações")
            return licitacoes
            
        except Exception as e:
            logger.error(f"Erro ao buscar licitações: {e}")
            return []
    
    def _buscar_por_palavra(self, palavra_chave, filtros=None):
        """Busca licitações por palavra-chave"""
        try:
            # Acessar página de busca
            busca_url = "https://www.comprasnet.gov.br/listacompra"
            self.driver.get(busca_url)
            time.sleep(2)
            
            # Preencher campo de busca
            try:
                campo_busca = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "txt_busca"))
                )
                campo_busca.clear()
                campo_busca.send_keys(palavra_chave)
                
                # Submeter busca
                campo_busca.submit()
                time.sleep(3)
            except Exception as e:
                logger.warning(f"Erro ao preencher busca: {e}")
                return []
            
            # Extrair licitações
            return self._extrair_licitacoes_pagina()
            
        except Exception as e:
            logger.error(f"Erro ao buscar por palavra: {e}")
            return []
    
    def _buscar_todas(self):
        """Busca todas as licitações"""
        try:
            self.driver.get("https://www.comprasnet.gov.br/listacompra")
            time.sleep(2)
            return self._extrair_licitacoes_pagina()
        except Exception as e:
            logger.error(f"Erro ao buscar todas: {e}")
            return []
    
    def _extrair_licitacoes_pagina(self):
        """Extrai licitações da página atual"""
        try:
            licitacoes = []
            
            # Aguardar carregamento da tabela
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
            )
            
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Encontrar tabela de resultados
            tabela = soup.find('table', class_='tabela-resultado')
            
            if not tabela:
                logger.warning("Tabela de resultados não encontrada")
                return licitacoes
            
            # Iterar sobre linhas
            for linha in tabela.find_all('tr')[1:]:  # Pular header
                try:
                    colunas = linha.find_all('td')
                    
                    if len(colunas) < 5:
                        continue
                    
                    # Extrair dados
                    licitacao = {
                        'id': colunas[0].text.strip(),
                        'numero': colunas[1].text.strip(),
                        'orgao': colunas[2].text.strip(),
                        'objeto': colunas[3].text.strip(),
                        'data_abertura': colunas[4].text.strip(),
                        'status': colunas[5].text.strip() if len(colunas) > 5 else 'Ativa',
                        'url': self._extrair_url_licitacao(linha),
                        'data_extracao': datetime.now().isoformat(),
                    }
                    
                    # Verificar se é nova
                    if licitacao['id'] not in self.licitacoes_cache:
                        licitacoes.append(licitacao)
                        self.licitacoes_cache[licitacao['id']] = licitacao
                        logger.debug(f"✨ Licitação nova: {licitacao['numero']}")
                    
                except Exception as e:
                    logger.debug(f"Erro ao extrair linha: {e}")
                    continue
            
            return licitacoes
            
        except Exception as e:
            logger.error(f"Erro ao extrair licitações: {e}")
            return []
    
    def _extrair_url_licitacao(self, linha):
        """Extrai URL da licitação"""
        try:
            link = linha.find('a', href=True)
            if link:
                return link.get('href', '')
        except:
            pass
        return ''
    
    def obter_detalhes_licitacao(self, url):
        """
        Obtém detalhes completos de uma licitação
        
        Args:
            url: URL da licitação
            
        Returns:
            dict: Detalhes da licitação
        """
        try:
            self.driver.get(url)
            time.sleep(2)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            detalhes = {
                'descricao': self._extrair_texto(soup, 'descricao'),
                'valor': self._extrair_valor(soup),
                'documentos': self._extrair_documentos(soup),
                'datas': self._extrair_datas(soup),
            }
            
            return detalhes
            
        except Exception as e:
            logger.error(f"Erro ao obter detalhes: {e}")
            return {}
    
    def _extrair_texto(self, soup, classe):
        """Extrai texto de elemento"""
        try:
            elemento = soup.find(class_=classe)
            return elemento.get_text(strip=True) if elemento else ''
        except:
            return ''
    
    def _extrair_valor(self, soup):
        """Extrai valor da licitação"""
        try:
            valor_elem = soup.find(class_='valor-licitacao')
            if valor_elem:
                texto = valor_elem.get_text(strip=True)
                # Extrair número
                match = re.search(r'[\d.,]+', texto)
                return match.group(0) if match else ''
        except:
            pass
        return ''
    
    def _extrair_documentos(self, soup):
        """Extrai documentos da licitação"""
        documentos = []
        try:
            secao_docs = soup.find(class_='documentos')
            if secao_docs:
                for link in secao_docs.find_all('a'):
                    documentos.append({
                        'nome': link.get_text(strip=True),
                        'url': link.get('href', ''),
                    })
        except:
            pass
        return documentos
    
    def _extrair_datas(self, soup):
        """Extrai datas importantes da licitação"""
        datas = {}
        try:
            for campo in ['abertura', 'encerramento', 'julgamento']:
                elem = soup.find(class_=f'data-{campo}')
                if elem:
                    datas[campo] = elem.get_text(strip=True)
        except:
            pass
        return datas
