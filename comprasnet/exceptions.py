"""Exceções customizadas para ComprasNet"""

class ComprasNetException(Exception):
    """Exceção base para ComprasNet"""
    pass

class ComprasNetAuthError(ComprasNetException):
    """Erro de autenticação"""
    pass

class ComprasNetScraperError(ComprasNetException):
    """Erro no scraping"""
    pass

class ComprasNetSessionError(ComprasNetException):
    """Erro na sessão"""
    pass
