"""Tela de Integração com ComprasNet"""
import customtkinter as ctk
from services.comprasnet_service import comprasnet_service
from database import db
import threading

class ComprasNetFrame(ctk.CTkFrame):
    """Tela para integração e sincronização com ComprasNet"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.status_conexao = False
        self.sincronizando = False
        self.criar_widgets()
    
    def criar_widgets(self):
        # Header
        frame_header = ctk.CTkFrame(self)
        frame_header.pack(fill="x", padx=20, pady=20)
        
        titulo = ctk.CTkLabel(
            frame_header,
            text="🌐 Integração ComprasNet",
            font=("Arial", 24, "bold")
        )
        titulo.pack(side="left")
        
        btn_voltar = ctk.CTkButton(
            frame_header,
            text="← Voltar",
            command=lambda: self.controller.mostrar_frame("Dashboard"),
            width=100
        )
        btn_voltar.pack(side="right")
        
        # Conteúdo principal
        frame_conteudo = ctk.CTkScrollableFrame(self)
        frame_conteudo.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Seção de Conexão
        self.criar_secao_conexao(frame_conteudo)
        
        # Divider
        divider1 = ctk.CTkFrame(frame_conteudo, height=2, fg_color="gray30")
        divider1.pack(fill="x", pady=20)
        
        # Seção de Sincronização
        self.criar_secao_sincronizacao(frame_conteudo)
        
        # Divider
        divider2 = ctk.CTkFrame(frame_conteudo, height=2, fg_color="gray30")
        divider2.pack(fill="x", pady=20)
        
        # Seção de Status
        self.criar_secao_status(frame_conteudo)
    
    def criar_secao_conexao(self, parent):
        """Seção para testar conexão com ComprasNet"""
        label_titulo = ctk.CTkLabel(
            parent,
            text="📡 Conectar ao ComprasNet",
            font=("Arial", 16, "bold")
        )
        label_titulo.pack(anchor="w", pady=10)
        
        label_desc = ctk.CTkLabel(
            parent,
            text="Teste e configure a conexão com o portal oficial de licitações do governo federal.",
            font=("Arial", 11),
            text_color="gray70"
        )
        label_desc.pack(anchor="w", pady=5)
        
        frame_botoes = ctk.CTkFrame(parent, fg_color="transparent")
        frame_botoes.pack(fill="x", pady=15)
        
        self.btn_conectar = ctk.CTkButton(
            frame_botoes,
            text="🔗 Testar Conexão",
            command=self.testar_conexao,
            height=40,
            width=150
        )
        self.btn_conectar.pack(side="left", padx=5)
        
        self.label_status_conexao = ctk.CTkLabel(
            frame_botoes,
            text="Status: Não testado",
            font=("Arial", 11),
            text_color="gray70"
        )
        self.label_status_conexao.pack(side="left", padx=20)
    
    def criar_secao_sincronizacao(self, parent):
        """Seção para sincronizar licitações"""
        label_titulo = ctk.CTkLabel(
            parent,
            text="🔄 Sincronizar Licitações",
            font=("Arial", 16, "bold")
        )
        label_titulo.pack(anchor="w", pady=10)
        
        label_desc = ctk.CTkLabel(
            parent,
            text="Busque licitações ativas no ComprasNet e as monitore com suas palavras-chave.",
            font=("Arial", 11),
            text_color="gray70"
        )
        label_desc.pack(anchor="w", pady=5)
        
        # Opções de filtro
        frame_filtros = ctk.CTkFrame(parent, fg_color="transparent")
        frame_filtros.pack(fill="x", pady=10)
        
        label_orgao = ctk.CTkLabel(frame_filtros, text="Órgão (opcional):", font=("Arial", 11))
        label_orgao.pack(side="left", padx=5)
        
        self.entry_orgao = ctk.CTkEntry(
            frame_filtros,
            placeholder_text="Ex: Prefeitura, Ministério...",
            width=200
        )
        self.entry_orgao.pack(side="left", padx=5)
        
        label_modal = ctk.CTkLabel(frame_filtros, text="Modalidade (opcional):", font=("Arial", 11))
        label_modal.pack(side="left", padx=5)
        
        self.combo_modalidade = ctk.CTkComboBox(
            frame_filtros,
            values=["Pregão", "Concorrência", "Dispensa", "Inexigibilidade", "Todas"],
            width=150
        )
        self.combo_modalidade.set("Todas")
        self.combo_modalidade.pack(side="left", padx=5)
        
        # Botão de sincronização
        frame_sync = ctk.CTkFrame(parent, fg_color="transparent")
        frame_sync.pack(fill="x", pady=15)
        
        self.btn_sincronizar = ctk.CTkButton(
            frame_sync,
            text="▶️ Iniciar Sincronização",
            command=self.sincronizar_licitacoes,
            height=40,
            width=180,
            fg_color="#059669"
        )
        self.btn_sincronizar.pack(side="left", padx=5)
        
        self.label_status_sync = ctk.CTkLabel(
            frame_sync,
            text="Pronto para sincronizar",
            font=("Arial", 11),
            text_color="gray70"
        )
        self.label_status_sync.pack(side="left", padx=20)
        
        # Progressbar
        self.progress_sync = ctk.CTkProgressBar(parent, width=400)
        self.progress_sync.set(0)
        self.progress_sync.pack(fill="x", pady=10)
        
        # Detalhes da sincronização
        frame_detalhes = ctk.CTkFrame(parent, fg_color="#2b2b2b")
        frame_detalhes.pack(fill="x", pady=10)
        
        self.label_detalhes = ctk.CTkLabel(
            frame_detalhes,
            text="Detalhes da sincronização aparecerão aqui...",
            font=("Arial", 10),
            text_color="gray70"
        )
        self.label_detalhes.pack(padx=15, pady=15, anchor="w")
    
    def criar_secao_status(self, parent):
        """Seção com histórico de sincronizações"""
        label_titulo = ctk.CTkLabel(
            parent,
            text="📋 Histórico de Sincronizações",
            font=("Arial", 16, "bold")
        )
        label_titulo.pack(anchor="w", pady=10)
        
        # Atualizar status
        self.atualizar_status_sincronizacoes(parent)
    
    def atualizar_status_sincronizacoes(self, parent):
        """Atualiza o histórico de sincronizações"""
        # Limpar widgets anteriores se existirem
        for widget in parent.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != parent:
                if "hist" in str(widget):
                    widget.destroy()
        
        ultimo_sync = db.obter_ultimo_sync_comprasnet()
        
        if ultimo_sync:
            frame_sync = ctk.CTkFrame(parent, fg_color="#2b2b2b")
            frame_sync.pack(fill="x", pady=5)
            
            info_text = f"📅 {ultimo_sync['data_sincronizacao']}"
            info_text += f" | 📦 {ultimo_sync['total_licitacoes']} licitações"
            info_text += f" | 🔔 {ultimo_sync['total_alertas']} alertas criados"
            info_text += f" | Status: {ultimo_sync['status']}"
            
            label_info = ctk.CTkLabel(
                frame_sync,
                text=info_text,
                font=("Arial", 10),
                text_color="white"
            )
            label_info.pack(padx=15, pady=10, anchor="w")
        else:
            label_vazio = ctk.CTkLabel(
                parent,
                text="Nenhuma sincronização realizada ainda.",
                font=("Arial", 11),
                text_color="gray70"
            )
            label_vazio.pack(pady=10)
    
    def testar_conexao(self):
        """Testa conexão com ComprasNet"""
        self.btn_conectar.configure(state="disabled", text="🔗 Testando...")
        self.label_status_conexao.configure(text="Status: Testando...", text_color="yellow")
        
        def teste():
            conectado = comprasnet_service.conectar_comprasnet()
            self.status_conexao = conectado
            
            if conectado:
                self.label_status_conexao.configure(
                    text="✅ Status: Conectado com sucesso",
                    text_color="green"
                )
            else:
                self.label_status_conexao.configure(
                    text="❌ Status: Falha na conexão",
                    text_color="red"
                )
            
            self.btn_conectar.configure(state="normal", text="🔗 Testar Conexão")
        
        thread = threading.Thread(target=teste)
        thread.daemon = True
        thread.start()
    
    def sincronizar_licitacoes(self):
        """Inicia sincronização com ComprasNet"""
        if self.sincronizando:
            return
        
        self.sincronizando = True
        self.btn_sincronizar.configure(state="disabled", text="▶️ Sincronizando...")
        self.label_status_sync.configure(text="Status: Sincronizando...", text_color="yellow")
        self.progress_sync.set(0)
        
        filtros = {}
        if self.entry_orgao.get():
            filtros['orgao'] = self.entry_orgao.get()
        if self.combo_modalidade.get() != "Todas":
            filtros['modalidade'] = self.combo_modalidade.get()
        
        def sincronizar():
            try:
                self.label_detalhes.configure(text="Buscando licitações no ComprasNet...")
                
                # Buscar licitações
                licitacoes = comprasnet_service.buscar_licitacoes_ativas(filtros)
                self.progress_sync.set(0.3)
                
                if not licitacoes:
                    self.label_detalhes.configure(
                        text="❌ Nenhuma licitação encontrada com os critérios especificados.",
                        text_color="red"
                    )
                    self.label_status_sync.configure(
                        text="Status: Sem resultados",
                        text_color="gray70"
                    )
                    return
                
                self.label_detalhes.configure(
                    text=f"✓ {len(licitacoes)} licitações encontradas. Processando...",
                    text_color="white"
                )
                
                # Sincronizar com banco
                alertas_total = 0
                licitacoes_adicionadas = 0
                
                for i, lic in enumerate(licitacoes):
                    if not db.verificar_licitacao_existente(lic['numero']):
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
                            licitacoes_adicionadas += 1
                            # Verificar palavras-chave
                            alertas_total += self._contar_alertas_licitacao(id_novo, lic)
                    
                    progress = 0.3 + (0.7 * (i + 1) / len(licitacoes))
                    self.progress_sync.set(progress)
                
                # Registrar sincronização
                db.registrar_sincronizacao_comprasnet(
                    total_licitacoes=licitacoes_adicionadas,
                    total_alertas=alertas_total,
                    status='Sucesso'
                )
                
                mensagem = f"✅ Sincronização concluída!\n"
                mensagem += f"  • {licitacoes_adicionadas} licitações adicionadas\n"
                mensagem += f"  • {alertas_total} alertas criados para seus interesses"
                
                self.label_detalhes.configure(text=mensagem, text_color="green")
                self.label_status_sync.configure(text="Status: Sincronizado com sucesso", text_color="green")
                self.progress_sync.set(1.0)
            
            except Exception as e:
                self.label_detalhes.configure(
                    text=f"❌ Erro: {str(e)}",
                    text_color="red"
                )
                self.label_status_sync.configure(text="Status: Erro", text_color="red")
            
            finally:
                self.sincronizando = False
                self.btn_sincronizar.configure(state="normal", text="▶️ Iniciar Sincronização")
        
        thread = threading.Thread(target=sincronizar)
        thread.daemon = True
        thread.start()
    
    def _contar_alertas_licitacao(self, licitacao_id, licitacao_dados):
        """Conta alertas gerados para uma licitação"""
        texto_licitacao = f"{licitacao_dados['numero']} {licitacao_dados['titulo']} {licitacao_dados.get('objeto', '')} {licitacao_dados['orgao']}".upper()
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, usuario_id, palavra FROM palavras_chave WHERE ativo = 1')
        todas_palavras = cursor.fetchall()
        conn.close()
        
        alertas = 0
        for palavra_obj in todas_palavras:
            if palavra_obj['palavra'] in texto_licitacao:
                db.criar_alerta(
                    usuario_id=palavra_obj['usuario_id'],
                    licitacao_id=licitacao_id,
                    palavra_chave_id=palavra_obj['id'],
                    tipo_alerta="comprasnet",
                    mensagem=f"Licitação encontrada no ComprasNet: {licitacao_dados['numero']}"
                )
                alertas += 1
        
        return alertas
