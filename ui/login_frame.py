"""Tela de login"""
import customtkinter as ctk
from database import db

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.criar_widgets()
    
    def criar_widgets(self):
        # Título
        titulo = ctk.CTkLabel(
            self,
            text="Central de Licitações",
            font=("Arial", 32, "bold")
        )
        titulo.pack(pady=40)
        
        # Frame de login
        frame_login = ctk.CTkFrame(self)
        frame_login.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Username
        label_user = ctk.CTkLabel(frame_login, text="Usuário:", font=("Arial", 14))
        label_user.pack(pady=10)
        self.entry_username = ctk.CTkEntry(
            frame_login,
            placeholder_text="Digite seu usuário",
            width=300
        )
        self.entry_username.pack(pady=5)
        
        # Senha
        label_senha = ctk.CTkLabel(frame_login, text="Senha:", font=("Arial", 14))
        label_senha.pack(pady=10)
        self.entry_senha = ctk.CTkEntry(
            frame_login,
            placeholder_text="Digite sua senha",
            show="*",
            width=300
        )
        self.entry_senha.pack(pady=5)
        
        # Botões
        frame_botoes = ctk.CTkFrame(frame_login, fg_color="transparent")
        frame_botoes.pack(pady=20)
        
        btn_login = ctk.CTkButton(
            frame_botoes,
            text="Login",
            command=self.fazer_login,
            width=120
        )
        btn_login.grid(row=0, column=0, padx=10)
        
        btn_registrar = ctk.CTkButton(
            frame_botoes,
            text="Registrar",
            command=self.abrir_registrar,
            width=120,
            fg_color="gray60"
        )
        btn_registrar.grid(row=0, column=1, padx=10)
        
        # Label de mensagem
        self.label_mensagem = ctk.CTkLabel(
            frame_login,
            text="",
            font=("Arial", 12),
            text_color="red"
        )
        self.label_mensagem.pack(pady=10)
    
    def fazer_login(self):
        username = self.entry_username.get()
        senha = self.entry_senha.get()
        
        if not username or not senha:
            self.label_mensagem.configure(text="Preencha todos os campos", text_color="red")
            return
        
        usuario = db.autenticar_usuario(username, senha)
        if usuario:
            self.controller.usuario_logado = dict(usuario)
            self.controller.mostrar_frame("Dashboard")
            self.entry_username.delete(0, "end")
            self.entry_senha.delete(0, "end")
        else:
            self.label_mensagem.configure(text="Usuário ou senha incorretos", text_color="red")
    
    def abrir_registrar(self):
        self.controller.mostrar_frame("Registrar")


class RegistroFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.criar_widgets()
    
    def criar_widgets(self):
        # Título
        titulo = ctk.CTkLabel(
            self,
            text="Criar Nova Conta",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=20)
        
        # Frame de registro
        frame_registro = ctk.CTkFrame(self)
        frame_registro.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Nome
        label_nome = ctk.CTkLabel(frame_registro, text="Nome Completo:", font=("Arial", 12))
        label_nome.pack(pady=5)
        self.entry_nome = ctk.CTkEntry(
            frame_registro,
            placeholder_text="Digite seu nome completo",
            width=300
        )
        self.entry_nome.pack(pady=5)
        
        # Email
        label_email = ctk.CTkLabel(frame_registro, text="Email:", font=("Arial", 12))
        label_email.pack(pady=5)
        self.entry_email = ctk.CTkEntry(
            frame_registro,
            placeholder_text="Digite seu email",
            width=300
        )
        self.entry_email.pack(pady=5)
        
        # Username
        label_user = ctk.CTkLabel(frame_registro, text="Usuário:", font=("Arial", 12))
        label_user.pack(pady=5)
        self.entry_username = ctk.CTkEntry(
            frame_registro,
            placeholder_text="Escolha um usuário",
            width=300
        )
        self.entry_username.pack(pady=5)
        
        # Senha
        label_senha = ctk.CTkLabel(frame_registro, text="Senha:", font=("Arial", 12))
        label_senha.pack(pady=5)
        self.entry_senha = ctk.CTkEntry(
            frame_registro,
            placeholder_text="Digite uma senha",
            show="*",
            width=300
        )
        self.entry_senha.pack(pady=5)
        
        # Botões
        frame_botoes = ctk.CTkFrame(frame_registro, fg_color="transparent")
        frame_botoes.pack(pady=20)
        
        btn_registrar = ctk.CTkButton(
            frame_botoes,
            text="Criar Conta",
            command=self.registrar_usuario,
            width=120
        )
        btn_registrar.grid(row=0, column=0, padx=10)
        
        btn_voltar = ctk.CTkButton(
            frame_botoes,
            text="Voltar",
            command=lambda: self.controller.mostrar_frame("Login"),
            width=120,
            fg_color="gray60"
        )
        btn_voltar.grid(row=0, column=1, padx=10)
        
        # Label de mensagem
        self.label_mensagem = ctk.CTkLabel(
            frame_registro,
            text="",
            font=("Arial", 12),
            text_color="red"
        )
        self.label_mensagem.pack(pady=10)
    
    def registrar_usuario(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        username = self.entry_username.get()
        senha = self.entry_senha.get()
        
        if not all([nome, email, username, senha]):
            self.label_mensagem.configure(text="Preencha todos os campos", text_color="red")
            return
        
        if len(senha) < 4:
            self.label_mensagem.configure(text="Senha deve ter pelo menos 4 caracteres", text_color="red")
            return
        
        sucesso = db.criar_usuario(username, senha, email, nome)
        if sucesso:
            self.label_mensagem.configure(text="Conta criada com sucesso! Faça login.", text_color="green")
            self.after(1500, lambda: self.controller.mostrar_frame("Login"))
        else:
            self.label_mensagem.configure(text="Usuário já existe", text_color="red")
