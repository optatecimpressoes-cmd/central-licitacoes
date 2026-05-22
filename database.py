"""Gerenciamento do banco de dados SQLite"""
import sqlite3
import os
from config import DB_PATH
from datetime import datetime
import hashlib

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Inicializa o banco de dados com as tabelas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                email TEXT,
                nome TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de licitações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS licitacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT,
                orgao TEXT,
                modalidade TEXT,
                data_abertura DATE,
                data_encerramento DATE,
                valor_estimado REAL,
                status TEXT,
                usuario_id INTEGER,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Tabela de documentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                licitacao_id INTEGER NOT NULL,
                nome_arquivo TEXT,
                caminho TEXT,
                tipo TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (licitacao_id) REFERENCES licitacoes(id)
            )
        ''')
        
        # Tabela de palavras-chave para alertas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS palavras_chave (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                palavra TEXT NOT NULL,
                tipo TEXT,
                ativo INTEGER DEFAULT 1,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Tabela de alertas/notificações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                licitacao_id INTEGER,
                palavra_chave_id INTEGER,
                tipo_alerta TEXT,
                mensagem TEXT,
                lida INTEGER DEFAULT 0,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (licitacao_id) REFERENCES licitacoes(id),
                FOREIGN KEY (palavra_chave_id) REFERENCES palavras_chave(id)
            )
        ''')
        
        # Tabela para rastrear sincronizações com ComprasNet
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comprasnet_sync (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_sincronizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_licitacoes INTEGER,
                total_alertas INTEGER,
                status TEXT,
                mensagem TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def hash_senha(senha):
        """Cria hash da senha"""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def criar_usuario(self, username, senha, email, nome):
        """Cria um novo usuário"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (username, senha, email, nome)
                VALUES (?, ?, ?, ?)
            ''', (username, self.hash_senha(senha), email, nome))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def autenticar_usuario(self, username, senha):
        """Autentica um usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, nome FROM usuarios
            WHERE username = ? AND senha = ?
        ''', (username, self.hash_senha(senha)))
        usuario = cursor.fetchone()
        conn.close()
        return usuario
    
    def listar_licitacoes(self, filtro=None):
        """Lista todas as licitações com opção de filtro"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if filtro:
            query = '''
                SELECT * FROM licitacoes
                WHERE titulo LIKE ? OR numero LIKE ? OR orgao LIKE ?
                ORDER BY data_abertura DESC
            '''
            cursor.execute(query, (f'%{filtro}%', f'%{filtro}%', f'%{filtro}%'))
        else:
            cursor.execute('SELECT * FROM licitacoes ORDER BY data_abertura DESC')
        
        licitacoes = cursor.fetchall()
        conn.close()
        return licitacoes
    
    def obter_licitacao(self, licitacao_id):
        """Obtém uma licitação específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM licitacoes WHERE id = ?', (licitacao_id,))
        licitacao = cursor.fetchone()
        conn.close()
        return licitacao
    
    def criar_licitacao(self, numero, titulo, descricao, orgao, modalidade, 
                       data_abertura, data_encerramento, valor_estimado, usuario_id):
        """Cria uma nova licitação"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO licitacoes 
                (numero, titulo, descricao, orgao, modalidade, data_abertura, 
                 data_encerramento, valor_estimado, status, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (numero, titulo, descricao, orgao, modalidade, data_abertura,
                  data_encerramento, valor_estimado, 'Ativa', usuario_id))
            conn.commit()
            id_novo = cursor.lastrowid
            conn.close()
            return id_novo
        except sqlite3.IntegrityError:
            return None
    
    def atualizar_licitacao(self, licitacao_id, **kwargs):
        """Atualiza uma licitação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        campos = ', '.join([f'{k} = ?' for k in kwargs.keys()])
        valores = list(kwargs.values()) + [licitacao_id]
        
        cursor.execute(f'''
            UPDATE licitacoes
            SET {campos}, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', valores)
        
        conn.commit()
        conn.close()
    
    def deletar_licitacao(self, licitacao_id):
        """Deleta uma licitação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM licitacoes WHERE id = ?', (licitacao_id,))
        conn.commit()
        conn.close()
    
    def obter_estatisticas(self):
        """Obtém estatísticas do sistema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        cursor.execute('SELECT COUNT(*) as total FROM licitacoes')
        stats['total_licitacoes'] = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as ativas FROM licitacoes WHERE status = 'Ativa'")
        stats['licitacoes_ativas'] = cursor.fetchone()['ativas']
        
        cursor.execute('SELECT SUM(valor_estimado) as valor_total FROM licitacoes')
        stats['valor_total'] = cursor.fetchone()['valor_total'] or 0
        
        cursor.execute('SELECT COUNT(*) as usuarios FROM usuarios')
        stats['total_usuarios'] = cursor.fetchone()['usuarios']
        
        conn.close()
        return stats
    
    # ============ MÉTODOS PARA PALAVRAS-CHAVE ============
    
    def adicionar_palavra_chave(self, usuario_id, palavra, tipo="geral"):
        """Adiciona uma palavra-chave para monitoramento"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO palavras_chave (usuario_id, palavra, tipo, ativo)
                VALUES (?, ?, ?, 1)
            ''', (usuario_id, palavra.upper(), tipo))
            conn.commit()
            id_novo = cursor.lastrowid
            conn.close()
            return id_novo
        except sqlite3.IntegrityError:
            return None
    
    def listar_palavras_chave(self, usuario_id):
        """Lista todas as palavras-chave do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM palavras_chave
            WHERE usuario_id = ? AND ativo = 1
            ORDER BY criado_em DESC
        ''', (usuario_id,))
        palavras = cursor.fetchall()
        conn.close()
        return palavras
    
    def deletar_palavra_chave(self, palavra_id):
        """Deleta uma palavra-chave"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE palavras_chave SET ativo = 0 WHERE id = ?', (palavra_id,))
        conn.commit()
        conn.close()
    
    def obter_palavra_chave(self, palavra_id):
        """Obtém uma palavra-chave específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM palavras_chave WHERE id = ?', (palavra_id,))
        palavra = cursor.fetchone()
        conn.close()
        return palavra
    
    # ============ MÉTODOS PARA ALERTAS ============
    
    def criar_alerta(self, usuario_id, licitacao_id, palavra_chave_id, tipo_alerta, mensagem):
        """Cria um novo alerta/notificação"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO alertas 
                (usuario_id, licitacao_id, palavra_chave_id, tipo_alerta, mensagem, lida)
                VALUES (?, ?, ?, ?, ?, 0)
            ''', (usuario_id, licitacao_id, palavra_chave_id, tipo_alerta, mensagem))
            conn.commit()
            id_novo = cursor.lastrowid
            conn.close()
            return id_novo
        except Exception as e:
            print(f"Erro ao criar alerta: {e}")
            return None
    
    def listar_alertas(self, usuario_id, nao_lidos=False):
        """Lista alertas do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if nao_lidos:
            cursor.execute('''
                SELECT a.*, l.numero as licitacao_numero, l.titulo as licitacao_titulo,
                       p.palavra as palavra_chave
                FROM alertas a
                LEFT JOIN licitacoes l ON a.licitacao_id = l.id
                LEFT JOIN palavras_chave p ON a.palavra_chave_id = p.id
                WHERE a.usuario_id = ? AND a.lida = 0
                ORDER BY a.criado_em DESC
            ''', (usuario_id,))
        else:
            cursor.execute('''
                SELECT a.*, l.numero as licitacao_numero, l.titulo as licitacao_titulo,
                       p.palavra as palavra_chave
                FROM alertas a
                LEFT JOIN licitacoes l ON a.licitacao_id = l.id
                LEFT JOIN palavras_chave p ON a.palavra_chave_id = p.id
                WHERE a.usuario_id = ?
                ORDER BY a.criado_em DESC
            ''', (usuario_id,))
        
        alertas = cursor.fetchall()
        conn.close()
        return alertas
    
    def marcar_alerta_como_lido(self, alerta_id):
        """Marca um alerta como lido"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE alertas SET lida = 1 WHERE id = ?', (alerta_id,))
        conn.commit()
        conn.close()
    
    def contar_alertas_nao_lidos(self, usuario_id):
        """Conta alertas não lidos do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) as total FROM alertas
            WHERE usuario_id = ? AND lida = 0
        ''', (usuario_id,))
        total = cursor.fetchone()['total']
        conn.close()
        return total
    
    def verificar_palavras_chave_em_licitacao(self, usuario_id, licitacao_id):
        """Verifica se alguma palavra-chave aparece na licitação"""
        licitacao = self.obter_licitacao(licitacao_id)
        if not licitacao:
            return []
        
        # Combinando todos os campos de texto para buscar
        texto_licitacao = f"{licitacao['numero']} {licitacao['titulo']} {licitacao['descricao']} {licitacao['orgao']}".upper()
        
        palavras = self.listar_palavras_chave(usuario_id)
        matches = []
        
        for palavra in palavras:
            if palavra['palavra'] in texto_licitacao:
                matches.append(palavra)
        
        return matches
    
    # ============ MÉTODOS PARA COMPRASNET ============
    
    def criar_licitacao_comprasnet(self, numero, titulo, descricao, orgao, modalidade, 
                                   data_publicacao, url_comprasnet):
        """Cria uma licitação importada do ComprasNet"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO licitacoes 
                (numero, titulo, descricao, orgao, modalidade, data_abertura, 
                 valor_estimado, status, usuario_id, criado_em)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (numero, titulo, descricao, orgao, modalidade, data_publicacao, 0, 'Ativa', None))
            conn.commit()
            id_novo = cursor.lastrowid
            conn.close()
            return id_novo
        except sqlite3.IntegrityError:
            return None
    
    def verificar_licitacao_existente(self, numero):
        """Verifica se uma licitação já existe pelo número"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM licitacoes WHERE numero = ?', (numero,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado is not None
    
    def registrar_sincronizacao_comprasnet(self, total_licitacoes, total_alertas, status='Sucesso', mensagem=''):
        """Registra uma sincronização com ComprasNet"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO comprasnet_sync (total_licitacoes, total_alertas, status, mensagem)
                VALUES (?, ?, ?, ?)
            ''', (total_licitacoes, total_alertas, status, mensagem))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao registrar sincronização: {e}")
            return False
    
    def obter_ultimo_sync_comprasnet(self):
        """Obtém informações do último sync com ComprasNet"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM comprasnet_sync
            ORDER BY data_sincronizacao DESC
            LIMIT 1
        ''')
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    
    def obter_licitacoes_comprasnet(self):
        """Lista todas as licitações importadas do ComprasNet"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM licitacoes
            WHERE usuario_id IS NULL
            ORDER BY criado_em DESC
        ''')
        licitacoes = cursor.fetchall()
        conn.close()
        return licitacoes

# Instância global
db = Database()
