import tkinter as tk
import tkinter.font as tkFont
from datetime import datetime
from tkcalendar import DateEntry
from tkinter import ttk
import jogos as jg
import telas as tl
from tkinter import ttk, messagebox

co0 = "#2c1b47" # Roxo escuro (fundo principal)
co1 = "#f2e5b8" # Bege claro (fundo interno / caixas)
co2 = "#d4af37" # Dourado (bordas, títulos)
co3 = "#8b5e3c" # Marrom (borda interna, contraste)
co4 = "#ffffff" # Branco (texto principal)
co5 = "#ffcc00" # Amarelo ouro (destaque)
co6 = "#5a3e2b" # Marrom escuro (detalhes de botões/frames)
co7 = "#3a2a5c" # Roxo médio (gradiente/fundo secundário)
co8 = "#228b22" # Verde (botões de ação, ex: "Adicionar")
co9 = "#b22222" # Vermelho (botão de excluir / erro)
co10 = "#6c757d" # Cinza (neutro, desabilitado)
co11 = "#f8f1dc" # Marfim (contraste de fundo/tabela)

co12 = "#9b4503"

colors = ['#d4af37', '#f2e5b8', '#8b5e3c', '#3a2a5c', '#228b22', '#b22222']



class MeuApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Inventário de Jogos")
        self.janela.geometry("800x600")
        self.janela.configure(bg=co0)

        minha_fonte = tkFont.Font(family="MedievalSharp", size= 26)

        self.font_geral = ("Arial", 12)
        self.font_botao = ("Arial", 12, "bold")

        # Estilo do combox
        style = ttk.Style(self.janela)
        style.theme_use('clam')
        style.configure("TCombobox",
                        fieldbackground=co11,
                        background=co1,
                        foreground=co7,
                        arrowcolor=co7,
                        bordercolor=co3,
                        lightcolor=co1,
                        darkcolor=co1)

        #Widgets
        self.frame_principal = tk.Frame(self.janela, bg=co1, bd=0, 
                                        highlightthickness=5, highlightbackground=co2)
        self.frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        self.label_titulo = tk.Label(self.frame_principal, text="Inventário de Jogos", bg=co1, fg=co3, font=minha_fonte)
        self.label_titulo.pack(pady=15)

        # Campos de entrada
        self.frame_campos = tk.Frame(self.frame_principal, bg=co1, bd=0)
        self.frame_campos.pack(pady=10, padx=20, fill="x")
        self.frame_campos.grid_columnconfigure(1, weight=1) # Faz a coluna dos inputs expandir

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

        # Área de exibição dos jogos

        #Estilo da tabela
        style.configure("Jogo.Treeview",
                        background=co11,       # Fundo das linhas (marfim)
                        foreground=co7,        # Texto (roxo escuro)
                        fieldbackground=co11,  # Fundo da área vazia
                        font=self.font_geral)

        style.configure("Jogo.Treeview.Heading",
                        background=co1,
                        foreground=co7,
                        font=("Arial", 12, "bold"),
                        relief="flat")
        
        style.map('Jogo.Treeview',
                background=[('selected', co3)],
                foreground=[('selected', co4)])
        
        #frame dos botões e tabela
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

        #Botões editar, excluir, atualizar e buscar

        self.botao_editar = tk.Button(self.frame_botoes, text="Editar", font=self.font_botao, bg=co3, fg=co4, relief="raised", bd=2, width=12, command=lambda: tl.janela_editar(self.janela, self.tabela_jogos))
        self.botao_editar.grid(row=0, column=0, padx=5, pady=10)
        
        self.botao_excluir = tk.Button(self.frame_botoes, text="Excluir", font=self.font_botao, bg=co3, fg=co4, relief="raised", bd=2, width=12, command=lambda: tl.janela_excluir(self.janela, self.tabela_jogos))
        self.botao_excluir.grid(row=0, column=1, padx=5, pady=10)

        self.botao_buscar = tk.Button(self.frame_botoes, text="Buscar", font=self.font_botao, bg=co3, fg=co4, relief="raised", bd=2, width=12, command=lambda: tl.janela_buscar(self.janela, self.tabela_jogos))
        self.botao_buscar.grid(row=0, column=2, padx=5, pady=10)

        self.botao_atualizar = tk.Button(self.frame_botoes, text="Atualizar", font=self.font_botao, bg=co3, fg=co4, relief="raised", bd=2, width=12, command=self.atualizar_tabela)
        self.botao_atualizar.grid(row=0, column=3, padx=5, pady=10)

    def limpar_campos(self):
        self.nome_var.set("")
        self.plataforma_var.set("")
        self.entry_lancamento.set_date(datetime.now())
        self.status_var.set("Não Jogado")
    
    def adicionar_jogo(self):
        nome = self.nome_var.get()
        plataforma = self.plataforma_var.get()
        lancamento = self.entry_lancamento.get_date().strftime('%Y-%m-%d')

        if self.status_var.get() == "Não Jogado":
            status = "Nao jogado"
        else:
            status = self.status_var.get()

        if nome and plataforma and lancamento and status:
            jg.adicionar(nome, plataforma, lancamento, status)
            self.atualizar_tabela()
            self.limpar_campos()
        else:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, preenche todos os campos.")

    def atualizar_tabela(self):
        for item in self.tabela_jogos.get_children():
            self.tabela_jogos.delete(item)

        jogos = jg.listar()  
        for jogo in jogos:
            self.tabela_jogos.insert("", "end", values=jogo)
        
janela = tk.Tk()
app = MeuApp(janela)
janela.mainloop()

