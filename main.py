# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont
from datetime import datetime
from tkcalendar import DateEntry
from tkinter import ttk
import jogos as jg
import telas as tl
from tkinter import ttk, messagebox

# --- Importações Novas ---
import api # Importa nosso novo arquivo de API
import dados # Importa o script de criação do banco

# --- Cores (do seu arquivo original) ---
co0 = "#2c1b47" 
co1 = "#f2e5b8" 
co2 = "#d4af37" 
co3 = "#8b5e3c" 
co4 = "#ffffff" 
co8 = "#228b22" 
co7 = "#3a2a5c" 
co9 = "#b22222" # Vermelho (para o botão Deslogar)
co10 = "#6c757d" # Cinza
co11 = "#f8f1dc" 

# --- CLASSE TELA DE LOGIN (Modificada) ---
class TelaLogin:
    def __init__(self, root, app_manager): # Alterado: recebe o AppManager
        self.root = root
        self.app_manager = app_manager # Armazena o gerenciador
        self.root.title("Login - Inventário")
        self.root.geometry("400x420") 
        self.root.configure(bg=co0)
        self.root.resizable(False, False)

        self.minha_fonte = tkFont.Font(family="MedievalSharp", size=26)
        self.font_geral = ("Arial", 12)
        self.font_botao = ("Arial", 12, "bold")

        self.frame_login = tk.Frame(self.root, bg=co1, bd=0, 
                                    highlightthickness=5, highlightbackground=co2)
        self.frame_login.pack(pady=40, padx=20, fill="both", expand=True)

        self.label_titulo = tk.Label(self.frame_login, text="Login", bg=co1, fg=co3, font=self.minha_fonte)
        self.label_titulo.pack(pady=20)

        self.frame_campos = tk.Frame(self.frame_login, bg=co1, bd=0)
        self.frame_campos.pack(pady=10, padx=20, fill="both", expand=True)
        self.frame_campos.grid_columnconfigure(0, weight=1) 

        # Campo Usuário
        tk.Label(self.frame_campos, text="Usuário", bg=co1, fg=co7, font=self.font_geral).grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")
        self.user_var = tk.StringVar()
        self.entry_user = tk.Entry(self.frame_campos, textvariable=self.user_var, font=self.font_geral, bg=co11, fg=co7, relief="solid", bd=1)
        self.entry_user.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Campo Senha
        tk.Label(self.frame_campos, text="Senha", bg=co1, fg=co7, font=self.font_geral).grid(row=2, column=0, padx=10, pady=(10,0), sticky="w")
        self.pass_var = tk.StringVar()
        self.entry_pass = tk.Entry(self.frame_campos, textvariable=self.pass_var, show="*", font=self.font_geral, bg=co11, fg=co7, relief="solid", bd=1)
        self.entry_pass.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # --- Botão 1: API Segura ---
        self.botao_login_seguro = tk.Button(self.frame_campos, text="Entrar (API Segura)", font=self.font_botao,
                                             bg=co8, fg=co4, relief="raised", bd=2, command=self.tentar_login_seguro)
        self.botao_login_seguro.grid(row=4, column=0, pady=(20, 5), padx=10, sticky="ew")
        
        # --- Botão 2: API Insegura ---
        self.botao_login_inseguro = tk.Button(self.frame_campos, text="Entrar (API Insegura)", font=self.font_botao,
                                             bg=co10, fg=co4, relief="raised", bd=2, command=self.tentar_login_inseguro)
        self.botao_login_inseguro.grid(row=5, column=0, pady=5, padx=10, sticky="ew")
        
        self.frame_campos.grid_rowconfigure(6, weight=1) 

    def tentar_login_seguro(self):
        """Chama a API segura (syncjava2.php)"""
        usuario = self.user_var.get()
        senha = self.pass_var.get()
        user_id, mensagem = api.login_api_segura(usuario, senha)
        
        # --- MENSAGEM NO TERMINAL ---
        print("\n" + "="*40)
        print("  RESULTADO DA TENTATIVA DE LOGIN")
        print(f"  API: Segura (syncjava2.php)")
        print(f"  Usuário: {usuario}")
        print(f"  Mensagem: {mensagem}")
        print("="*40 + "\n")

        if user_id:
            # Sucesso: chama o gerenciador
            self.app_manager.on_login_success(user_id, usuario, mensagem) 
        else:
            messagebox.showerror("Erro de Login (Seguro)", mensagem, parent=self.root)

    def tentar_login_inseguro(self):
        """Chama a API insegura (syncjava.php)"""
        usuario = self.user_var.get()
        senha = self.pass_var.get()
        user_id, mensagem = api.login_api_insegura(usuario, senha)
        
        # --- MENSAGEM NO TERMINAL ---
        print("\n" + "="*40)
        print("  RESULTADO DA TENTATIVA DE LOGIN")
        print(f"  API: Insegura (syncjava.php)")
        print(f"  Usuário: {usuario}")
        print(f"  Mensagem: {mensagem}")
        print("="*40 + "\n")

        if user_id:
            # Sucesso: chama o gerenciador
            self.app_manager.on_login_success(user_id, usuario, mensagem) 
        else:
            messagebox.showerror("Erro de Login (Inseguro)", mensagem, parent=self.root)


# --- CLASSE MeuApp (Inventário de Jogos)
class MeuApp:
    def __init__(self, janela, user_id, username, app_manager): # Alterado: recebe o AppManager
        self.janela = janela
        self.user_id = user_id 
        self.username = username
        self.app_manager = app_manager # Armazena o gerenciador
        
        self.janela.title(f"Inventário de Jogos (Usuário: {self.username})") 
        self.janela.geometry("800x600")
        self.janela.configure(bg=co0)
        self.janela.resizable(True, True) 

        minha_fonte = tkFont.Font(family="MedievalSharp", size= 26)
        self.font_geral = ("Arial", 12)
        self.font_botao = ("Arial", 12, "bold")

        style = ttk.Style(self.janela)
        style.theme_use('clam')
        style.configure("TCombobox",
                        fieldbackground=co11, background=co1, foreground=co7,
                        arrowcolor=co7, bordercolor=co3,
                        lightcolor=co1, darkcolor=co1)

        self.frame_principal = tk.Frame(self.janela, bg=co1, bd=0, 
                                        highlightthickness=5, highlightbackground=co2)
        self.frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

        # --- BOTÃO DESLOGAR ADICIONADO ---
        self.botao_deslogar = tk.Button(self.frame_principal, text="Deslogar", font=("Arial", 10, "bold"),
                                         bg=co9, fg=co4, relief="raised", bd=2, command=self.fazer_logout)
        # .place() permite posicionamento exato no canto
        self.botao_deslogar.place(relx=1.0, rely=0, x=-10, y=10, anchor="ne")


        self.label_titulo = tk.Label(self.frame_principal, text="Inventário de Jogos", bg=co1, fg=co3, font=minha_fonte)
        self.label_titulo.pack(pady=15) # Padding original

        self.frame_campos = tk.Frame(self.frame_principal, bg=co1, bd=0)
        self.frame_campos.pack(pady=10, padx=20, fill="x")
        self.frame_campos.grid_columnconfigure(1, weight=1) 

        # (O restante dos campos Nome, Plataforma, Lançamento, Status, Adicionar... é idêntico)
        # Campo Nome
        self.label_nome = tk.Label(self.frame_campos, text="Nome", bg=co1, fg=co7, font=self.font_geral)
        self.label_nome.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nome_var = tk.StringVar()
        self.entry_nome = tk.Entry(self.frame_campos, textvariable=self.nome_var, font=self.font_geral, bg=co11, fg=co7, relief="solid", bd=1)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        # Campo Plataforma
        self.label_plataforma = tk.Label(self.frame_campos, text="Plataforma", bg=co1, fg=co7, font=self.font_geral)
        self.label_plataforma.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.plataforma_var = tk.StringVar()
        self.entry_plataforma = tk.Entry(self.frame_campos, textvariable=self.plataforma_var, font=self.font_geral, bg=co11, fg=co7, relief="solid", bd=1)
        self.entry_plataforma.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        # Campo Lançamento
        self.label_lancamento = tk.Label(self.frame_campos, text="Lançamento", bg=co1, fg=co7, font=self.font_geral)
        self.label_lancamento.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_lancamento = DateEntry(
            self.frame_campos, font=self.font_geral, width=18,
            fieldbackground=co11, background=co3, foreground=co4,
            locale='pt_BR', date_pattern='y-mm-dd'
        )
        self.entry_lancamento.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        # Campo Status
        self.label_status = tk.Label(self.frame_campos, text="Status", bg=co1, fg=co7, font=self.font_geral)
        self.label_status.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        status_opcoes = ["Não Jogado", "Jogando", "Zerado"]
        self.status_var = tk.StringVar()
        self.combobox_status = ttk.Combobox(
            self.frame_campos, textvariable=self.status_var,
            values=status_opcoes, font=self.font_geral, state='readonly'
        )
        self.combobox_status.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.combobox_status.set("Não Jogado")
        # Botão Adicionar
        self.botao_adicionar = tk.Button(self.frame_campos, text="Adicionar", font=self.font_botao,
                                         bg=co8, fg=co4, relief="raised", bd=2, padx=10, command=self.adicionar_jogo)
        self.botao_adicionar.grid(row=4, column=1, pady=15, padx=10, sticky="e")

        # --- Área da Tabela ---
        style.configure("Jogo.Treeview",
                        background=co11, fieldbackground=co11,
                        foreground=co7, font=self.font_geral)
        style.configure("Jogo.Treeview.Heading",
                        background=co1, foreground=co7,
                        font=("Arial", 12, "bold"), relief="flat")
        style.map('Jogo.Treeview',
                background=[('selected', co3)],
                foreground=[('selected', co4)])
        
        self.frame_botoes = tk.Frame(self.frame_principal, bg=co1)
        self.frame_botoes.pack(pady=10, padx=20, fill="x", side="bottom")
        self.frame_botoes.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.frame_tabela = tk.Frame(self.frame_principal, bg=co1, bd=0)
        self.frame_tabela.pack(pady=10, padx=20, fill="both", expand=True)

        colunas = ("Id","Nome", "Plataforma", "Lançamento", "Status")
        scrollbar = tk.Scrollbar(self.frame_tabela)
        scrollbar.pack(side="right", fill="y")

        self.tabela_jogos = ttk.Treeview(self.frame_tabela, columns=colunas, show="headings", yscrollcommand=scrollbar.set, style="Jogo.Treeview")

        self.tabela_jogos.heading("Id", text="ID")
        self.tabela_jogos.heading("Nome", text="Nome")
        self.tabela_jogos.heading("Plataforma", text="Plataforma")
        self.tabela_jogos.heading("Lançamento", text="Lançamento")
        self.tabela_jogos.heading("Status", text="Status")

        self.tabela_jogos.column("Id", width=50, anchor="center")
        self.tabela_jogos.column("Nome", width=250)
        self.tabela_jogos.column("Plataforma", width=100, anchor="center")
        self.tabela_jogos.column("Lançamento", width=100, anchor="center")
        self.tabela_jogos.column("Status", width=120, anchor="center")

        self.tabela_jogos.pack(fill="both", expand=True)
        scrollbar.config(command=self.tabela_jogos.yview)

        self.atualizar_tabela() 

        # --- Botões (passando self.user_id) ---
        self.botao_editar = tk.Button(self.frame_botoes, text="Editar", font=self.font_botao, bg=co3, fg=co4, relief="raised", bd=2, width=12, 
                                      command=lambda: tl.janela_editar(self.janela, self.tabela_jogos, self.user_id))
        self.botao_editar.grid(row=0, column=0, padx=5, pady=10)
        
        self.botao_excluir = tk.Button(self.frame_botoes, text="Excluir", font=self.font_botao, bg=co3, fg=co4, relief="raised", bd=2, width=12, 
                                       command=lambda: tl.janela_excluir(self.janela, self.tabela_jogos, self.user_id))
        self.botao_excluir.grid(row=0, column=1, padx=5, pady=10)

        self.botao_buscar = tk.Button(self.frame_botoes, text="Buscar", font=self.font_botao, bg=co3, fg=co4, relief="raised", bd=2, width=12, 
                                      command=lambda: tl.janela_buscar(self.janela, self.tabela_jogos, self.user_id))
        self.botao_buscar.grid(row=0, column=2, padx=5, pady=10)

        self.botao_atualizar = tk.Button(self.frame_botoes, text="Atualizar", font=self.font_botao, bg=co3, fg=co4, relief="raised", bd=2, width=12, 
                                         command=self.atualizar_tabela)
        self.botao_atualizar.grid(row=0, column=3, pady=10)

    # --- MÉTODO DESLOGAR ADICIONADO ---
    def fazer_logout(self):
        print("[App] Usuário deslogou. Voltando para a tela de login.")
        self.app_manager.show_login_screen()

    def limpar_campos(self):
        self.nome_var.set("")
        self.plataforma_var.set("")
        self.entry_lancamento.set_date(datetime.now())
        self.status_var.set("Não Jogado")
    
    def adicionar_jogo(self):
        nome = self.nome_var.get()
        plataforma = self.plataforma_var.get()
        lancamento = self.entry_lancamento.get_date().strftime('%Y-%m-%d')
        status = self.status_var.get()

        if status == "Não Jogado":
            status = "Nao jogado"

        if nome and plataforma and lancamento and status:
            jg.adicionar(nome, plataforma, lancamento, status, self.user_id)
            self.atualizar_tabela()
            self.limpar_campos()
        else:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, preenche todos os campos.")

    def atualizar_tabela(self):
        for item in self.tabela_jogos.get_children():
            self.tabela_jogos.delete(item)

        jogos = jg.listar(self.user_id)  
        for jogo in jogos:
            self.tabela_jogos.insert("", "end", values=jogo[0:5])
        

class AppManager:
    def __init__(self, root):
        self.root = root
        self.current_screen = None

    def _clear_window(self):
        """Destrói todos os widgets na janela raiz."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Limpa a janela e mostra a tela de login."""
        self._clear_window()
        self.current_screen = TelaLogin(self.root, self)

    def on_login_success(self, user_id, username, msg_api_login):
        """Callback que a TelaLogin chama."""
        self._clear_window()
        
        # Mostra a mensagem de sucesso da API que foi usada para logar
        messagebox.showinfo("Sucesso no Login", msg_api_login, parent=self.root)
        
        # Inicia a aplicação principal
        self.current_screen = MeuApp(self.root, user_id, username, self)


# --- LÓGICA PRINCIPAL (Modificada para usar o AppManager) ---
if __name__ == "__main__":
    
    # 1. Garante que o banco de dados e as tabelas existam
    dados.criar_banco_de_dados()
    
    janela_raiz = tk.Tk()
    
    # 2. Cria o AppManager
    app_manager = AppManager(janela_raiz)
    
    # 3. Mostra a tela de login inicial
    app_manager.show_login_screen()
    
    # 4. Inicia o loop principal
    janela_raiz.mainloop()