"""Integração com ComprasNet - Portal de Licitações do Governo Federal"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from database import db
import re

class ComprasNetService:
    """Serviço para integração com o ComprasNet"""
    
    # URLs do ComprasNet
    BASE_URL = "https://www.comprasnet.gov.br"
    LICITACOES_URL = "https://www.comprasnet.gov.br/snlc/consulta/consultarEdital.do"
    AVISOS_URL = "https://www.comprasnet.gov.br/snlc/consulta/avisoEdital.do"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.licitacoes_cache = {}
    
    def conectar_comprasnet(self):
        """Testa conexão com ComprasNet"""
        try:
            response = self.session.get(self.BASE_URL, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Erro ao conectar ComprasNet: {e}")
            return False
    
    def buscar_licitacoes_ativas(self, filtros=None):
        """
        Busca licitações ativas no ComprasNet
        
        Parâmetros opcionais:
        - modalidade: 'Pregão', 'Concorrência', etc.
        - orgao: nome do órgão
        - palavras_chave: termos para buscar
        """
        try:
            # Parâmetros padrão para busca
            params = {
                'agrupadores': 'UASG',
                'hitsPorPagina': 50
            }
            
            if filtros:
                if 'orgao' in filtros:
                    params['UASG'] = filtros['orgao']
                if 'modalidade' in filtros:
                    params['modalidade'] = filtros['modalidade']
            
            response = self.session.get(self.LICITACOES_URL, params=params, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                licitacoes = self._extrair_licitacoes(response.text)
                return licitacoes
            else:
                print(f"Erro na requisição: {response.status_code}")
                return []
        
        except Exception as e:
            print(f"Erro ao buscar licitações: {e}")
            return []
    
    def buscar_avisos_recentes(self):
        """Busca avisos de licitações recentes (últimos 7 dias)"""
        try:
            response = self.session.get(self.AVISOS_URL, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                avisos = self._extrair_avisos(response.text)
                return avisos
            else:
                return []
        
        except Exception as e:
            print(f"Erro ao buscar avisos: {e}")
            return []
    
    def _extrair_licitacoes(self, html):
        """Extrai dados de licitações do HTML do ComprasNet"""
        licitacoes = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Procurar por elementos com informações de licitações
            # O ComprasNet usa tabelas para exibir dados
            tabelas = soup.find_all('table')
            
            for tabela in tabelas:
                linhas = tabela.find_all('tr')
                
                for linha in linhas[1:]:  # Pular header
                    colunas = linha.find_all('td')
                    
                    if len(colunas) >= 4:
                        try:
                            numero = colunas[0].text.strip()
                            titulo = colunas[1].text.strip()
                            orgao = colunas[2].text.strip()
                            data = colunas[3].text.strip()
                            
                            if numero and titulo:
                                licitacao = {
                                    'numero': numero,
                                    'titulo': titulo,
                                    'orgao': orgao,
                                    'data_publicacao': data,
                                    'url_comprasnet': self._extrair_url_licitacao(linha),
                                    'fonte': 'ComprasNet'
                                }
                                licitacoes.append(licitacao)
                        except Exception as e:
                            print(f"Erro ao extrair linha: {e}")
                            continue
        
        except Exception as e:
            print(f"Erro ao fazer parsing: {e}")
        
        return licitacoes
    
    def _extrair_avisos(self, html):
        """Extrai avisos de licitações"""
        avisos = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Procurar por links ou elementos com avisos
            links = soup.find_all('a', class_=re.compile('.*aviso.*', re.I))
            
            for link in links:
                titulo = link.text.strip()
                url = link.get('href', '')
                
                if titulo and url:
                    aviso = {
                        'titulo': titulo,
                        'url': url,
                        'data': datetime.now().strftime('%Y-%m-%d'),
                        'fonte': 'ComprasNet'
                    }
                    avisos.append(aviso)
        
        except Exception as e:
            print(f"Erro ao extrair avisos: {e}")
        
        return avisos
    
    def _extrair_url_licitacao(self, elemento_linha):
        """Extrai URL da licitação do elemento da linha"""
        try:
            link = elemento_linha.find('a')
            if link:
                return link.get('href', '')
        except:
            pass
        return None
    
    def obter_detalhes_licitacao(self, url_licitacao):
        """Obtém detalhes completos de uma licitação do ComprasNet"""
        try:
            response = self.session.get(url_licitacao, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                detalhes = self._extrair_detalhes(response.text)
                return detalhes
            else:
                return None
        
        except Exception as e:
            print(f"Erro ao obter detalhes: {e}")
            return None
    
    def _extrair_detalhes(self, html):
        """Extrai detalhes da licitação do HTML"""
        detalhes = {
            'descricao': '',
            'objeto': '',
            'valor_estimado': '',
            'modalidade': '',
            'data_abertura': '',
            'data_encerramento': ''
        }
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Procurar por campos específicos
            campo_obj = soup.find(text=re.compile('Objeto|objeto'))
            if campo_obj:
                pai = campo_obj.parent
                detalhes['objeto'] = pai.next_sibling.text.strip() if pai.next_sibling else ''
            
            campo_valor = soup.find(text=re.compile('Valor|valor|Estimado'))
            if campo_valor:
                pai = campo_valor.parent
                detalhes['valor_estimado'] = pai.next_sibling.text.strip() if pai.next_sibling else ''
            
            campo_modal = soup.find(text=re.compile('Modalidade|modalidade'))
            if campo_modal:
                pai = campo_modal.parent
                detalhes['modalidade'] = pai.next_sibling.text.strip() if pai.next_sibling else ''
        
        except Exception as e:
            print(f"Erro ao extrair detalhes: {e}")
        
        return detalhes
    
    def sincronizar_licitacoes_comprasnet(self):
        """
        Sincroniza licitações do ComprasNet com o banco de dados
        Verifica palavras-chave de todos os usuários
        """
        try:
            # Buscar licitações ativas
            licitacoes = self.buscar_licitacoes_ativas()
            
            if not licitacoes:
                print("Nenhuma licitação encontrada no ComprasNet")
                return False
            
            alertas_criados = 0
            
            # Para cada licitação do ComprasNet
            for lic in licitacoes:
                # Verificar se já existe no banco
                numero_existente = db.verificar_licitacao_existente(lic['numero'])
                
                if not numero_existente:
                    # Adicionar à base local
                    id_novo = db.criar_licitacao_comprasnet(
                        numero=lic['numero'],
                        titulo=lic['titulo'],
                        descricao=lic.get('objeto', ''),
                        orgao=lic['orgao'],
                        modalidade=lic.get('modalidade', 'Não especificada'),
                        data_publicacao=lic.get('data_publicacao', ''),
                        url_comprasnet=lic.get('url_comprasnet', '')
                    )
                    
                    if id_novo:
                        # Buscar todas as palavras-chave e criar alertas
                        alertas = self._verificar_palavras_chave_em_licitacao(id_novo, lic)
                        alertas_criados += len(alertas)
            
            return alertas_criados > 0
        
        except Exception as e:
            print(f"Erro ao sincronizar: {e}")
            return False
    
    def _verificar_palavras_chave_em_licitacao(self, licitacao_id, licitacao_dados):
        """Verifica palavras-chave em uma licitação e cria alertas"""
        alertas_criados = 0
        
        # Combinar texto para busca
        texto_licitacao = f"{licitacao_dados['numero']} {licitacao_dados['titulo']} {licitacao_dados.get('objeto', '')} {licitacao_dados['orgao']}".upper()
        
        # Buscar todas as palavras-chave do sistema
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, usuario_id, palavra FROM palavras_chave WHERE ativo = 1')
        todas_palavras = cursor.fetchall()
        conn.close()
        
        # Verificar cada palavra-chave
        for palavra_obj in todas_palavras:
            if palavra_obj['palavra'] in texto_licitacao:
                mensagem = f"Licitação encontrada no ComprasNet: {licitacao_dados['numero']} - {licitacao_dados['titulo']}"
                
                db.criar_alerta(
                    usuario_id=palavra_obj['usuario_id'],
                    licitacao_id=licitacao_id,
                    palavra_chave_id=palavra_obj['id'],
                    tipo_alerta="comprasnet",
                    mensagem=mensagem
                )
                alertas_criados += 1
        
        return alertas_criados
    
    def obter_estatisticas_comprasnet(self):
        """Obtém estatísticas do ComprasNet"""
        try:
            licitacoes = self.buscar_licitacoes_ativas()
            
            stats = {
                'total_licitacoes': len(licitacoes),
                'ultima_atualizacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status_conexao': 'Conectado' if licitacoes else 'Sem dados'
            }
            
            return stats
        
        except Exception as e:
            return {
                'total_licitacoes': 0,
                'ultima_atualizacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status_conexao': 'Erro'
            }


# Instância global
comprasnet_service = ComprasNetService()
