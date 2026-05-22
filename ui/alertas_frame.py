"""Telas de alertas e palavras-chave"""
import customtkinter as ctk
from database import db
from datetime import datetime

class AlertasFrame(ctk.CTkFrame):
    """Tela para visualizar alertas/notificações"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.alertas = []
        self.criar_widgets()
    
    def criar_widgets(self):
        # Header
        frame_header = ctk.CTkFrame(self)
        frame_header.pack(fill="x", padx=20, pady=20)
        
        titulo = ctk.CTkLabel(
            frame_header,
            text="🔔 Alertas e Notificações",
            font=("Arial", 24, "bold")
        )
        titulo.pack(side="left")
        
        btn_voltar = ctk.CTkButton(
            frame_header,
            text="← Voltar",
            command=lambda: self.controller.mostrar_frame("Dashboard"),
            width=100
        )
        btn_voltar.pack(side="right", padx=5)
        
        btn_palavras = ctk.CTkButton(
            frame_header,
            text="⚙️ Configurar",
            command=lambda: self.controller.mostrar_frame("PalavrasChave"),
            width=100
        )
        btn_palavras.pack(side="right", padx=5)
        
        # Abas
        frame_abas = ctk.CTkFrame(self)
        frame_abas.pack(fill="x", padx=20, pady=10)
        
        btn_nao_lidos = ctk.CTkButton(
            frame_abas,
            text="Não Lidos",
            command=self.mostrar_nao_lidos,
            width=120
        )
        btn_nao_lidos.pack(side="left", padx=5)
        
        btn_todos = ctk.CTkButton(
            frame_abas,
            text="Todos",
            command=self.mostrar_todos,
            width=120,
            fg_color="gray60"
        )
        btn_todos.pack(side="left", padx=5)
        
        # Lista de alertas
        frame_alertas = ctk.CTkFrame(self)
        frame_alertas.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.frame_scroll = ctk.CTkScrollableFrame(frame_alertas, fg_color="transparent")
        self.frame_scroll.pack(fill="both", expand=True)
        
        self.carregar_alertas(nao_lidos=True)
    
    def carregar_alertas(self, nao_lidos=False):
        """Carrega alertas do banco de dados"""
        # Limpar
        for widget in self.frame_scroll.winfo_children():
            widget.destroy()
        
        if self.controller.usuario_logado is None:
            return
        
        usuario_id = self.controller.usuario_logado['id']
        self.alertas = db.listar_alertas(usuario_id, nao_lidos=nao_lidos)
        
        if not self.alertas:
            label_vazio = ctk.CTkLabel(
                self.frame_scroll,
                text="Nenhum alerta" if not nao_lidos else "Nenhum alerta não lido",
                font=("Arial", 14),
                text_color="gray60"
            )
            label_vazio.pack(pady=40)
            return
        
        for alerta in self.alertas:
            self.criar_card_alerta(alerta)
    
    def criar_card_alerta(self, alerta):
        """Cria um card visual para o alerta"""
        cor_fundo = "#1f4788" if alerta['lida'] == 0 else "#2b2b2b"
        
        card = ctk.CTkFrame(self.frame_scroll, fg_color=cor_fundo)
        card.pack(fill="x", pady=10)
        
        # Conteúdo
        frame_conteudo = ctk.CTkFrame(card, fg_color="transparent")
        frame_conteudo.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Tipo de alerta e data
        tipo_icon = "🔍" if alerta['tipo_alerta'] == "mencao" else "📌"
        label_tipo = ctk.CTkLabel(
            frame_conteudo,
            text=f"{tipo_icon} {alerta['tipo_alerta'].upper()} - {alerta['criado_em'][:10]}",
            font=("Arial", 10),
            text_color="gray70"
        )
        label_tipo.pack(anchor="w", pady=2)
        
        # Licitação
        if alerta['licitacao_numero']:
            label_licitacao = ctk.CTkLabel(
                frame_conteudo,
                text=f"Licitação: {alerta['licitacao_numero']} - {alerta['licitacao_titulo'][:60]}",
                font=("Arial", 12, "bold")
            )
            label_licitacao.pack(anchor="w", pady=5)
        
        # Palavra-chave detectada
        if alerta['palavra_chave']:
            label_palavra = ctk.CTkLabel(
                frame_conteudo,
                text=f"Palavra-chave detectada: {alerta['palavra_chave']}",
                font=("Arial", 11),
                text_color="lightblue"
            )
            label_palavra.pack(anchor="w", pady=3)
        
        # Mensagem
        label_msg = ctk.CTkLabel(
            frame_conteudo,
            text=alerta['mensagem'],
            font=("Arial", 11),
            text_color="white"
        )
        label_msg.pack(anchor="w", pady=5, fill="x")
        
        # Botões
        frame_botoes = ctk.CTkFrame(card, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=15, pady=10)
        
        if alerta['lida'] == 0:
            btn_marcar_lido = ctk.CTkButton(
                frame_botoes,
                text="✓ Marcar como Lido",
                command=lambda: self.marcar_lido(alerta['id']),
                width=80,
                height=28
            )
            btn_marcar_lido.pack(side="left", padx=5)
        else:
            label_lido = ctk.CTkLabel(
                frame_botoes,
                text="✓ Lido",
                font=("Arial", 10),
                text_color="green"
            )
            label_lido.pack(side="left", padx=5)
    
    def marcar_lido(self, alerta_id):
        """Marca um alerta como lido"""
        db.marcar_alerta_como_lido(alerta_id)
        self.carregar_alertas(nao_lidos=True)
    
    def mostrar_nao_lidos(self):
        """Mostra apenas alertas não lidos"""
        self.carregar_alertas(nao_lidos=True)
    
    def mostrar_todos(self):
        """Mostra todos os alertas"""
        self.carregar_alertas(nao_lidos=False)


class PalavrasChaveFrame(ctk.CTkFrame):
    """Tela para gerenciar palavras-chave de monitoramento"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.palavras = []
        self.criar_widgets()
    
    def criar_widgets(self):
        # Header
        frame_header = ctk.CTkFrame(self)
        frame_header.pack(fill="x", padx=20, pady=20)
        
        titulo = ctk.CTkLabel(
            frame_header,
            text="⚙️ Gerenciar Palavras-Chave",
            font=("Arial", 24, "bold")
        )
        titulo.pack(side="left")
        
        btn_voltar = ctk.CTkButton(
            frame_header,
            text="← Voltar",
            command=lambda: self.controller.mostrar_frame("Alertas"),
            width=100
        )
        btn_voltar.pack(side="right")
        
        # Frame de adição
        frame_adicionar = ctk.CTkFrame(self)
        frame_adicionar.pack(fill="x", padx=20, pady=20)
        
        label_nova = ctk.CTkLabel(
            frame_adicionar,
            text="Adicionar Nova Palavra-Chave:",
            font=("Arial", 14, "bold")
        )
        label_nova.pack(anchor="w", pady=5)
        
        # Input
        frame_input = ctk.CTkFrame(frame_adicionar, fg_color="transparent")
        frame_input.pack(fill="x", pady=10)
        
        label_palavra = ctk.CTkLabel(frame_input, text="Palavra:", font=("Arial", 12))
        label_palavra.pack(side="left", padx=5)
        
        self.entry_palavra = ctk.CTkEntry(
            frame_input,
            placeholder_text="Ex: Razão Social ou CNPJ",
            width=300
        )
        self.entry_palavra.pack(side="left", padx=5)
        
        label_tipo = ctk.CTkLabel(frame_input, text="Tipo:", font=("Arial", 12))
        label_tipo.pack(side="left", padx=5)
        
        self.combo_tipo = ctk.CTkComboBox(
            frame_input,
            values=["Razão Social", "CNPJ", "Email", "Telefone", "Outro"],
            width=150
        )
        self.combo_tipo.set("Razão Social")
        self.combo_tipo.pack(side="left", padx=5)
        
        btn_adicionar = ctk.CTkButton(
            frame_input,
            text="+ Adicionar",
            command=self.adicionar_palavra,
            width=100
        )
        btn_adicionar.pack(side="left", padx=5)
        
        # Label de mensagem
        self.label_msg = ctk.CTkLabel(
            frame_adicionar,
            text="",
            font=("Arial", 11),
            text_color="green"
        )
        self.label_msg.pack(pady=5)
        
        # Divider
        divider = ctk.CTkFrame(self, height=2, fg_color="gray30")
        divider.pack(fill="x", padx=20, pady=10)
        
        # Lista de palavras
        frame_lista = ctk.CTkFrame(self)
        frame_lista.pack(fill="both", expand=True, padx=20, pady=20)
        
        label_lista = ctk.CTkLabel(
            frame_lista,
            text="Suas Palavras-Chave Monitoradas:",
            font=("Arial", 14, "bold")
        )
        label_lista.pack(anchor="w", pady=5)
        
        self.frame_scroll = ctk.CTkScrollableFrame(frame_lista, fg_color="transparent")
        self.frame_scroll.pack(fill="both", expand=True)
        
        self.carregar_palavras()
    
    def carregar_palavras(self):
        """Carrega palavras-chave do banco de dados"""
        # Limpar
        for widget in self.frame_scroll.winfo_children():
            widget.destroy()
        
        if self.controller.usuario_logado is None:
            return
        
        usuario_id = self.controller.usuario_logado['id']
        self.palavras = db.listar_palavras_chave(usuario_id)
        
        if not self.palavras:
            label_vazio = ctk.CTkLabel(
                self.frame_scroll,
                text="Nenhuma palavra-chave adicionada ainda.\nAdicione uma para começar a monitorar!",
                font=("Arial", 13),
                text_color="gray60"
            )
            label_vazio.pack(pady=40)
            return
        
        for palavra in self.palavras:
            self.criar_card_palavra(palavra)
    
    def criar_card_palavra(self, palavra):
        """Cria um card para cada palavra-chave"""
        card = ctk.CTkFrame(self.frame_scroll, fg_color="#2b2b2b")
        card.pack(fill="x", pady=8)
        
        # Conteúdo
        frame_conteudo = ctk.CTkFrame(card, fg_color="transparent")
        frame_conteudo.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Palavra
        label_palavra = ctk.CTkLabel(
            frame_conteudo,
            text=f"🔑 {palavra['palavra']}",
            font=("Arial", 13, "bold"),
            text_color="lightblue"
        )
        label_palavra.pack(anchor="w", pady=2)
        
        # Tipo e data
        info_text = f"Tipo: {palavra['tipo']} | Adicionado em: {palavra['criado_em'][:10]}"
        label_info = ctk.CTkLabel(
            frame_conteudo,
            text=info_text,
            font=("Arial", 10),
            text_color="gray70"
        )
        label_info.pack(anchor="w", pady=2)
        
        # Botão deletar
        frame_botoes = ctk.CTkFrame(card, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=15, pady=10)
        
        btn_deletar = ctk.CTkButton(
            frame_botoes,
            text="🗑️ Remover",
            command=lambda: self.remover_palavra(palavra['id']),
            width=100,
            height=28,
            fg_color="red"
        )
        btn_deletar.pack(side="left")
    
    def adicionar_palavra(self):
        """Adiciona uma nova palavra-chave"""
        palavra = self.entry_palavra.get().strip()
        tipo = self.combo_tipo.get()
        
        if not palavra:
            self.label_msg.configure(
                text="Digite uma palavra-chave",
                text_color="red"
            )
            return
        
        if self.controller.usuario_logado is None:
            self.label_msg.configure(
                text="Você precisa estar logado",
                text_color="red"
            )
            return
        
        usuario_id = self.controller.usuario_logado['id']
        resultado = db.adicionar_palavra_chave(usuario_id, palavra, tipo)
        
        if resultado:
            self.label_msg.configure(
                text=f"✓ Palavra-chave '{palavra}' adicionada com sucesso!",
                text_color="green"
            )
            self.entry_palavra.delete(0, "end")
            self.combo_tipo.set("Razão Social")
            self.after(1500, self.label_msg.configure, {"text": ""})
            self.carregar_palavras()
        else:
            self.label_msg.configure(
                text="Erro ao adicionar palavra-chave",
                text_color="red"
            )
    
    def remover_palavra(self, palavra_id):
        """Remove uma palavra-chave"""
        db.deletar_palavra_chave(palavra_id)
        self.carregar_palavras()
