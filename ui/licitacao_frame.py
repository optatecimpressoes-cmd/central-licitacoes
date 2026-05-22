"""Tela de licitações"""
import customtkinter as ctk
from database import db
from datetime import datetime
from services.notifications_service import NotificationService
class LicitacoesFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.licitacoes = []
        self.criar_widgets()
    
    def criar_widgets(self):
        # Header
        frame_header = ctk.CTkFrame(self)
        frame_header.pack(fill="x", padx=20, pady=20)
        
        titulo = ctk.CTkLabel(
            frame_header,
            text="Licitações",
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
        
        btn_nova = ctk.CTkButton(
            frame_header,
            text="+ Nova",
            command=lambda: self.controller.mostrar_frame("NovaLicitacao"),
            width=100
        )
        btn_nova.pack(side="right", padx=5)
        
        # Filtro
        frame_filtro = ctk.CTkFrame(self)
        frame_filtro.pack(fill="x", padx=20, pady=10)
        
        label_filtro = ctk.CTkLabel(frame_filtro, text="Filtro:", font=("Arial", 12))
        label_filtro.pack(side="left", padx=5)
        
        self.entry_filtro = ctk.CTkEntry(
            frame_filtro,
            placeholder_text="Buscar por título, número ou órgão...",
            width=400
        )
        self.entry_filtro.pack(side="left", padx=5, fill="x", expand=True)
        
        btn_filtrar = ctk.CTkButton(
            frame_filtro,
            text="Filtrar",
            command=self.aplicar_filtro,
            width=100
        )
        btn_filtrar.pack(side="left", padx=5)
        
        # Tabela de licitações
        frame_tabela = ctk.CTkFrame(self)
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame para scroll
        self.frame_scroll = ctk.CTkScrollableFrame(frame_tabela, fg_color="transparent")
        self.frame_scroll.pack(fill="both", expand=True)
        
        self.carregar_licitacoes()
    
    def carregar_licitacoes(self):
        # Limpar frame anterior
        for widget in self.frame_scroll.winfo_children():
            widget.destroy()
        
        self.licitacoes = db.listar_licitacoes()
        
        if not self.licitacoes:
            label_vazio = ctk.CTkLabel(
                self.frame_scroll,
                text="Nenhuma licitação cadastrada",
                font=("Arial", 14)
            )
            label_vazio.pack(pady=20)
            return
        
        for licitacao in self.licitacoes:
            self.criar_card_licitacao(licitacao)
    
    def criar_card_licitacao(self, licitacao):
        card = ctk.CTkFrame(self.frame_scroll, fg_color="#2b2b2b")
        card.pack(fill="x", pady=10)
        
        # Conteúdo
        frame_conteudo = ctk.CTkFrame(card, fg_color="transparent")
        frame_conteudo.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Título e número
        label_titulo = ctk.CTkLabel(
            frame_conteudo,
            text=f"{licitacao['numero']} - {licitacao['titulo']}",
            font=("Arial", 14, "bold")
        )
        label_titulo.pack(anchor="w", pady=5)
        
        # Informações
        info_text = f"Órgão: {licitacao['orgao']} | Modalidade: {licitacao['modalidade']} | Status: {licitacao['status']}"
        label_info = ctk.CTkLabel(
            frame_conteudo,
            text=info_text,
            font=("Arial", 11),
            text_color="gray70"
        )
        label_info.pack(anchor="w", pady=2)
        
        # Datas e valor
        valor_formatado = f"R$ {licitacao['valor_estimado']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        datas_text = f"Abertura: {licitacao['data_abertura']} | Encerramento: {licitacao['data_encerramento']} | Valor: {valor_formatado}"
        label_datas = ctk.CTkLabel(
            frame_conteudo,
            text=datas_text,
            font=("Arial", 10),
            text_color="gray60"
        )
        label_datas.pack(anchor="w", pady=5)
        
        # Botões
        frame_botoes = ctk.CTkFrame(card, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=15, pady=10)
        
        btn_ver = ctk.CTkButton(
            frame_botoes,
            text="Visualizar",
            command=lambda: self.visualizar_licitacao(licitacao['id']),
            width=80,
            height=28
        )
        btn_ver.pack(side="left", padx=5)
        
        btn_editar = ctk.CTkButton(
            frame_botoes,
            text="Editar",
            command=lambda: self.editar_licitacao(licitacao['id']),
            width=80,
            height=28
        )
        btn_editar.pack(side="left", padx=5)
        
        btn_deletar = ctk.CTkButton(
            frame_botoes,
            text="Deletar",
            command=lambda: self.deletar_licitacao(licitacao['id']),
            width=80,
            height=28,
            fg_color="red"
        )
        btn_deletar.pack(side="left", padx=5)
    
    def aplicar_filtro(self):
        filtro = self.entry_filtro.get()
        
        # Limpar frame anterior
        for widget in self.frame_scroll.winfo_children():
            widget.destroy()
        
        if filtro:
            self.licitacoes = db.listar_licitacoes(filtro)
        else:
            self.licitacoes = db.listar_licitacoes()
        
        if not self.licitacoes:
            label_vazio = ctk.CTkLabel(
                self.frame_scroll,
                text="Nenhuma licitação encontrada",
                font=("Arial", 14)
            )
            label_vazio.pack(pady=20)
            return
        
        for licitacao in self.licitacoes:
            self.criar_card_licitacao(licitacao)
    
    def visualizar_licitacao(self, licitacao_id):
        # TODO: Implementar visualização detalhada
        print(f"Visualizar licitação {licitacao_id}")
    
    def editar_licitacao(self, licitacao_id):
        # TODO: Implementar edição
        print(f"Editar licitação {licitacao_id}")
    
    def deletar_licitacao(self, licitacao_id):
        db.deletar_licitacao(licitacao_id)
        self.carregar_licitacoes()


class NovaLicitacaoFrame(ctk.CTkFrame):
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
            text="Nova Licitação",
            font=("Arial", 24, "bold")
        )
        titulo.pack(side="left")
        
        btn_voltar = ctk.CTkButton(
            frame_header,
            text="← Voltar",
            command=lambda: self.controller.mostrar_frame("Licitacoes"),
            width=100
        )
        btn_voltar.pack(side="right")
        
        # Formulário
        frame_form = ctk.CTkScrollableFrame(self)
        frame_form.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Número
        label = ctk.CTkLabel(frame_form, text="Número da Licitação:", font=("Arial", 12))
        label.pack(anchor="w", pady=5)
        self.entry_numero = ctk.CTkEntry(frame_form, width=400)
        self.entry_numero.pack(anchor="w", pady=5)
        
        # Título
        label = ctk.CTkLabel(frame_form, text="Título:", font=("Arial", 12))
        label.pack(anchor="w", pady=5)
        self.entry_titulo = ctk.CTkEntry(frame_form, width=400)
        self.entry_titulo.pack(anchor="w", pady=5)
        
        # Descrição
        label = ctk.CTkLabel(frame_form, text="Descrição:", font=("Arial", 12))
        label.pack(anchor="w", pady=5)
        self.entry_descricao = ctk.CTkTextbox(frame_form, height=100, width=400)
        self.entry_descricao.pack(anchor="w", pady=5)
        
        # Órgão
        label = ctk.CTkLabel(frame_form, text="Órgão:", font=("Arial", 12))
        label.pack(anchor="w", pady=5)
        self.entry_orgao = ctk.CTkEntry(frame_form, width=400)
        self.entry_orgao.pack(anchor="w", pady=5)
        
        # Modalidade
        label = ctk.CTkLabel(frame_form, text="Modalidade:", font=("Arial", 12))
        label.pack(anchor="w", pady=5)
        self.combo_modalidade = ctk.CTkComboBox(
            frame_form,
            values=["Pregão", "Concorrência", "Dispensa", "Inexigibilidade"],
            width=400
        )
        self.combo_modalidade.pack(anchor="w", pady=5)
        
        # Data de abertura
        label = ctk.CTkLabel(frame_form, text="Data de Abertura (YYYY-MM-DD):", font=("Arial", 12))
        label.pack(anchor="w", pady=5)
        self.entry_data_abertura = ctk.CTkEntry(frame_form, width=400)
        self.entry_data_abertura.pack(anchor="w", pady=5)
        
        # Data de encerramento
        label = ctk.CTkLabel(frame_form, text="Data de Encerramento (YYYY-MM-DD):", font=("Arial", 12))
        label.pack(anchor="w", pady=5)
        self.entry_data_encerramento = ctk.CTkEntry(frame_form, width=400)
        self.entry_data_encerramento.pack(anchor="w", pady=5)
        
        # Valor estimado
        label = ctk.CTkLabel(frame_form, text="Valor Estimado (R$):", font=("Arial", 12))
        label.pack(anchor="w", pady=5)
        self.entry_valor = ctk.CTkEntry(frame_form, width=400)
        self.entry_valor.pack(anchor="w", pady=5)
        
        # Botões
        frame_botoes = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_botoes.pack(fill="x", pady=20)
        
        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            command=self.salvar_licitacao,
            width=120
        )
        btn_salvar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            command=lambda: self.controller.mostrar_frame("Licitacoes"),
            width=120,
            fg_color="gray60"
        )
        btn_cancelar.pack(side="left", padx=10)
        
        # Label de mensagem
        self.label_mensagem = ctk.CTkLabel(
            frame_form,
            text="",
            font=("Arial", 12),
            text_color="red"
        )
        self.label_mensagem.pack(pady=10)
    
    def salvar_licitacao(self):
        numero = self.entry_numero.get()
        titulo = self.entry_titulo.get()
        descricao = self.entry_descricao.get("1.0", "end")
        orgao = self.entry_orgao.get()
        modalidade = self.combo_modalidade.get()
        data_abertura = self.entry_data_abertura.get()
        data_encerramento = self.entry_data_encerramento.get()
        valor_str = self.entry_valor.get()
        
        if not all([numero, titulo, orgao, modalidade, data_abertura, data_encerramento, valor_str]):
            self.label_mensagem.configure(text="Preencha todos os campos obrigatórios", text_color="red")
            return
        
        try:
            valor = float(valor_str)
            usuario_id = self.controller.usuario_logado['id']
            
            id_novo = db.criar_licitacao(
                numero, titulo, descricao, orgao, modalidade,
                data_abertura, data_encerramento, valor, usuario_id
            )
            
            if id_novo:
                # Verificar e criar alertas automaticamente para todos os usuários
                self.verificar_e_criar_alertas(id_novo)
                
                self.label_mensagem.configure(text="Licitação criada com sucesso!", text_color="green")
                self.after(1500, lambda: self.controller.mostrar_frame("Licitacoes"))
            else:
                self.label_mensagem.configure(text="Número de licitação já existe", text_color="red")
        except ValueError:
            self.label_mensagem.configure(text="Valor deve ser um número", text_color="red")
    
    def verificar_e_criar_alertas(self, licitacao_id):
        """Verifica palavras-chave de todos os usuários e cria alertas se encontrar correspondências"""
        NotificationService.processar_nova_licitacao(licitacao_id)
