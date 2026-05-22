"""
Módulo de Integração ComprasNet
Gerencia login, scraping e monitoramento de licitações
"""

from .auth import ComprasNetAuth
from .scraper import ComprasNetScraper
from .monitor import ComprasNetMonitor

__all__ = ['ComprasNetAuth', 'ComprasNetScraper', 'ComprasNetMonitor']
