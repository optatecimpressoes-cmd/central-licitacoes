"""Serviço de Notificações e Processamento de Alertas"""
from database import db

class NotificationService:
    """Serviço para gerenciar notificações e alertas de palavras-chave"""
    
    @staticmethod
    def processar_nova_licitacao(licitacao_id):
        """
        Quando uma licitação é criada, verifica todas as palavras-chave 
        de todos os usuários e cria alertas se houver correspondência
        """
        licitacao = db.obter_licitacao(licitacao_id)
        if not licitacao:
            return False
        
        # Combinar todos os campos de texto da licitação
        texto_licitacao = f"{licitacao['numero']} {licitacao['titulo']} {licitacao['descricao']} {licitacao['orgao']}".upper()
        
        # Buscar todas as palavras-chave do sistema (de todos os usuários)
        # Para isso, precisamos de uma função que retorne todas
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, usuario_id, palavra FROM palavras_chave
            WHERE ativo = 1
        ''')
        todas_palavras = cursor.fetchall()
        conn.close()
        
        alertas_criados = 0
        
        # Verificar cada palavra-chave
        for palavra_obj in todas_palavras:
            palavra_id = palavra_obj['id']
            usuario_id = palavra_obj['usuario_id']
            palavra = palavra_obj['palavra']
            
            # Verificar se a palavra está no texto da licitação
            if palavra in texto_licitacao:
                # Criar alerta para o usuário
                mensagem = f"A palavra-chave '{palavra}' foi encontrada na licitação {licitacao['numero']}"
                
                db.criar_alerta(
                    usuario_id=usuario_id,
                    licitacao_id=licitacao_id,
                    palavra_chave_id=palavra_id,
                    tipo_alerta="mencao",
                    mensagem=mensagem
                )
                alertas_criados += 1
        
        return alertas_criados > 0
    
    @staticmethod
    def processar_atualizacao_licitacao(licitacao_id):
        """
        Quando uma licitação é atualizada, verifica novamente as palavras-chave
        (funcionalidade futura para monitoramento contínuo)
        """
        return NotificationService.processar_nova_licitacao(licitacao_id)
    
    @staticmethod
    def criar_alerta_manual(usuario_id, titulo, mensagem, tipo="notificacao"):
        """Cria um alerta manual para notificações gerais"""
        return db.criar_alerta(
            usuario_id=usuario_id,
            licitacao_id=None,
            palavra_chave_id=None,
            tipo_alerta=tipo,
            mensagem=mensagem
        )
    
    @staticmethod
    def verificar_palavra_chave_em_licitacao(usuario_id, licitacao_id):
        """
        Verifica se alguma palavra-chave do usuário está em uma licitação específica
        Retorna lista de palavras encontradas
        """
        palavras_encontradas = []
        
        licitacao = db.obter_licitacao(licitacao_id)
        if not licitacao:
            return palavras_encontradas
        
        # Combinar texto
        texto_licitacao = f"{licitacao['numero']} {licitacao['titulo']} {licitacao['descricao']} {licitacao['orgao']}".upper()
        
        # Buscar palavras do usuário
        palavras_usuario = db.listar_palavras_chave(usuario_id)
        
        for palavra_obj in palavras_usuario:
            if palavra_obj['palavra'] in texto_licitacao:
                palavras_encontradas.append(palavra_obj)
        
        return palavras_encontradas
    
    @staticmethod
    def gerar_relatorio_alertas(usuario_id, filtro_tipo=None):
        """
        Gera um relatório de alertas do usuário
        Útil para análises e estatísticas
        """
        alertas = db.listar_alertas(usuario_id, nao_lidos=False)
        
        if filtro_tipo:
            alertas = [a for a in alertas if a['tipo_alerta'] == filtro_tipo]
        
        relatorio = {
            'total': len(alertas),
            'nao_lidos': sum(1 for a in alertas if a['lida'] == 0),
            'lidos': sum(1 for a in alertas if a['lida'] == 1),
            'por_tipo': {},
            'alertas': alertas
        }
        
        # Contar por tipo
        for alerta in alertas:
            tipo = alerta['tipo_alerta']
            if tipo not in relatorio['por_tipo']:
                relatorio['por_tipo'][tipo] = 0
            relatorio['por_tipo'][tipo] += 1
        
        return relatorio
