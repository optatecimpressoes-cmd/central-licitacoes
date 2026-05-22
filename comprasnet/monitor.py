"""Monitor contínuo de licitações em thread separada"""
import threading
import time
import logging
from queue import Queue
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ComprasNetMonitor(threading.Thread):
    """Monitor de licitações em background"""
    
    def __init__(self, auth, scraper, db, callback=None, intervalo=300):
        """
        Inicializa monitor
        
        Args:
            auth: Instância de ComprasNetAuth
            scraper: Instância de ComprasNetScraper
            db: Instância do banco de dados
            callback: Função para chamar quando encontrar licitação nova
            intervalo: Intervalo entre buscas em segundos (default 5 min)
        """
        super().__init__(daemon=True)
        
        self.auth = auth
        self.scraper = scraper
        self.db = db
        self.callback = callback
        self.intervalo = intervalo
        
        self.rodando = False
        self.pausado = False
        self.queue = Queue()
        
        self.licitacoes_conhecidas = set()
        self.ultima_busca = None
        self.proxima_busca = None
        
    def run(self):
        """Loop principal do monitor"""
        logger.info("🚀 Monitor de ComprasNet iniciado")
        self.rodando = True
        
        try:
            while self.rodando:
                # Processar comandos da fila
                self._processar_fila()
                
                # Se pausado, aguardar
                if self.pausado:
                    time.sleep(1)
                    continue
                
                # Verificar se é hora de buscar
                agora = datetime.now()
                if self.proxima_busca is None or agora >= self.proxima_busca:
                    self._executar_busca()
                    self.proxima_busca = agora + timedelta(seconds=self.intervalo)
                
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Erro no monitor: {e}")
        finally:
            self._limpar()
    
    def _processar_fila(self):
        """Processa comandos da fila"""
        while not self.queue.empty():
            try:
                comando, args = self.queue.get_nowait()
                
                if comando == 'parar':
                    self.rodando = False
                    logger.info("⏹️ Monitor parado")
                
                elif comando == 'pausar':
                    self.pausado = args.get('status', True)
                    status_txt = "⏸️ pausado" if self.pausado else "▶️ retomado"
                    logger.info(f"Monitor {status_txt}")
                
                elif comando == 'intervalo':
                    self.intervalo = args.get('intervalo', 300)
                    logger.info(f"Intervalo alterado para {self.intervalo}s")
                
                elif comando == 'buscar':
                    self._executar_busca()
                
            except Exception as e:
                logger.error(f"Erro ao processar comando: {e}")
    
    def _executar_busca(self):
        """Executa busca de licitações"""
        try:
            logger.info("🔍 Iniciando busca de licitações...")
            
            # Verificar sessão
            if not self.auth.verificar_sessao():
                logger.warning("⚠️ Sessão inativa - renovando...")
                if not self.auth.renovar_sessao():
                    logger.error("❌ Falha ao renovar sessão")
                    return
            
            # Obter palavras-chave do banco
            palavras = self._obter_palavras_chave()
            
            if not palavras:
                logger.warning("Nenhuma palavra-chave configurada")
                return
            
            # Realizar busca
            licitacoes = self.scraper.buscar_licitacoes(palavras_chave=palavras)
            
            # Processar novas licitações
            novas = 0
            for lic in licitacoes:
                if lic['id'] not in self.licitacoes_conhecidas:
                    novas += 1
                    self.licitacoes_conhecidas.add(lic['id'])
                    
                    # Salvar no banco
                    self._salvar_licitacao(lic)
                    
                    # Chamar callback
                    if self.callback:
                        self.callback(lic)
                    
                    logger.info(f"✨ Nova licitação: {lic['numero']}")
            
            self.ultima_busca = datetime.now()
            logger.info(f"✅ Busca concluída - {novas} novos registros")
            
        except Exception as e:
            logger.error(f"Erro ao executar busca: {e}")
    
    def _obter_palavras_chave(self):
        """Obtém palavras-chave do banco de dados"""
        try:
            # Implementação depende da estrutura do seu banco
            # Exemplo:
            palavras = self.db.obter_palavras_chave_ativas()
            return [p['palavra'] for p in palavras] if palavras else []
        except Exception as e:
            logger.error(f"Erro ao obter palavras-chave: {e}")
            return []
    
    def _salvar_licitacao(self, licitacao):
        """Salva licitação no banco de dados"""
        try:
            self.db.salvar_licitacao(licitacao)
        except Exception as e:
            logger.error(f"Erro ao salvar licitação: {e}")
    
    def _limpar(self):
        """Limpeza ao finalizar"""
        try:
            self.auth.fechar()
            logger.info("🧹 Monitor finalizado e limpo")
        except Exception as e:
            logger.error(f"Erro ao limpar: {e}")
    
    # Métodos de controle
    
    def parar(self):
        """Para o monitor"""
        self.queue.put(('parar', {}))
    
    def pausar(self):
        """Pausa o monitor"""
        self.queue.put(('pausar', {'status': True}))
    
    def retomar(self):
        """Retoma o monitor"""
        self.queue.put(('pausar', {'status': False}))
    
    def alterar_intervalo(self, segundos):
        """Altera intervalo entre buscas"""
        self.queue.put(('intervalo', {'intervalo': segundos}))
    
    def forcar_busca(self):
        """Força uma busca imediatamente"""
        self.queue.put(('buscar', {}))
    
    def obter_status(self):
        """Retorna status do monitor"""
        return {
            'rodando': self.rodando,
            'pausado': self.pausado,
            'intervalo': self.intervalo,
            'ultima_busca': self.ultima_busca.isoformat() if self.ultima_busca else None,
            'proxima_busca': self.proxima_busca.isoformat() if self.proxima_busca else None,
            'licitacoes_conhecidas': len(self.licitacoes_conhecidas),
        }
