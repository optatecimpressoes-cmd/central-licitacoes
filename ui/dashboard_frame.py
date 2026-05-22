"""Tela do dashboard"""
import customtkinter as ctk
from database import db

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.criar_widgets()
    
    def criar_widgets(self):
        # Header
        frame_header = ctk.CTkFrame(self)
        frame_header.pack(fill="x", padx=20, pady=20)
        
        titulo = ctk.CTkLabel(
            frame_header,
            text="Dashboard",
            font=("Arial", 24, "bold")
        )
        titulo.pack(side="left")
        
        # Botões do lado direito
        frame_botoes_header = ctk.CTkFrame(frame_header, fg_color="transparent")
        frame_botoes_header.pack(side="right")
        
        # Botão de alertas com contador
        self.btn_alertas = ctk.CTkButton(
            frame_botoes_header,
            text="",
            command=lambda: self.controller.mostrar_frame("Alertas"),
            width=80,
            fg_color="#d97706"
        )
        self.btn_alertas.pack(side="right", padx=5)
        
        btn_logout = ctk.CTkButton(
            frame_botoes_header,
            text="Logout",
            command=self.fazer_logout,
            width=100,
            fg_color="red"
        )
        btn_logout.pack(side="right", padx=5)
        
        # Conteúdo principal
        frame_conteudo = ctk.CTkFrame(self)
        frame_conteudo.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Estatísticas
        self.criar_cards_estatisticas(frame_conteudo)
        
        # Ações rápidas
        self.criar_acoes_rapidas(frame_conteudo)
        
        # Atualizar contador de alertas
        self.atualizar_contador_alertas()
    
    def criar_cards_estatisticas(self, parent):
        frame_stats = ctk.CTkFrame(parent)
        frame_stats.pack(fill="x", pady=20)
        
        stats = db.obter_estatisticas()
        
        # Card 1: Total de Licitações
        card1 = ctk.CTkFrame(frame_stats, fg_color="#1f4788")
        card1.pack(side="left", fill="both", expand=True, padx=10)
        
        label1 = ctk.CTkLabel(
            card1,
            text=str(stats['total_licitacoes']),
            font=("Arial", 28, "bold"),
            text_color="white"
        )
        label1.pack(pady=15)
        
        label_desc1 = ctk.CTkLabel(
            card1,
            text="Total de Licitações",
            font=("Arial", 12),
            text_color="white"
        )
        label_desc1.pack(pady=10)
        
        # Card 2: Licitações Ativas
        card2 = ctk.CTkFrame(frame_stats, fg_color="#1f4788")
        card2.pack(side="left", fill="both", expand=True, padx=10)
        
        label2 = ctk.CTkLabel(
            card2,
            text=str(stats['licitacoes_ativas']),
            font=("Arial", 28, "bold"),
            text_color="white"
        )
        label2.pack(pady=15)
        
        label_desc2 = ctk.CTkLabel(
            card2,
            text="Licitações Ativas",
            font=("Arial", 12),
            text_color="white"
        )
        label_desc2.pack(pady=10)
        
        # Card 3: Valor Total
        card3 = ctk.CTkFrame(frame_stats, fg_color="#1f4788")
        card3.pack(side="left", fill="both", expand=True, padx=10)
        
        valor_formatado = f"R$ {stats['valor_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        label3 = ctk.CTkLabel(
            card3,
            text=valor_formatado,
            font=("Arial", 18, "bold"),
            text_color="white"
        )
        label3.pack(pady=15)
        
        label_desc3 = ctk.CTkLabel(
            card3,
            text="Valor Total",
            font=("Arial", 12),
            text_color="white"
        )
        label_desc3.pack(pady=10)
    
    def criar_acoes_rapidas(self, parent):
        frame_acoes = ctk.CTkFrame(parent)
        frame_acoes.pack(fill="both", expand=True, pady=20)
        
        titulo_acoes = ctk.CTkLabel(
            frame_acoes,
            text="Ações Rápidas",
            font=("Arial", 18, "bold")
        )
        titulo_acoes.pack(pady=10, anchor="w")
        
        frame_botoes = ctk.CTkFrame(frame_acoes, fg_color="transparent")
        frame_botoes.pack(fill="both", expand=True)
        
        btn_listar = ctk.CTkButton(
            frame_botoes,
            text="📋 Listar Licitações",
            command=lambda: self.controller.mostrar_frame("Licitacoes"),
            height=50
        )
        btn_listar.pack(fill="x", pady=10)
        
        btn_nova = ctk.CTkButton(
            frame_botoes,
            text="➕ Nova Licitação",
            command=lambda: self.controller.mostrar_frame("NovaLicitacao"),
            height=50
        )
        btn_nova.pack(fill="x", pady=10)
        
        btn_alertas = ctk.CTkButton(
            frame_botoes,
            text="🔔 Gerenciar Alertas e Notificações",
            command=lambda: self.controller.mostrar_frame("Alertas"),
            height=50,
            fg_color="#d97706"
        )
        btn_alertas.pack(fill="x", pady=10)
        
        btn_palavras = ctk.CTkButton(
            frame_botoes,
            text="⚙️ Configurar Palavras-Chave",
            command=lambda: self.controller.mostrar_frame("PalavrasChave"),
            height=50,
            fg_color="#059669"
        )
        btn_palavras.pack(fill="x", pady=10)
        
        btn_comprasnet = ctk.CTkButton(
            frame_botoes,
            text="🌐 Sincronizar ComprasNet",
            command=lambda: self.controller.mostrar_frame("ComprasNet"),
            height=50,
            fg_color="#1f4788"
        )
        btn_comprasnet.pack(fill="x", pady=10)
    
    def atualizar_contador_alertas(self):
        """Atualiza o contador de alertas não lidos"""
        if self.controller.usuario_logado is None:
            self.btn_alertas.configure(text="🔔")
            return
        
        usuario_id = self.controller.usuario_logado['id']
        nao_lidos = db.contar_alertas_nao_lidos(usuario_id)
        
        if nao_lidos > 0:
            texto = f"🔔 {nao_lidos}"
        else:
            texto = "🔔"
        
        self.btn_alertas.configure(text=texto)
    
    def fazer_logout(self):
        self.controller.usuario_logado = None
        self.controller.mostrar_frame("Login")
