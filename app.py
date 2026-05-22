"""Central de Licitações - Aplicação Principal"""
import customtkinter as ctk
from config import *
from ui.login_frame import LoginFrame, RegistroFrame
from ui.dashboard_frame import DashboardFrame
from ui.licitacao_frame import LicitacoesFrame, NovaLicitacaoFrame
from ui.alertas_frame import AlertasFrame, PalavrasChaveFrame
from ui.comprasnet_frame import ComprasNetFrame
from database import db

class CentralLicitacoesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(COLOR_THEME)
        
        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(1000, 600)
        
        # Variáveis de controle
        self.usuario_logado = None
        self.frames = {}
        
        # Container principal
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.container = container
        
        # Criar frames
        self.criar_frames()
        
        # Mostrar primeira tela
        self.mostrar_frame("Login")
    
    def criar_frames(self):
        """Cria todos os frames da aplicação"""
        frames_config = {
            "Login": LoginFrame,
            "Registrar": RegistroFrame,
            "Dashboard": DashboardFrame,
            "Licitacoes": LicitacoesFrame,
            "NovaLicitacao": NovaLicitacaoFrame,
            "Alertas": AlertasFrame,
            "PalavrasChave": PalavrasChaveFrame,
            "ComprasNet": ComprasNetFrame,
        }
        
        for nome, frame_class in frames_config.items():
            frame = frame_class(self.container, self)
            self.frames[nome] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_frame(self, nome):
        """Exibe um frame específico"""
        # Se for ir para Dashboard e usuário não está logado, volta para Login
        if nome == "Dashboard" and not self.usuario_logado:
            nome = "Login"
        
        frame = self.frames.get(nome)
        if frame:
            # Se for Licitações, recarregar dados
            if nome == "Licitacoes" and hasattr(frame, 'carregar_licitacoes'):
                frame.carregar_licitacoes()
            
            # Se for Alertas, recarregar notificações
            if nome == "Alertas" and hasattr(frame, 'carregar_alertas'):
                frame.carregar_alertas()
            
            # Se for Palavras-Chave, recarregar
            if nome == "PalavrasChave" and hasattr(frame, 'carregar_palavras'):
                frame.carregar_palavras()
            
            frame.tkraise()
            frame.focus()


if __name__ == "__main__":
    app = CentralLicitacoesApp()
    app.mainloop()